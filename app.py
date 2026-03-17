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
# 页面配置
# =========================
st.set_page_config(
    page_title="全球留学智能系统",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# 环境变量
# =========================
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
# 样式
# =========================
st.markdown("""
<style>
:root {
    --bg: #f6f8fc;
    --card: #ffffff;
    --line: #e7ebf3;
    --text: #1f2a44;
    --muted: #6b7280;
    --brand: #315efb;
    --brand2: #6b7cff;
    --ok: #15a34a;
    --warn: #d97706;
    --danger: #dc2626;
}

html, body, [class*="css"]  {
    font-family: Inter, "PingFang SC", "Microsoft YaHei", sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #f7f9ff 0%, #f6f8fc 100%);
}

.block-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 20px 22px;
    box-shadow: 0 10px 30px rgba(49, 94, 251, 0.06);
    margin-bottom: 16px;
}

.hero {
    background: linear-gradient(135deg, #315efb 0%, #6b7cff 100%);
    color: white;
    border-radius: 24px;
    padding: 28px 30px;
    box-shadow: 0 16px 40px rgba(49, 94, 251, 0.22);
    margin-bottom: 18px;
}

.hero h1 {
    margin: 0 0 8px 0;
    font-size: 38px;
    font-weight: 800;
}

.hero p {
    margin: 0;
    opacity: 0.95;
    font-size: 16px;
}

.kpi {
    background: white;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 8px 22px rgba(0,0,0,0.04);
}

.kpi .num {
    font-size: 30px;
    font-weight: 800;
    color: var(--brand);
    margin-bottom: 6px;
}

.kpi .label {
    font-size: 13px;
    color: var(--muted);
}

.section-title {
    font-size: 24px;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 10px;
}

.small-muted {
    color: var(--muted);
    font-size: 13px;
}

.module-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
}
.module-card {
    background: white;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 18px;
    min-height: 132px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.04);
}
.module-card h4 {
    margin: 0 0 10px 0;
    font-size: 18px;
}
.module-card p {
    margin: 0;
    color: var(--muted);
    line-height: 1.65;
    font-size: 14px;
}

.hr {
    height: 1px;
    background: var(--line);
    margin: 8px 0 18px 0;
}

.status-ok { color: var(--ok); font-weight: 700; }
.status-warn { color: var(--warn); font-weight: 700; }
.status-danger { color: var(--danger); font-weight: 700; }

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 14px 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.04);
}

div.stButton > button {
    border-radius: 12px !important;
    border: 1px solid #dbe3ff !important;
    background: linear-gradient(180deg, #ffffff 0%, #f8faff 100%) !important;
    color: #234 !important;
    font-weight: 700 !important;
    min-height: 42px !important;
}

div.stDownloadButton > button {
    border-radius: 12px !important;
}

@media (max-width: 900px) {
    .module-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

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
        return [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", "")
            }
            for r in data.get("results", [])
        ]
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
            results.append({
                "title": a.get_text(" ", strip=True),
                "url": a.get("href", ""),
                "content": ""
            })
        return results
    except Exception:
        return []

def search_web(query: str, max_results=5):
    items = search_web_tavily(query, max_results=max_results)
    return items if items else search_web_duckduckgo(query, max_results=max_results)

# =========================
# AI
# =========================
def ai_chat(system_prompt: str, user_prompt: str):
    if not AI_API_KEY or not AI_BASE_URL or not AI_MODEL:
        return None

    try:
        resp = requests.post(
            f"{AI_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {AI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": AI_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.4
            },
            timeout=60
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[AI调用失败] {e}"

# =========================
# 规则与 Agent
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

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

def fallback_plan(profile: dict, searches: list):
    ranked = recommend_countries(profile)
    country_text = "、".join([c[0] for c in ranked]) if ranked else "待分析"
    refs = "\n".join([f"- {r['title']} {r['url']}" for r in searches[:5]]) if searches else "暂无"

    return f"""
# 个性化留学全流程规划

## 推荐国家
{country_text}

## 申请与材料
- 明确主申国家和保底国家
- 建立学校、导师、官网和截止日期表
- 整理成绩单、语言成绩、简历、推荐信、文书

## 签证与身份
- 收集官方签证页面
- 准备资金、保险、住宿、录取相关证明
- 记录签证预约和补材料节点

## 落地生活
- 提前找住宿
- 办银行卡、电话卡、医保
- 熟悉求医、超市、交通与安全规则

## 就业与长期发展
- 从入学开始准备实习和简历
- 毕业前 6-12 个月开始求职
- 提前规划工签、蓝卡、长期居留或永居路径

## 联网参考
{refs}
""".strip()

def build_tasks_from_plan():
    return [
        {"title": "建立学校/导师/签证/租房数据库", "due_date": "本周", "status": "pending"},
        {"title": "整理语言成绩、成绩单、护照和简历", "due_date": "3天内", "status": "pending"},
        {"title": "搜索目标国家签证、住宿、医保官网", "due_date": "3天内", "status": "pending"},
        {"title": "完成第一版文书与邮件模板", "due_date": "7天内", "status": "pending"},
        {"title": "开始导师/项目联络与跟进", "due_date": "7天内", "status": "pending"},
    ]

def run_agent(username: str, profile: dict, user_goal: str):
    logs = []
    queries = [
        f"{profile.get('major', '')} study opportunities {profile.get('countries', '')}",
        f"{profile.get('countries', '')} student visa official site",
        f"{profile.get('countries', '')} student accommodation guide",
        f"{profile.get('countries', '')} health insurance international students",
        f"{profile.get('countries', '')} jobs for {profile.get('major', '')}"
    ]

    web_results = []
    for q in queries:
        items = search_web(q, max_results=3)
        web_results.extend(items)
        logs.append(f"搜索：{q} -> {len(items)} 条")

    save_search(username, " | ".join(queries), web_results)

    system_prompt = """
你是全球留学、签证、落地生活和长期身份规划专家。
请根据用户背景和联网结果，输出一份周到全面的中文规划。
必须覆盖：
1. 国家和学校策略
2. 导师/官网/申请路径
3. 签证与身份
4. 租房、求医、保险、购物、交通
5. 邮件联络策略
6. 实习、就业、长期身份
7. 本周任务
8. 风险提醒
""".strip()

    user_prompt = f"""
用户画像：
{json.dumps(profile, ensure_ascii=False)}

用户目标：
{user_goal}

联网信息：
{json.dumps(web_results[:12], ensure_ascii=False)}
""".strip()

    plan = ai_chat(system_prompt, user_prompt)
    if not plan or str(plan).startswith("[AI调用失败]"):
        plan = fallback_plan(profile, web_results)
        logs.append("AI 不可用，使用本地规划")

    title = f"智能规划 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    save_plan(username, title, plan)

    tasks = build_tasks_from_plan()
    save_tasks(username, tasks, source="agent")

    return plan, logs, web_results, tasks

# =========================
# 邮件
# =========================
def build_email_draft(profile: dict, recipient_name: str, recipient_email: str, purpose: str):
    subject = f"{profile.get('education', '')}申请咨询 - {profile.get('major', '')} - {purpose}"
    base = f"""Dear {recipient_name or "Sir/Madam"},

I hope this email finds you well.

My name is {profile.get("username", "")}. I am currently planning my overseas study/career path in {profile.get("major", "")}. My current stage is {profile.get("education", "")}, and my goal is {profile.get("goal", "")}.

I am writing to ask about {purpose}. I would be grateful if you could share any relevant information regarding requirements, timeline, funding, or recommended preparation steps.

Thank you very much for your time and consideration.

Best regards,
{profile.get("username", "")}
Email: {profile.get("email", "")}
""".strip()

    improved = ai_chat(
        "You are an expert academic email writer. Improve the email and keep it concise, natural and professional.",
        f"Profile: {json.dumps(profile, ensure_ascii=False)}\nRecipient:{recipient_name} <{recipient_email}>\nPurpose:{purpose}\nDraft:\n{base}"
    )
    body = improved if improved and not str(improved).startswith("[AI调用失败]") else base
    return subject, body

def send_email(recipient: str, subject: str, body: str):
    if not (SMTP_HOST and SMTP_USER and SMTP_PASS and SMTP_FROM):
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
# 顶部欢迎区
# =========================
st.markdown("""
<div class="hero">
    <h1>🌍 全球留学智能系统</h1>
    <p>联网搜索、学校与签证信息整合、邮件唤起、AI Agent 规划、任务分解、长期发展路径，一站式完成。</p>
</div>
""", unsafe_allow_html=True)

# =========================
# 侧边栏
# =========================
with st.sidebar:
    st.markdown("## 控制台")
    username_input = st.text_input("用户名", value=st.session_state.get("username", ""))
    if st.button("载入用户"):
        if username_input.strip():
            st.session_state["username"] = username_input.strip()
            st.success(f"已载入：{username_input.strip()}")
        else:
            st.warning("请输入用户名")

    current_user = st.session_state.get("username", "")

    st.markdown("---")
    st.markdown("### 状态")
    st.write(f"当前用户：{current_user or '未设置'}")
    st.write(f"AI：{'已配置' if AI_API_KEY and AI_BASE_URL and AI_MODEL else '未配置'}")
    st.write(f"搜索：{'Tavily' if TAVILY_API_KEY else 'DuckDuckGo 简易模式'}")
    st.write(f"邮件：{'已配置 SMTP' if SMTP_HOST and SMTP_USER and SMTP_PASS else '未配置'}")

    st.markdown("---")
    page = st.radio(
        "页面导航",
        ["总览", "个人画像", "联网搜索", "AI规划", "邮件中心", "任务中心", "历史中心"]
    )

# =========================
# 数据统计
# =========================
def get_counts(username):
    if not username:
        return 0, 0, 0, 0
    cursor.execute("SELECT COUNT(*) FROM plans WHERE username=?", (username,))
    p = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE username=?", (username,))
    t = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM emails WHERE username=?", (username,))
    e = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM searches WHERE username=?", (username,))
    s = cursor.fetchone()[0]
    return p, t, e, s

# =========================
# 页面：总览
# =========================
if page == "总览":
    p_count, t_count, e_count, s_count = get_counts(current_user)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("规划总数", p_count)
    with c2:
        st.metric("任务总数", t_count)
    with c3:
        st.metric("邮件记录", e_count)
    with c4:
        st.metric("搜索记录", s_count)

    st.markdown('<div class="section-title">系统模块</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="module-grid">
        <div class="module-card">
            <h4>👤 用户画像</h4>
            <p>记录学历、专业、预算、目标国家、语言能力和长期诉求，作为后续推荐和 Agent 规划的基础。</p>
        </div>
        <div class="module-card">
            <h4>🌐 联网搜索</h4>
            <p>搜索学校官网、签证规则、住宿、医保、求职和城市信息，尽量减少静态内容的局限。</p>
        </div>
        <div class="module-card">
            <h4>🤖 AI 规划</h4>
            <p>将用户背景与联网结果整合成一份完整路线图，覆盖申请、签证、生活和就业。</p>
        </div>
        <div class="module-card">
            <h4>✉️ 邮件中心</h4>
            <p>生成导师、项目方、招生办公室邮件草稿，并可通过 SMTP 直接发送。</p>
        </div>
        <div class="module-card">
            <h4>🗂 任务系统</h4>
            <p>把规划拆成短期可执行步骤，让用户知道这周、这几天该做什么。</p>
        </div>
        <div class="module-card">
            <h4>📚 历史中心</h4>
            <p>保存过去的搜索、规划、任务和邮件，形成长期记忆和可追踪档案。</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    left, right = st.columns([1.5, 1])
    with left:
        st.markdown('<div class="block-card">', unsafe_allow_html=True)
        st.markdown("### 适合你的使用顺序")
        st.write("1. 先创建用户并填写个人画像")
        st.write("2. 再做联网搜索，收集目标国家和项目资料")
        st.write("3. 然后运行 AI Agent 生成完整规划")
        st.write("4. 接着生成邮件草稿，联系学校、导师或招生办公室")
        st.write("5. 最后在任务中心持续推进")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="block-card">', unsafe_allow_html=True)
        st.markdown("### 当前建议")
        if not current_user:
            st.warning("先在左侧输入用户名并载入。")
        else:
            profile = get_profile(current_user)
            if not profile:
                st.info("下一步：去“个人画像”填写基本信息。")
            else:
                st.success("下一步：去“AI规划”运行 Agent。")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 页面：个人画像
# =========================
elif page == "个人画像":
    st.markdown('<div class="section-title">个人画像</div>', unsafe_allow_html=True)

    if not current_user:
        st.warning("请先在左侧输入用户名并载入。")
    else:
        profile = get_profile(current_user) or {
            "username": current_user,
            "email": "",
            "education": "本科",
            "major": "",
            "budget": "低",
            "goal": "",
            "countries": "",
            "languages": "",
            "notes": "",
        }

        left, right = st.columns([1.3, 1])

        with left:
            st.markdown('<div class="block-card">', unsafe_allow_html=True)
            with st.form("profile_form"):
                email = st.text_input("邮箱", value=profile["email"])
                education = st.selectbox("当前阶段", ["本科", "硕士", "博士", "工作"], index=["本科", "硕士", "博士", "工作"].index(profile["education"]) if profile["education"] in ["本科", "硕士", "博士", "工作"] else 0)
                major = st.text_input("专业", value=profile["major"])
                budget = st.selectbox("预算", ["低", "中", "高"], index=["低", "中", "高"].index(profile["budget"]) if profile["budget"] in ["低", "中", "高"] else 0)
                goal = st.text_input("目标", value=profile["goal"], placeholder="移民 / 就业 / 读博 / 奖学金")
                countries = st.text_input("目标国家", value=profile["countries"], placeholder="德国, 荷兰, 加拿大")
                languages = st.text_input("语言能力", value=profile["languages"], placeholder="英语, 德语")
                notes = st.text_area("补充说明", value=profile["notes"], height=150, placeholder="预算限制、家庭因素、是否接受小语种、是否希望长期留下等")
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
                st.success("画像已保存")
            st.markdown("</div>", unsafe_allow_html=True)

        with right:
            st.markdown('<div class="block-card">', unsafe_allow_html=True)
            st.markdown("### 推荐国家")
            ranked = recommend_countries(get_profile(current_user) or profile)
            for name, score in ranked:
                st.write(f"**{name}**  · 评分 {score}")
            st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
            st.markdown("### 使用提示")
            st.write("画像越完整，Agent 的规划越贴近真实需求。")
            st.write("尤其建议填写：专业、预算、目标、目标国家、语言能力。")
            st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 页面：联网搜索
# =========================
elif page == "联网搜索":
    st.markdown('<div class="section-title">联网搜索</div>', unsafe_allow_html=True)

    if not current_user:
        st.warning("请先载入用户。")
    else:
        st.markdown('<div class="block-card">', unsafe_allow_html=True)
        query = st.text_input("输入搜索问题", placeholder="例如：德国计算机硕士申请官网 / 比利时学生租房指南 / Canada international student health insurance")
        c1, c2 = st.columns([1, 3])
        with c1:
            do_search = st.button("开始搜索")
        with c2:
            st.caption("建议直接搜官网、签证、住宿、保险、就业、导师主页等。")

        if do_search:
            if not query.strip():
                st.warning("请输入搜索内容。")
            else:
                with st.spinner("正在联网搜索..."):
                    results = search_web(query, max_results=8)
                    save_search(current_user, query, results)

                st.success(f"已获取 {len(results)} 条结果")
                for i, item in enumerate(results, 1):
                    with st.container():
                        st.markdown(f"**{i}. {item['title']}**")
                        if item.get("url"):
                            st.write(item["url"])
                        if item.get("content"):
                            st.caption(item["content"])
                        st.markdown("---")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 页面：AI规划
# =========================
elif page == "AI规划":
    st.markdown('<div class="section-title">AI Agent 规划</div>', unsafe_allow_html=True)

    if not current_user:
        st.warning("请先载入用户。")
    else:
        profile = get_profile(current_user)
        if not profile:
            st.warning("请先填写个人画像。")
        else:
            left, right = st.columns([1.2, 1])

            with left:
                st.markdown('<div class="block-card">', unsafe_allow_html=True)
                agent_goal = st.text_area(
                    "告诉系统你要什么",
                    value="请基于我的背景，联网搜索并给我一份从申请、签证、租房、求医、购物到就业和长期身份的全面周到规划。",
                    height=120
                )
                run = st.button("运行智能 Agent")
                st.markdown("</div>", unsafe_allow_html=True)

                if run:
                    with st.spinner("Agent 正在工作..."):
                        plan, logs, web_results, tasks = run_agent(current_user, profile, agent_goal)

                    st.markdown('<div class="block-card">', unsafe_allow_html=True)
                    st.markdown("### 规划结果")
                    st.markdown(plan)
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown('<div class="block-card">', unsafe_allow_html=True)
                    st.markdown("### 本次生成的任务")
                    for t in tasks:
                        st.write(f"- {t['title']} ｜ {t['due_date']} ｜ {t['status']}")
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown('<div class="block-card">', unsafe_allow_html=True)
                    st.markdown("### Agent 日志")
                    for line in logs:
                        st.code(line)
                    st.markdown("</div>", unsafe_allow_html=True)

            with right:
                st.markdown('<div class="block-card">', unsafe_allow_html=True)
                st.markdown("### 当前画像摘要")
                st.write(f"用户：{profile.get('username', '')}")
                st.write(f"阶段：{profile.get('education', '')}")
                st.write(f"专业：{profile.get('major', '')}")
                st.write(f"预算：{profile.get('budget', '')}")
                st.write(f"目标：{profile.get('goal', '')}")
                st.write(f"国家：{profile.get('countries', '')}")
                st.write(f"语言：{profile.get('languages', '')}")
                st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 页面：邮件中心
# =========================
elif page == "邮件中心":
    st.markdown('<div class="section-title">邮件中心</div>', unsafe_allow_html=True)

    if not current_user:
        st.warning("请先载入用户。")
    else:
        profile = get_profile(current_user)
        if not profile:
            st.warning("请先填写个人画像。")
        else:
            left, right = st.columns([1.1, 1.2])

            with left:
                st.markdown('<div class="block-card">', unsafe_allow_html=True)
                recipient_name = st.text_input("收件人姓名", placeholder="Professor Smith / Admissions Office")
                recipient_email = st.text_input("收件人邮箱", placeholder="example@university.edu")
                purpose = st.text_input("邮件目的", placeholder="申请咨询 / 套磁 / 奖学金咨询 / follow-up")
                if st.button("生成邮件草稿"):
                    if not recipient_email or not purpose:
                        st.warning("请填写收件人邮箱和邮件目的。")
                    else:
                        subject, body = build_email_draft(profile, recipient_name, recipient_email, purpose)
                        st.session_state["draft_subject"] = subject
                        st.session_state["draft_body"] = body
                        st.success("草稿已生成")
                st.markdown("</div>", unsafe_allow_html=True)

            with right:
                st.markdown('<div class="block-card">', unsafe_allow_html=True)
                draft_subject = st.text_input("主题", value=st.session_state.get("draft_subject", ""))
                draft_body = st.text_area("正文", value=st.session_state.get("draft_body", ""), height=280)

                c1, c2 = st.columns(2)
                with c1:
                    if st.button("保存草稿"):
                        save_email(current_user, recipient_email, draft_subject, draft_body, "draft")
                        st.success("草稿已保存")
                with c2:
                    if st.button("发送邮件"):
                        ok, msg = send_email(recipient_email, draft_subject, draft_body)
                        save_email(current_user, recipient_email, draft_subject, draft_body, "sent" if ok else "failed")
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)
                st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 页面：任务中心
# =========================
elif page == "任务中心":
    st.markdown('<div class="section-title">任务中心</div>', unsafe_allow_html=True)

    if not current_user:
        st.warning("请先载入用户。")
    else:
        rows = get_user_tasks(current_user)

        st.markdown('<div class="block-card">', unsafe_allow_html=True)
        if not rows:
            st.info("暂无任务。先去运行 AI Agent。")
        else:
            for row in rows:
                st.write(f"**#{row[0]}**｜{row[1]}")
                st.caption(f"截止：{row[2]} ｜ 状态：{row[3]} ｜ 来源：{row[4]} ｜ 创建于：{row[5]}")
                st.markdown("---")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 页面：历史中心
# =========================
elif page == "历史中心":
    st.markdown('<div class="section-title">历史中心</div>', unsafe_allow_html=True)

    if not current_user:
        st.warning("请先载入用户。")
    else:
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown('<div class="block-card">', unsafe_allow_html=True)
            st.markdown("### 历史规划")
            plans = get_user_plans(current_user)
            if not plans:
                st.caption("暂无")
            for p in plans[:10]:
                with st.expander(f"{p[1]}｜{p[3]}"):
                    st.markdown(p[2])
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="block-card">', unsafe_allow_html=True)
            st.markdown("### 邮件记录")
            emails = get_user_emails(current_user)
            if not emails:
                st.caption("暂无")
            for e in emails[:10]:
                with st.expander(f"{e[2]}｜{e[5]}｜{e[4]}"):
                    st.write(f"收件人：{e[1]}")
                    st.text(e[3])
            st.markdown("</div>", unsafe_allow_html=True)

        with c3:
            st.markdown('<div class="block-card">', unsafe_allow_html=True)
            st.markdown("### 搜索记录")
            searches = get_user_searches(current_user)
            if not searches:
                st.caption("暂无")
            for s in searches[:10]:
                with st.expander(f"{s[1]}｜{s[3]}"):
                    try:
                        items = json.loads(s[2])
                        for item in items[:5]:
                            st.write(f"- {item.get('title', '')}")
                            if item.get("url"):
                                st.caption(item["url"])
                    except Exception:
                        st.write(s[2])
            st.markdown("</div>", unsafe_allow_html=True)
