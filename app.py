from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import sqlite3
import json

app = FastAPI()

# =========================
# 📦 数据库
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
# 📅 规划
# =========================
def generate_plan(country):
    return [
        "📘 0-6月：申请学校 + 套磁",
        "🛂 6-12月：签证 + 入学",
        "💼 12-24月：实习 + 本地经验",
        "🚀 24-36月：找工作",
        "🏡 36-48月：申请永居"
    ]

# =========================
# 🌐 UI 页面
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Study OS</title>
        <style>
            body { font-family: Arial; background:#f5f6fa; padding:30px; }
            .card {
                background:white;
                padding:20px;
                margin:15px 0;
                border-radius:12px;
                box-shadow:0 4px 10px rgba(0,0,0,0.05);
            }
            h1 { color:#2c3e50; }
            button {
                background:#4CAF50;
                color:white;
                padding:8px 15px;
                border:none;
                border-radius:6px;
                cursor:pointer;
            }
        </style>
    </head>

    <body>

        <h1>🌍 全球留学系统 Dashboard</h1>

        <div class="card">
            <h2>👤 注册 / 登录</h2>
            <form action="/login" method="post">
                用户名: <input name="username"><br><br>
                密码: <input name="password" type="password"><br><br>
                <button>登录 / 注册</button>
            </form>
        </div>

        <div class="card">
            <h2>🎯 生成你的留学路径</h2>
            <form action="/generate" method="post">
                用户ID: <input name="user_id"><br><br>

                学历:
                <select name="education">
                    <option value="bachelor">本科</option>
                    <option value="master">硕士</option>
                </select><br><br>

                预算:
                <select name="budget">
                    <option value="low">低</option>
                    <option value="high">高</option>
                </select><br><br>

                目标:
                <select name="goal">
                    <option value="immigration">移民</option>
                    <option value="career">就业</option>
                </select><br><br>

                <button>生成规划</button>
            </form>
        </div>

        <div class="card">
            <h2>📊 查看我的规划</h2>
            <form action="/plans" method="post">
                用户ID: <input name="user_id"><br><br>
                <button>查看</button>
            </form>
        </div>

    </body>
    </html>
    """

# =========================
# 👤 登录 / 注册合并
# =========================
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
        if user[2] == password:
            return f"<h2>登录成功！你的ID是：{user[0]}</h2><a href=' '>返回</a >"
        else:
            return "密码错误"
    else:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return f"<h2>注册成功！你的ID是：{cursor.lastrowid}</h2><a href='/'>返回</a >"

# =========================
# 🎯 生成规划
# =========================
@app.post("/generate")
def generate(user_id: int = Form(...), education: str = Form(...), budget: str = Form(...), goal: str = Form(...)):
    country = recommend_country(education, budget, goal)
    plan = generate_plan(country)

    cursor.execute(
        "INSERT INTO plans (user_id, country, content) VALUES (?, ?, ?)",
        (user_id, country, json.dumps(plan))
    )
    conn.commit()

    html = f"<h2>🌍 推荐国家：{country}</h2><div class='card'>"
    for p in plan:
        html += f"<p>{p}</p >"
    html += "</div><a href='/'>返回</a >"

    return HTMLResponse(html)

# =========================
# 📊 查看规划
# =========================
@app.post("/plans")
def get_plans(user_id: int = Form(...)):
    cursor.execute("SELECT country, content FROM plans WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()

    html = "<h1>📊 我的规划</h1>"

    for r in rows:
        plan = json.loads(r[1])
        html += f"<div class='card'><h3>{r[0]}</h3>"
        for p in plan:
            html += f"<p>{p}</p >"
        html += "</div>"

    html += "<a href='/'>返回</a >"

    return HTMLResponse(html)
