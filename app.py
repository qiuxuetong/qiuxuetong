from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json

app = FastAPI()

# 允许浏览器访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 📦 数据库初始化
# =========================
conn = sqlite3.connect("study.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    country TEXT,
    content TEXT
)
""")

conn.commit()

# =========================
# 🧠 推荐算法
# =========================
def recommend_country(education, budget, goal):
    scores = {"Canada":0, "Germany":0, "Netherlands":0, "USA":0}

    if goal == "immigration":
        scores["Canada"] += 3
        scores["Germany"] += 2

    if budget == "low":
        scores["Germany"] += 3
    else:
        scores["USA"] += 2

    if education == "bachelor":
        scores["Canada"] += 2

    return max(scores, key=scores.get)

# =========================
# 📅 48个月规划
# =========================
def generate_plan(country):
    return [
        "0-6月：申请学校 + 套磁",
        "6-12月：签证 + 入学",
        "12-24月：实习 + 本地经验",
        "24-36月：找工作",
        "36-48月：申请永居"
    ]

# =========================
# 🌐 前端页面
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Study OS</title>
    </head>
    <body style="font-family:Arial; padding:40px;">
        <h1>🌍 全球留学系统</h1>

        <h2>注册</h2>
        <form action="/register" method="post">
            用户名: <input name="username"><br>
            密码: <input name="password" type="password"><br>
            <button type="submit">注册</button>
        </form>

        <h2>登录</h2>
        <form action="/login" method="post">
            用户名: <input name="username"><br>
            密码: <input name="password" type="password"><br>
            <button type="submit">登录</button>
        </form>

        <h2>生成留学路径</h2>
        <form action="/generate" method="post">
            用户ID: <input name="user_id"><br>

            学历:
            <select name="education">
                <option value="bachelor">本科</option>
                <option value="master">硕士</option>
            </select><br>

            预算:
            <select name="budget">
                <option value="low">低</option>
                <option value="high">高</option>
            </select><br>

            目标:
            <select name="goal">
                <option value="immigration">移民</option>
                <option value="career">就业</option>
            </select><br>

            <button type="submit">生成方案</button>
        </form>

        <h2>查看我的规划</h2>
        <form action="/plans" method="post">
            用户ID: <input name="user_id"><br>
            <button type="submit">查看</button>
        </form>

    </body>
    </html>
    """

# =========================
# 👤 注册
# =========================
@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return f"注册成功！"
    except:
        return "用户已存在"

# =========================
# 🔐 登录
# =========================
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    if user:
        return f"登录成功！你的用户ID是：{user[0]}"
    else:
        return "登录失败"

# =========================
# 🎯 生成计划
# =========================
@app.post("/generate")
def generate(
    user_id: int = Form(...),
    education: str = Form(...),
    budget: str = Form(...),
    goal: str = Form(...)
):
    country = recommend_country(education, budget, goal)
    plan = generate_plan(country)

    cursor.execute(
        "INSERT INTO plans (user_id, country, content) VALUES (?, ?, ?)",
        (user_id, country, json.dumps(plan))
    )
    conn.commit()

    return f"推荐国家：{country}<br>规划：<br>" + "<br>".join(plan)

# =========================
# 📊 查看规划
# =========================
@app.post("/plans")
def get_plans(user_id: int = Form(...)):
    cursor.execute("SELECT country, content FROM plans WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()

    result = "<h2>你的规划</h2>"

    for r in rows:
        plan = json.loads(r[1])
        result += f"<h3>{r[0]}</h3>"
        result += "<br>".join(plan)
        result += "<hr>"

    return result
