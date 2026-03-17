import os
import json
import sqlite3
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import quote_plus

import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# =========================
# 基础配置
# =========================
st.set_page_config(page_title="全球留学智能系统", layout="wide")

AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_BASE_URL = os.getenv("AI_BASE_URL", "").rstrip("/")
AI_MODEL = os.getenv("AI_MODEL", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)

DB_PATH = "study_agent.db"

# =========================
# 数据库
# =========================
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT,
    education TEXT,
    major TEXT,
    budget TEXT,
    goal TEXT,
    countries TEXT,
    languages TEXT,
    notes TEXT,
    updated_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    query TEXT,
    results_json TEXT,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    title TEXT,
    content TEXT,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    recipient TEXT,
    subject TEXT,
    body TEXT,
    status TEXT,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    title TEXT,
    due_date TEXT,
    status TEXT,
    source TEXT,
    created_at TEXT
)
""")

conn.commit()

# =========================
# 工具函数
# =========================
def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_profile(username: str):
    cursor.execute("""
        SELECT username, email, education, major, budget, goal, countries, languages, notes, updated_at
        FROM profiles WHERE username=?
    """, (username,))
    row = cursor.fetchone()
    if not row:
        return None
    return {
        "username": row[0],
        "email": row[1] or "",
        "education": row[2] or "",
        "major": row[3] or "",
        "budget": row[4] or "",
        "goal": row[5] or "",
        "countries": row[6] or "",
        "languages": row[7] or "",
        "notes": row[8] or "",
        "updated_at": row[9] or "",
    }

def save_profile(profile: dict):
    exists = get_profile(profile["username"])
    if exists:
        cursor.execute("""
            UPDATE profiles
            SET email=?, education=?, major=?, budget=?, goal=?, countries=?, languages=?, notes=?, updated_at=?
            WHERE username=?
        """, (
            profile["email"],
            profile["education"],
            profile["major"],
            profile["budget"],
            profile["goal"],
            profile["countries"],
            profile["languages"],
            profile["notes"],
            now_str(),
            profile["username"]
        ))
    else:
        cursor.execute("""
            INSERT INTO profiles (
                username, email, education, major, budget, goal, countries, languages, notes, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profile["username"],
            profile["email"],
            profile["education"],
            profile["major"],
            profile["budget"],
            profile["goal"],
            profile["countries"],
            profile["languages"],
            profile["notes"],
            now_str()
        ))
    conn.commit()

def save_search(username: str, query: str, results: list):
    cursor.execute("""
        INSERT INTO searches (username, query, results_json, created_at)
        VALUES (?, ?, ?, ?)
    """, (username, query, json.dumps(results, ensure_ascii=False), now_str()))
    conn.commit()

def save_plan(username: str, title: str, content: str):
    cursor.execute("""
        INSERT INTO plans (username, title, content, created_at)
        VALUES (?, ?, ?, ?)
    """, (username, title, content, now_str()))
    conn.commit()

def save_email(username: str, recipient: str, subject: str, body: str, status: str):
    cursor.execute("""
        INSERT INTO emails (username, recipient, subject, body, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, recipient, subject, body, status, now_str()))
    conn.commit()

def save_tasks(username: str, tasks: list, source="agent"):
    for t in tasks:
        cursor.execute("""
            INSERT INTO tasks (username, title, due_date, status, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            username,
            t.get("title", ""),
            t.get("due_date", ""),
            t.get("status", "pending"),
            source,
            now_str()
        ))
    conn.commit()

def get_user_plans(username: str):
    cursor.execute("""
        SELECT id, title, content, created_at
        FROM plans WHERE username=?
        ORDER BY id DESC
    """, (username,))
    return cursor.fetchall()

def get_user_emails(username: str):
    cursor.execute("""
        SELECT id, recipient, subject, body, status, created_at
        FROM emails WHERE username=?
        ORDER BY id DESC
    """, (username,))
    return cursor.fetchall()

def get_user_tasks(username: str):
    cursor.execute("""
        SELECT id, title, due_date, status, source, created_at
        FROM tasks WHERE username=?
        ORDER BY id DESC
    """, (username,))
    return cursor.fetchall()

def get_user_searches(username: str):
    cursor.execute("""
        SELECT id, query, results_json, created_at
        FROM searches WHERE username=?
        ORDER BY id DESC
    """, (username,))
    return cursor.fetchall()

# =========================
# 联网搜索
# =========================
def search_web_tavily(query: str, max_results=5):
    if not TAVILY_API_KEY:
        return []
    try:
        resp = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": max_results,
                "search_depth": "advanced",
                "include_answer": True
            },
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        items = []
        for r in data.get("results", []):
            items.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", "")
            })
        return items
    except Exception:
        return []

def search_web_duckduckgo(query: str, max_results=5):
    try:
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for a in soup.select(".result__title a")[:max_results]:
            title = a.get_text(" ", strip=True)
            href = a.get("href", "")
            results.append({"title": title, "url": href, "content": ""})
        return results
    except Exception:
        return []

def search_web(query: str, max_results=5):
    items = search_web_tavily(query, max_results=max_results)
    if items:
        return items
    return search_web_duckduckgo(query, max_results=max_results)

# =========================
# AI
# =========================
def ai_chat(system_prompt: str, user_prompt: str):
    if not AI_API_KEY or not AI_BASE_URL or not AI_MODEL:
        return None

    payload = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.4
    }

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(
            f"{AI_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[AI调用失败] {e}"

# =========================
# 规则引擎
# =========================
def recommend_countries(profile: dict):
    scores = {
        "加拿大": 0,
        "德国": 0,
        "荷兰": 0,
        "比利时": 0,
        "澳大利亚": 0,
        "英国": 0,
        "美国": 0
    }

    goal = profile.get("goal", "")
    budget = profile.get("budget", "")
    education = profile.get("education", "")
    languages = profile.get("languages", "").lower()

    if "移民" in goal:
        scores["加拿大"] += 4
        scores["澳大利亚"] += 3
        scores["德国"] += 2

    if "就业" in goal:
        scores["德国"] += 2
        scores["荷兰"] += 2
        scores["英国"] += 2
        scores["美国"] += 3

    if "低" in budget:
        scores["德国"] += 4
        scores["比利时"] += 2
    else:
        scores["英国"] += 1
        scores["美国"] += 1
        scores["澳大利亚"] += 1

    if "本科" in education:
        scores["加拿大"] += 2
        scores["荷兰"] += 1
    if "硕士" in education:
        scores["德国"] += 1
        scores["荷兰"] += 1
    if "博士" in education:
        scores["德国"] += 2
        scores["比利时"] += 1

    if "德" in languages:
        scores["德国"] += 2
    if "英" in languages:
        scores["加拿大"] += 1
        scores["荷兰"] += 1
        scores["英国"] += 1
        scores["美国"] += 1

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:3]

def fallback_plan(profile: dict, searches: list):
    countries = recommend_countries(profile)
    country_text = "、".join([c[0] for c in countries])
    search_summary = "\n".join(
        [f"- {r['title']} {r['url']}" for r in searches[:5]]
    ) if searches else "暂无联网结果"

    return f"""
# 个性化留学与就业规划

## 推荐国家
{country_text}

## 核心路径
1. 先锁定国家、学校层级、预算和身份目标。
2. 同步准备语言成绩、成绩单、简历、推荐信、文书。
3. 提前搜集签证、住宿、保险、医疗和城市生活信息。
4. 在入学后尽早做实习、科研、项目和导师联络。
5. 毕业前至少提前 6-12 个月开始求职与身份转换。

## 最近联网参考
{search_summary}

## 执行重点
- 每周检查官网更新
- 关键材料建立版本管理
- 学校、导师、租房、签证、就业分别建表
- 邮件模板和 follow-up 节奏固定
""".strip()

def build_tasks_from_plan():
    return [
        {"title": "整理成绩单、护照、语言成绩", "due_date": "本周", "status": "pending"},
        {"title": "建立学校/导师/官网数据库", "due_date": "本周", "status": "pending"},
        {"title": "搜索目标国家签证与住宿规则", "due_date": "3天内", "status": "pending"},
        {"title": "准备第一版简历和个人陈述", "due_date": "7天内", "status": "pending"},
        {"title": "生成并检查套磁/咨询邮件", "due_date": "7天内", "status": "pending"},
    ]

# =========================
# 邮件
# =========================
def build_email_draft(profile: dict, recipient_name: str, recipient_email: str, purpose: str):
    major = profile.get("major", "")
    education = profile.get("education", "")
    goal = profile.get("goal", "")

    subject = f"{education}申请咨询 - {major} - {purpose}"
    body = f"""Dear {recipient_name or 'Sir/Madam'},

I hope this email finds you well.

My name is {profile.get('username', '')}. I am currently preparing for overseas study/work planning in the field of {major}. My current stage is {education}, and my goal is {goal}.

I am writing to ask about {purpose}. I would be grateful if you could share any relevant information regarding admission requirements, application timeline, funding opportunities, or recommended preparation steps.

Thank you very much for your time and consideration.

Best regards,
{profile.get('username', '')}
Email: {profile.get('email', '')}
""".strip()

    # AI 优化
    if AI_API_KEY and AI_BASE_URL and AI_MODEL:
        improved = ai_chat(
            "You are an expert education counselor and academic email writer. Improve the email. Keep it professional, concise, and natural.",
            f"Profile: {json.dumps(profile, ensure_ascii=False)}\nRecipient: {recipient_name} <{recipient_email}>\nPurpose: {purpose}\nDraft:\n{body}"
        )
        if improved and not improved.startswith("[AI调用失败]"):
            body = improved

    return subject, body

def send_email(recipient: str, subject: str, body: str):
    if not (SMTP_HOST and SMTP_PORT and SMTP_USER and SMTP_PASS and SMTP_FROM):
        return False, "SMTP 未配置完整"

    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_FROM
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_FROM, recipient, msg.as_string())
        server.quit()
        return True, "发送成功"
    except Exception as e:
        return False, f"发送失败: {e}"

# =========================
# Agent
# =========================
def run_agent(username: str, profile: dict, user_goal: str):
    logs = []
    logs.append("1. 读取用户画像")
    logs.append(json.dumps(profile, ensure_ascii=False, indent=2))

    queries = [
        f"{profile.get('major', '')} study opportunities {profile.get('countries', '')}",
        f"{profile.get('countries', '')} student visa official site",
        f"{profile.get('countries', '')} student accommodation guide",
        f"{profile.get('countries', '')} international student health insurance",
        f"{profile.get('countries', '')} graduate jobs {profile.get('major', '')}"
    ]

    web_results = []
    logs.append("2. 联网搜索")
    for q in queries:
        items = search_web(q, max_results=3)
        web_results.extend(items)
        logs.append(f"- 搜索: {q} -> {len(items)} 条")

    save_search(username, " | ".join(queries), web_results)

    logs.append("3. 生成个性化规划")
    system_prompt = """
你是全球留学与长期发展规划专家。请根据用户背景和联网信息，输出周到全面的中文规划。
必须覆盖：
1. 国家和学校策略
2. 导师/官网/申请路径
3. 签证与身份
4. 租房、求医、保险、购物、交通
5. 邮件联络策略
6. 实习、就业、长期身份
7. 本周可执行任务
8. 风险提醒
""".strip()

    user_prompt = f"""
用户画像：
{json.dumps(profile, ensure_ascii=False)}

用户目标：
{user_goal}

联网结果：
{json.dumps(web_results[:12], ensure_ascii=False)}
""".strip()

    plan = ai_chat(system_prompt, user_prompt)
    if not plan or plan.startswith("[AI调用失败]"):
        logs.append("AI 不可用，切换到本地规则规划")
        plan = fallback_plan(profile, web_results)

    plan_title = f"智能规划 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    save_plan(username, plan_title, plan)

    logs.append("4. 生成任务")
    tasks = build_tasks_from_plan()
    save_tasks(username, tasks, source="agent")

    return plan, logs, web_results, tasks

# =========================
# UI
# =========================
st.title("🌍 全球留学智能操作系统")
st.caption("联网搜索｜邮件草稿｜SMTP 发信｜AI Agent｜规划与任务")

with st.sidebar:
    st.header("账户")
    username = st.text_input("用户名", value=st.session_state.get("username", ""))
    if st.button("载入/切换用户"):
        if username.strip():
            st.session_state["username"] = username.strip()
            st.success(f"当前用户：{username.strip()}")
        else:
            st.warning("请输入用户名")

    current_user = st.session_state.get("username", "")
    if current_user:
        st.info(f"当前用户：{current_user}")
    else:
        st.warning("先在这里输入用户名并点击“载入/切换用户”")

    st.markdown("---")
    st.write("配置状态")
    st.write(f"AI: {'已配置' if AI_API_KEY and AI_BASE_URL and AI_MODEL else '未配置'}")
    st.write(f"搜索: {'Tavily已配置' if TAVILY_API_KEY else '使用DuckDuckGo简易搜索'}")
    st.write(f"SMTP: {'已配置' if SMTP_HOST and SMTP_USER and SMTP_PASS else '未配置'}")

tabs = st.tabs([
    "个人画像",
    "联网搜索",
    "智能规划",
    "邮件中心",
    "任务中心",
    "历史记录"
])

# 个人画像
with tabs[0]:
    st.subheader("个人画像")
    if not current_user:
        st.warning("请先在左侧输入用户名")
    else:
        profile = get_profile(current_user) or {
            "username": current_user,
            "email": "",
            "education": "",
            "major": "",
            "budget": "",
            "goal": "",
            "countries": "",
            "languages": "",
            "notes": "",
        }

        with st.form("profile_form"):
            email = st.text_input("邮箱", value=profile["email"])
            education = st.selectbox("当前阶段", ["本科", "硕士", "博士", "工作"], index=0 if profile["education"] == "" else ["本科", "硕士", "博士", "工作"].index(profile["education"]))
            major = st.text_input("专业", value=profile["major"])
            budget = st.selectbox("预算", ["低", "中", "高"], index=0 if profile["budget"] == "" else ["低", "中", "高"].index(profile["budget"]) if profile["budget"] in ["低", "中", "高"] else 0)
            goal = st.text_input("目标", value=profile["goal"], placeholder="移民 / 就业 / 读博 / 转专业")
            countries = st.text_input("目标国家", value=profile["countries"], placeholder="德国, 荷兰, 加拿大")
            languages = st.text_input("语言能力", value=profile["languages"], placeholder="英语, 德语")
            notes = st.text_area("补充说明", value=profile["notes"], height=120, placeholder="预算限制、家庭情况、奖学金需求、是否接受小语种等")
            submitted = st.form_submit_button("保存画像")

        if submitted:
            save_profile({
                "username": current_user,
                "email": email,
                "education": education,
                "major": major,
                "budget": budget,
                "goal": goal,
                "countries": countries,
                "languages": languages,
                "notes": notes
            })
            st.success("已保存")

        ranked = recommend_countries(get_profile(current_user) or {})
        if ranked:
            st.markdown("#### 推荐国家")
            for name, score in ranked:
                st.write(f"- {name}（评分 {score}）")

# 联网搜索
with tabs[1]:
    st.subheader("联网搜索")
    if not current_user:
        st.warning("请先在左侧输入用户名")
    else:
        q = st.text_input("输入搜索问题", placeholder="例如：德国计算机硕士申请官网")
        if st.button("开始搜索"):
            if not q.strip():
                st.warning("请输入搜索内容")
            else:
                with st.spinner("搜索中..."):
                    results = search_web(q, max_results=8)
                    save_search(current_user, q, results)
                st.success(f"已获取 {len(results)} 条结果")
                for i, item in enumerate(results, 1):
                    st.markdown(f"**{i}. {item['title']}**")
                    if item["url"]:
                        st.write(item["url"])
                    if item["content"]:
                        st.caption(item["content"])

# 智能规划
with tabs[2]:
    st.subheader("智能规划 / AI Agent")
    if not current_user:
        st.warning("请先在左侧输入用户名")
    else:
        profile = get_profile(current_user)
        if not profile:
            st.warning("请先填写个人画像")
        else:
            agent_goal = st.text_area(
                "你希望系统帮你做什么",
                value="请基于我的背景，联网搜索并给我一份从申请到签证、租房、求医、购物、就业、长期身份的周到全面规划。",
                height=100
            )

            if st.button("运行智能 Agent"):
                with st.spinner("Agent 正在联网、分析、生成规划..."):
                    plan, logs, web_results, tasks = run_agent(current_user, profile, agent_goal)

                st.markdown("### 生成结果")
                st.markdown(plan)

                st.markdown("### Agent 日志")
                for line in logs:
                    st.code(line)

                st.markdown("### 本次联网结果")
                for i, item in enumerate(web_results[:10], 1):
                    st.write(f"{i}. {item.get('title', '')}")
                    if item.get("url"):
                        st.caption(item["url"])

                st.markdown("### 已生成任务")
                for t in tasks:
                    st.write(f"- {t['title']} ｜ {t['due_date']} ｜ {t['status']}")

# 邮件中心
with tabs[3]:
    st.subheader("邮件中心")
    if not current_user:
        st.warning("请先在左侧输入用户名")
    else:
        profile = get_profile(current_user)
        if not profile:
            st.warning("请先填写个人画像")
        else:
            recipient_name = st.text_input("收件人姓名", placeholder="Professor Smith / Admissions Office")
            recipient_email = st.text_input("收件人邮箱", placeholder="professor@example.edu")
            purpose = st.text_input("邮件目的", placeholder="申请咨询 / 套磁 / 奖学金咨询 / 跟进")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("生成邮件草稿"):
                    if not recipient_email or not purpose:
                        st.warning("请填写收件人邮箱和邮件目的")
                    else:
                        subject, body = build_email_draft(profile, recipient_name, recipient_email, purpose)
                        st.session_state["draft_subject"] = subject
                        st.session_state["draft_body"] = body
                        st.success("已生成草稿")

            draft_subject = st.text_input("主题", value=st.session_state.get("draft_subject", ""))
            draft_body = st.text_area("正文", value=st.session_state.get("draft_body", ""), height=260)

            with col2:
                if st.button("保存草稿"):
                    save_email(current_user, recipient_email, draft_subject, draft_body, "draft")
                    st.success("草稿已保存")

                if st.button("直接发送邮件"):
                    ok, msg = send_email(recipient_email, draft_subject, draft_body)
                    save_email(current_user, recipient_email, draft_subject, draft_body, "sent" if ok else "failed")
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)

# 任务中心
with tabs[4]:
    st.subheader("任务中心")
    if not current_user:
        st.warning("请先在左侧输入用户名")
    else:
        rows = get_user_tasks(current_user)
        if not rows:
            st.info("暂无任务")
        else:
            for row in rows:
                st.write(f"#{row[0]} | {row[1]} | 截止: {row[2]} | 状态: {row[3]} | 来源: {row[4]} | 创建于: {row[5]}")

# 历史记录
with tabs[5]:
    st.subheader("历史记录")
    if not current_user:
        st.warning("请先在左侧输入用户名")
    else:
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("#### 规划")
            plans = get_user_plans(current_user)
            if not plans:
                st.caption("暂无")
            for p in plans[:10]:
                with st.expander(f"{p[1]} | {p[3]}"):
                    st.markdown(p[2])

        with c2:
            st.markdown("#### 邮件")
            emails = get_user_emails(current_user)
            if not emails:
                st.caption("暂无")
            for e in emails[:10]:
                with st.expander(f"{e[2]} | {e[5]} | {e[4]}"):
                    st.write(f"收件人: {e[1]}")
                    st.text(e[3])

        with c3:
            st.markdown("#### 搜索")
            searches = get_user_searches(current_user)
            if not searches:
                st.caption("暂无")
            for s in searches[:10]:
                with st.expander(f"{s[1]} | {s[3]}"):
                    try:
                        items = json.loads(s[2])
                        for item in items[:5]:
                            st.write(f"- {item.get('title', '')}")
                            if item.get("url"):
                                st.caption(item["url"])
                    except Exception:
                        st.write(s[2])
