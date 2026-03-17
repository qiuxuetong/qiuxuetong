import os
import json
import sqlite3
import smtplib
from datetime import datetime, timedelta
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
    page_title="全球留学智能平台",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "page" not in st.session_state:
    st.session_state["page"] = "首页"
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

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

DB_PATH = "study_product.db"

# =========================
# 样式
# =========================
st.markdown("""
<style>
:root {
    --bg: #f5f7fb;
    --card: #ffffff;
    --line: #e7ecf5;
    --text: #1b2559;
    --muted: #6b7280;
    --brand: #315efb;
    --brand2: #5b7cff;
    --ok: #16a34a;
    --warn: #d97706;
    --danger: #dc2626;
}

html, body, [class*="css"] {
    font-family: Inter, "PingFang SC", "Microsoft YaHei", sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #f8fbff 0%, #f5f7fb 100%);
}

.hero {
    background: linear-gradient(135deg, #315efb 0%, #5b7cff 100%);
    color: white;
    padding: 30px;
    border-radius: 26px;
    box-shadow: 0 20px 45px rgba(49,94,251,0.20);
    margin-bottom: 20px;
}

.hero h1 {
    margin: 0 0 10px 0;
    font-size: 40px;
    font-weight: 800;
}

.hero p {
    margin: 0;
    opacity: 0.96;
    font-size: 16px;
    line-height: 1.7;
}

.section-title {
    font-size: 26px;
    font-weight: 800;
    color: var(--text);
    margin: 6px 0 14px 0;
}

.block-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 10px 26px rgba(0,0,0,0.04);
    margin-bottom: 16px;
}

.home-card {
    background: white;
    border: 1px solid var(--line);
    border-radius: 22px;
    padding: 20px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.04);
    min-height: 170px;
}

.home-card h3 {
    margin: 0 0 10px 0;
    color: var(--text);
    font-size: 22px;
}

.home-card p {
    margin: 0;
    color: var(--muted);
    line-height: 1.7;
    font-size: 14px;
}

.kpi-wrap {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    margin-bottom: 18px;
}

.kpi {
    background: white;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.04);
}

.kpi .num {
    font-size: 30px;
    font-weight: 800;
    color: var(--brand);
}

.kpi .label {
    margin-top: 6px;
    font-size: 13px;
    color: var(--muted);
}

.timeline-box {
    border-left: 4px solid #c8d4ff;
    padding-left: 16px;
    margin-left: 4px;
}

.timeline-item {
    background: white;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 12px;
}

.timeline-item .time {
    color: var(--brand);
    font-weight: 700;
    margin-bottom: 6px;
}

.task-col {
    background: #f9fbff;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 14px;
    min-height: 320px;
}

.task-badge {
    display: inline-block;
    background: #edf2ff;
    color: #315efb;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 10px;
}

.task-card {
    background: white;
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 10px;
}

.small {
    color: var(--muted);
    font-size: 12px;
}

.chat-box {
    background: white;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 16px;
    max-height: 540px;
    overflow-y: auto;
}

.user-msg {
    background: #edf2ff;
    color: #1f3b73;
    padding: 12px 14px;
    border-radius: 14px 14px 4px 14px;
    margin: 10px 0;
}

.ai-msg {
    background: #f7f8fb;
    color: #223;
    padding: 12px 14px;
    border-radius: 14px 14px 14px 4px;
    margin: 10px 0;
}

.template-card {
    background: white;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 10px;
}

div.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    min-height: 42px !important;
}

@media (max-width: 900px) {
    .kpi-wrap {
        grid-template-columns: 1fr 1fr;
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
# 内置数据库
# =========================
SCHOOL_DB = [
    {
        "country": "德国",
        "name": "Technical University of Munich",
        "city": "Munich",
        "level": "顶尖",
        "tags": ["计算机", "工程", "英语项目", "研究强"],
        "tuition": "低/公立",
        "language": "英语/德语"
    },
    {
        "country": "荷兰",
        "name": "Delft University of Technology",
        "city": "Delft",
        "level": "顶尖",
        "tags": ["工程", "建筑", "计算机", "国际化"],
        "tuition": "中高",
        "language": "英语"
    },
    {
        "country": "加拿大",
        "name": "University of Toronto",
        "city": "Toronto",
        "level": "顶尖",
        "tags": ["综合", "医学", "计算机", "就业强"],
        "tuition": "高",
        "language": "英语"
    },
    {
        "country": "比利时",
        "name": "KU Leuven",
        "city": "Leuven",
        "level": "顶尖",
        "tags": ["综合", "工程", "生物", "欧洲机会"],
        "tuition": "中",
        "language": "英语/荷兰语"
    },
    {
        "country": "英国",
        "name": "University of Edinburgh",
        "city": "Edinburgh",
        "level": "强校",
        "tags": ["AI", "语言", "数据", "国际学生多"],
        "tuition": "高",
        "language": "英语"
    }
]

VISA_DB = [
    {"country": "德国", "type": "学生签证", "core": "录取信、资金证明、保险、住宿", "note": "落地后换居留"},
    {"country": "荷兰", "type": "学生居留", "core": "学校担保、资金、保险、护照", "note": "通常由学校协助"},
    {"country": "加拿大", "type": "Study Permit", "core": "录取信、资金、体检、护照", "note": "可衔接毕业工签"},
    {"country": "比利时", "type": "长居学生签", "core": "录取信、资金、保险、无犯罪", "note": "市政厅注册很关键"},
    {"country": "英国", "type": "Student Visa", "core": "CAS、资金、语言、护照", "note": "毕业可衔接 Graduate Route"}
]

MENTOR_DB = [
    {"name": "Prof. Anna Müller", "school": "Technical University of Munich", "field": "AI / Robotics", "email_hint": "lab website"},
    {"name": "Dr. James Carter", "school": "University of Toronto", "field": "Data Science", "email_hint": "department page"},
    {"name": "Prof. Sophie Vermeer", "school": "Delft University of Technology", "field": "Computer Vision", "email_hint": "faculty profile"},
    {"name": "Prof. Luca Janssens", "school": "KU Leuven", "field": "Bioengineering", "email_hint": "research unit page"}
]

EMAIL_TEMPLATES = [
    {
        "name": "导师套磁",
        "subject": "Prospective Student Inquiry",
        "body": "Dear Professor,\n\nI hope this email finds you well. My name is ... I am very interested in your research on ...\n\nBest regards,"
    },
    {
        "name": "项目申请咨询",
        "subject": "Inquiry About Program Application",
        "body": "Dear Admissions Office,\n\nI am writing to inquire about the application requirements and timeline for your program...\n\nBest regards,"
    },
    {
        "name": "奖学金咨询",
        "subject": "Inquiry About Scholarship Opportunities",
        "body": "Dear Sir/Madam,\n\nI would like to ask whether there are scholarship opportunities for international students in ...\n\nBest regards,"
    },
    {
        "name": "邮件跟进",
        "subject": "Follow-up on Previous Email",
        "body": "Dear Sir/Madam,\n\nI am writing to kindly follow up on my previous email regarding ...\n\nBest regards,"
    }
]

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
            profile["email"], profile["education"], profile["major"], profile["budget"],
            profile["goal"], profile["countries"], profile["languages"], profile["notes"],
            now_str(), profile["username"]
        ))
    else:
        cursor.execute("""
            INSERT INTO profiles (
                username, email, education, major, budget, goal, countries, languages, notes, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profile["username"], profile["email"], profile["education"], profile["major"],
            profile["budget"], profile["goal"], profile["countries"], profile["languages"],
            profile["notes"], now_str()
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
            t.get("status", "待办"),
            source,
            now_str()
        ))
    conn.commit()

def update_task_status(task_id: int, status: str):
    cursor.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    conn.commit()

def get_user_plans(username: str):
    cursor.execute("SELECT id, title, content, created_at FROM plans WHERE username=? ORDER BY id DESC", (username,))
    return cursor.fetchall()

def get_user_emails(username: str):
    cursor.execute("SELECT id, recipient, subject, body, status, created_at FROM emails WHERE username=? ORDER BY id DESC", (username,))
    return cursor.fetchall()

def get_user_tasks(username: str):
    cursor.execute("SELECT id, title, due_date, status, source, created_at FROM tasks WHERE username=? ORDER BY id DESC", (username,))
    return cursor.fetchall()

def get_user_searches(username: str):
    cursor.execute("SELECT id, query, results_json, created_at FROM searches WHERE username=? ORDER BY id DESC", (username,))
    return cursor.fetchall()

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
# 搜索
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
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
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
    if items:
        return items
    return search_web_duckduckgo(query, max_results=max_results)

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
# 业务逻辑
# =========================
def recommend_countries(profile: dict):
    scores = {
        "加拿大": 0, "德国": 0, "荷兰": 0, "比利时": 0, "澳大利亚": 0, "英国": 0, "美国": 0
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
    if budget == "低":
        scores["德国"] += 4
        scores["比利时"] += 2
    elif budget == "中":
        scores["荷兰"] += 1
        scores["加拿大"] += 1
    else:
        scores["英国"] += 1
        scores["美国"] += 1
        scores["澳大利亚"] += 1
    if education == "本科":
        scores["加拿大"] += 2
        scores["荷兰"] += 1
    elif education == "硕士":
        scores["德国"] += 1
        scores["荷兰"] += 1
    elif education == "博士":
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

def build_timeline(country: str):
    return [
        {"time": "0-3个月", "task": f"确定 {country} 为主申方向，整理学历材料、语言计划和预算。"},
        {"time": "3-6个月", "task": "完成学校筛选、导师检索、官网信息收集和申请清单。"},
        {"time": "6-12个月", "task": "提交申请，跟进邮件，准备签证和住宿。"},
        {"time": "12-18个月", "task": "落地后完成注册、居留、医保、银行卡、电话卡和基础生活配置。"},
        {"time": "18-36个月", "task": "尽快做实习、科研、项目和本地人脉积累。"},
        {"time": "36-48个月", "task": "冲刺毕业就业、工签/蓝卡/长期身份路径。"},
    ]

def build_kanban_tasks():
    return [
        {"title": "整理成绩单、护照、简历", "due_date": "本周", "status": "待办"},
        {"title": "建立学校/导师/签证表", "due_date": "3天内", "status": "进行中"},
        {"title": "完成第一封联系邮件", "due_date": "7天内", "status": "待办"},
        {"title": "检查住宿和保险方案", "due_date": "本周", "status": "待办"},
        {"title": "开始找实习/项目机会", "due_date": "本月", "status": "已完成"},
    ]

def fallback_plan(profile: dict, web_results: list):
    ranked = recommend_countries(profile)
    country = ranked[0][0] if ranked else "待分析"
    refs = "\n".join([f"- {x['title']} {x['url']}" for x in web_results[:5]]) if web_results else "暂无联网结果"
    return f"""
# 留学全流程方案

## 推荐国家
首选：{country}

## 申请阶段
- 先锁定主申国家与保底国家
- 建立学校和导师清单
- 同步准备成绩单、简历、语言成绩、推荐信、文书

## 签证与身份
- 优先查看官方签证说明
- 准备资金、保险、住宿和预约材料
- 记录关键时间节点

## 落地生活
- 提前准备租房、医保、电话卡、交通、银行卡
- 熟悉看病流程、药店、超市和治安信息

## 就业与长期发展
- 入学即开始规划实习
- 毕业前 6-12 个月系统投递
- 提前评估毕业工签、蓝卡、长期居留

## 联网参考
{refs}
""".strip()

def run_agent(username: str, profile: dict, user_goal: str):
    logs = []
    queries = [
        f"{profile.get('major', '')} {profile.get('countries', '')} university programs",
        f"{profile.get('countries', '')} student visa official site",
        f"{profile.get('countries', '')} student accommodation guide",
        f"{profile.get('countries', '')} international student health insurance",
        f"{profile.get('countries', '')} jobs for {profile.get('major', '')}"
    ]
    web_results = []
    for q in queries:
        items = search_web(q, max_results=3)
        web_results.extend(items)
        logs.append(f"搜索: {q} -> {len(items)} 条")

    save_search(username, " | ".join(queries), web_results)

    system_prompt = """
你是全球留学、签证、落地生活、就业与长期身份规划顾问。
请根据用户背景和联网结果，生成周到全面的中文规划。
必须覆盖：
1. 国家与学校策略
2. 导师与官网信息获取方式
3. 签证与身份
4. 租房、求医、保险、购物、交通
5. 就业和长期发展
6. 本周任务
7. 风险提醒
""".strip()

    user_prompt = f"""
用户画像：
{json.dumps(profile, ensure_ascii=False)}

用户需求：
{user_goal}

联网信息：
{json.dumps(web_results[:10], ensure_ascii=False)}
""".strip()

    plan = ai_chat(system_prompt, user_prompt)
    if not plan or str(plan).startswith("[AI调用失败]"):
        plan = fallback_plan(profile, web_results)
        logs.append("AI 不可用，改用本地规划")

    save_plan(username, f"正式规划 - {datetime.now().strftime('%Y-%m-%d %H:%M')}", plan)

    tasks = build_kanban_tasks()
    save_tasks(username, tasks, source="agent")

    return plan, logs, web_results, tasks

def build_email_draft(profile: dict, recipient_name: str, recipient_email: str, purpose: str):
    subject = f"{profile.get('education', '')}申请咨询 - {profile.get('major', '')} - {purpose}"
    base = f"""Dear {recipient_name or "Sir/Madam"},

I hope this email finds you well.

My name is {profile.get("username", "")}. I am currently preparing for my overseas study and career plan in {profile.get("major", "")}. My current stage is {profile.get("education", "")}, and my goal is {profile.get("goal", "")}.

I am writing to ask about {purpose}. I would be grateful if you could share any relevant information regarding requirements, timeline, funding, or recommended preparation steps.

Thank you very much for your time and consideration.

Best regards,
{profile.get("username", "")}
Email: {profile.get("email", "")}
""".strip()

    improved = ai_chat(
        "You are an expert education email writer. Improve the draft and keep it concise and professional.",
        f"Profile:{json.dumps(profile, ensure_ascii=False)}\nRecipient:{recipient_name} <{recipient_email}>\nPurpose:{purpose}\nDraft:\n{base}"
    )
    body = improved if improved and not str(improved).startswith("[AI调用失败]") else base
    return subject, body

def build_followup_email(original_subject: str):
    return f"Follow-up: {original_subject}", """Dear Sir/Madam,

I hope you are well.

I am writing to kindly follow up on my previous email. I would appreciate any update when convenient.

Best regards,
"""

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
# 顶部
# =========================
st.markdown("""
<div class="hero">
    <h1>🌍 全球留学智能平台</h1>
    <p>更像正式产品首页的版本：学校库、签证库、导师库、任务看板、时间线规划、AI 顾问、邮件模板和 follow-up 自动化，全部整合在一个页面系统里。</p>
</div>
""", unsafe_allow_html=True)

# =========================
# 侧边栏
# =========================
with st.sidebar:
    st.markdown("## 平台控制台")
    username_input = st.text_input("用户名", value=st.session_state.get("username", ""))
    if st.button("载入用户"):
        if username_input.strip():
            st.session_state["username"] = username_input.strip()
            st.success(f"当前用户：{username_input.strip()}")
        else:
            st.warning("请输入用户名")

    current_user = st.session_state.get("username", "")

    st.markdown("---")
    st.write(f"当前用户：{current_user or '未设置'}")
    st.write(f"AI：{'已配置' if AI_API_KEY and AI_BASE_URL and AI_MODEL else '未配置'}")
    st.write(f"搜索：{'Tavily' if TAVILY_API_KEY else 'DuckDuckGo 简易模式'}")
    st.write(f"邮件：{'已配置 SMTP' if SMTP_HOST and SMTP_USER and SMTP_PASS else '未配置'}")

    st.markdown("---")
    page_options = ["首页", "个人画像", "学校库", "签证库", "导师库", "任务看板", "时间线规划", "AI顾问", "邮件中心", "历史中心"]
    sidebar_page = st.radio("页面导航", page_options, index=page_options.index(st.session_state["page"]))
    st.session_state["page"] = sidebar_page
    page = st.session_state["page"]

# =========================
# 首页
# =========================
if page == "首页":
    p_count, t_count, e_count, s_count = get_counts(current_user)

    st.markdown(f"""
    <div class="kpi-wrap">
        <div class="kpi"><div class="num">{p_count}</div><div class="label">规划总数</div></div>
        <div class="kpi"><div class="num">{t_count}</div><div class="label">任务总数</div></div>
        <div class="kpi"><div class="num">{e_count}</div><div class="label">邮件记录</div></div>
        <div class="kpi"><div class="num">{s_count}</div><div class="label">搜索记录</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">产品入口</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    with c1:
        st.markdown('<div class="home-card"><h3>👤 用户画像</h3><p>填写学历、专业、预算、目标和语言能力，形成后续推荐与 Agent 规划的基础。</p></div>', unsafe_allow_html=True)
        if st.button("进入 用户画像", use_container_width=True):
            st.session_state["page"] = "个人画像"
            st.rerun()

    with c2:
        st.markdown('<div class="home-card"><h3>🏫 学校库</h3><p>按国家、城市、学科和学费查看适合的学校，快速建立申请池。</p></div>', unsafe_allow_html=True)
        if st.button("进入 学校库", use_container_width=True):
            st.session_state["page"] = "学校库"
            st.rerun()

    with c3:
        st.markdown('<div class="home-card"><h3>🛂 签证库</h3><p>查看不同国家的学生签、材料重点和落地后身份流程。</p></div>', unsafe_allow_html=True)
        if st.button("进入 签证库", use_container_width=True):
            st.session_state["page"] = "签证库"
            st.rerun()

    with c4:
        st.markdown('<div class="home-card"><h3>🎓 导师库</h3><p>整理导师方向和入口提示，方便你继续去官网和院系页面核实。</p></div>', unsafe_allow_html=True)
        if st.button("进入 导师库", use_container_width=True):
            st.session_state["page"] = "导师库"
            st.rerun()

    with c5:
        st.markdown('<div class="home-card"><h3>📋 任务看板</h3><p>把申请、签证、邮件、住宿和就业拆成可执行任务，不再只是看建议。</p></div>', unsafe_allow_html=True)
        if st.button("进入 任务看板", use_container_width=True):
            st.session_state["page"] = "任务看板"
            st.rerun()

    with c6:
        st.markdown('<div class="home-card"><h3>🤖 AI 顾问</h3><p>结合联网搜索和你的背景，生成更完整的规划与下一步行动建议。</p></div>', unsafe_allow_html=True)
        if st.button("进入 AI顾问", use_container_width=True):
            st.session_state["page"] = "AI顾问"
            st.rerun()

    left, right = st.columns([1.2, 1])
    with left:
        st.markdown('<div class="block-card">', unsafe_allow_html=True)
        st.markdown("### 推荐使用顺序")
        st.write("1. 先填写用户画像")
        st.write("2. 再看学校库、签证库、导师库")
        st.write("3. 然后运行 AI 顾问生成正式规划")
        st.write("4. 在邮件中心生成咨询、套磁和 follow-up")
        st.write("5. 最后到任务看板持续推进")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="block-card">', unsafe_allow_html=True)
        st.markdown("### 当前建议")
        if not current_user:
            st.warning("先在左侧输入用户名并载入。")
        else:
            profile = get_profile(current_user)
            if not profile:
                st.info("下一步：填写用户画像。")
            else:
                st.success("下一步：去 AI 顾问生成正式规划。")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 个人画像
# =========================
elif page == "个人画像":
    st.markdown('<div class="section-title">个人画像</div>', unsafe_allow_html=True)

    if not current_user:
        st.warning("请先载入用户。")
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
            "notes": ""
        }

        left, right = st.columns([1.2, 1])

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
                notes = st.text_area("补充说明", value=profile["notes"], height=150)
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
                st.write(f"**{name}** · 评分 {score}")
            st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 学校库
# =========================
elif page == "学校库":
    st.markdown('<div class="section-title">学校库</div>', unsafe_allow_html=True)

    country_filter = st.selectbox("按国家筛选", ["全部"] + sorted(list({x["country"] for x in SCHOOL_DB})))
    keyword = st.text_input("关键词", placeholder="计算机 / AI / 低学费 / 英语项目")

    for s in SCHOOL_DB:
        if country_filter != "全部" and s["country"] != country_filter:
            continue
        if keyword.strip():
            text = f"{s['name']} {s['city']} {s['level']} {' '.join(s['tags'])} {s['tuition']} {s['language']}"
            if keyword.lower() not in text.lower():
                continue

        st.markdown('<div class="block-card">', unsafe_allow_html=True)
        st.markdown(f"### {s['name']}")
        st.write(f"国家：{s['country']} ｜ 城市：{s['city']} ｜ 层级：{s['level']}")
        st.write(f"方向：{', '.join(s['tags'])}")
        st.write(f"学费：{s['tuition']} ｜ 语言：{s['language']}")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 签证库
# =========================
elif page == "签证库":
    st.markdown('<div class="section-title">签证库</div>', unsafe_allow_html=True)

    country_filter = st.selectbox("选择国家", sorted(list({x["country"] for x in VISA_DB})))
    for v in VISA_DB:
        if v["country"] != country_filter:
            continue
        st.markdown('<div class="block-card">', unsafe_allow_html=True)
        st.markdown(f"### {v['country']} - {v['type']}")
        st.write(f"核心材料：{v['core']}")
        st.write(f"说明：{v['note']}")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 导师库
# =========================
elif page == "导师库":
    st.markdown('<div class="section-title">导师库</div>', unsafe_allow_html=True)

    keyword = st.text_input("按方向或学校搜索导师", placeholder="AI / Data / KU Leuven")
    for m in MENTOR_DB:
        text = f"{m['name']} {m['school']} {m['field']}"
        if keyword.strip() and keyword.lower() not in text.lower():
            continue
        st.markdown('<div class="block-card">', unsafe_allow_html=True)
        st.markdown(f"### {m['name']}")
        st.write(f"学校：{m['school']}")
        st.write(f"方向：{m['field']}")
        st.write(f"邮箱线索：{m['email_hint']}")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 任务看板
# =========================
elif page == "任务看板":
    st.markdown('<div class="section-title">任务看板</div>', unsafe_allow_html=True)

    if not current_user:
        st.warning("请先载入用户。")
    else:
        rows = get_user_tasks(current_user)
        if not rows:
            st.info("暂无任务。先去 AI 顾问生成任务。")
        else:
            todo = [r for r in rows if r[3] == "待办"]
            doing = [r for r in rows if r[3] == "进行中"]
            done = [r for r in rows if r[3] == "已完成"]

            c1, c2, c3 = st.columns(3)
            for col, title, items in [(c1, "待办", todo), (c2, "进行中", doing), (c3, "已完成", done)]:
                with col:
                    st.markdown('<div class="task-col">', unsafe_allow_html=True)
                    st.markdown(f'<div class="task-badge">{title}</div>', unsafe_allow_html=True)
                    if not items:
                        st.caption("暂无")
                    for r in items:
                        st.markdown(f"""
                        <div class="task-card">
                            <strong>{r[1]}</strong><br>
                            <span class="small">截止：{r[2]} ｜ 来源：{r[4]}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        new_status = st.selectbox(
                            f"更新状态 #{r[0]}",
                            ["待办", "进行中", "已完成"],
                            index=["待办", "进行中", "已完成"].index(r[3]),
                            key=f"task_status_{r[0]}"
                        )
                        if new_status != r[3]:
                            update_task_status(r[0], new_status)
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 时间线规划
# =========================
elif page == "时间线规划":
    st.markdown('<div class="section-title">时间线规划</div>', unsafe_allow_html=True)

    if not current_user:
        st.warning("请先载入用户。")
    else:
        profile = get_profile(current_user)
        country = "加拿大"
        if profile:
            ranked = recommend_countries(profile)
            if ranked:
                country = ranked[0][0]

        timeline = build_timeline(country)
        st.markdown('<div class="timeline-box">', unsafe_allow_html=True)
        for item in timeline:
            st.markdown(f"""
            <div class="timeline-item">
                <div class="time">{item['time']}</div>
                <div>{item['task']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# AI顾问
# =========================
elif page == "AI顾问":
    st.markdown('<div class="section-title">AI 顾问</div>', unsafe_allow_html=True)

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
                st.markdown("### 正式规划生成")
                agent_goal = st.text_area(
                    "你的需求",
                    value="请基于我的背景，联网整合学校、签证、导师、租房、求医、购物、就业和长期身份信息，给我一份周到全面的正式规划。",
                    height=110
                )
                if st.button("运行 AI 顾问"):
                    with st.spinner("AI 顾问正在工作..."):
                        plan, logs, web_results, tasks = run_agent(current_user, profile, agent_goal)
                    st.session_state["latest_plan"] = plan
                    st.session_state["latest_logs"] = logs
                    st.session_state["latest_results"] = web_results
                    st.session_state["latest_tasks"] = tasks
                    st.success("已生成正式规划")
                st.markdown("</div>", unsafe_allow_html=True)

                if st.session_state.get("latest_plan"):
                    st.markdown('<div class="block-card">', unsafe_allow_html=True)
                    st.markdown("### 正式规划")
                    st.markdown(st.session_state["latest_plan"])
                    st.markdown("</div>", unsafe_allow_html=True)

            with right:
                st.markdown('<div class="block-card">', unsafe_allow_html=True)
                st.markdown("### AI 对话区")
                st.markdown('<div class="chat-box">', unsafe_allow_html=True)
                for role, content in st.session_state["chat_history"]:
                    if role == "user":
                        st.markdown(f'<div class="user-msg">{content}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="ai-msg">{content}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                user_q = st.text_area("继续追问 AI 顾问", height=100, placeholder="例如：我预算低，德语弱，想尽快留下来，该怎么选？")
                if st.button("发送问题"):
                    if user_q.strip():
                        st.session_state["chat_history"].append(("user", user_q.strip()))
                        answer = ai_chat(
                            "你是全球留学和长期发展顾问，请用中文提供具体可执行建议。",
                            f"用户画像：{json.dumps(profile, ensure_ascii=False)}\n问题：{user_q.strip()}"
                        )
                        if not answer:
                            answer = "当前 AI 未配置，无法回答。"
                        st.session_state["chat_history"].append(("ai", answer))
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 邮件中心
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
            left, right = st.columns([1, 1.2])

            with left:
                st.markdown('<div class="block-card">', unsafe_allow_html=True)
                st.markdown("### 模板库")
                template_names = [x["name"] for x in EMAIL_TEMPLATES]
                chosen = st.selectbox("选择模板", template_names)
                tpl = next(x for x in EMAIL_TEMPLATES if x["name"] == chosen)
                st.write(f"主题模板：{tpl['subject']}")
                st.text(tpl["body"])

                recipient_name = st.text_input("收件人姓名")
                recipient_email = st.text_input("收件人邮箱")
                purpose = st.text_input("邮件目的", value=chosen)

                if st.button("生成邮件草稿"):
                    subject, body = build_email_draft(profile, recipient_name, recipient_email, purpose)
                    st.session_state["draft_subject"] = subject
                    st.session_state["draft_body"] = body
                    st.success("已生成草稿")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown('<div class="block-card">', unsafe_allow_html=True)
                st.markdown("### Follow-up 自动化")
                original_subject = st.text_input("原邮件主题", placeholder="Inquiry About Program Application")
                if st.button("生成 Follow-up"):
                    sub, body = build_followup_email(original_subject or "Previous Email")
                    st.session_state["draft_subject"] = sub
                    st.session_state["draft_body"] = body
                    st.success("已生成 follow-up 草稿")
                st.markdown("</div>", unsafe_allow_html=True)

            with right:
                st.markdown('<div class="block-card">', unsafe_allow_html=True)
                st.markdown("### 编辑与发送")
                subject = st.text_input("主题", value=st.session_state.get("draft_subject", ""))
                body = st.text_area("正文", value=st.session_state.get("draft_body", ""), height=320)

                c1, c2 = st.columns(2)
                with c1:
                    if st.button("保存草稿"):
                        save_email(current_user, recipient_email, subject, body, "draft")
                        st.success("草稿已保存")
                with c2:
                    if st.button("发送邮件"):
                        ok, msg = send_email(recipient_email, subject, body)
                        save_email(current_user, recipient_email, subject, body, "sent" if ok else "failed")
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)
                st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 历史中心
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
