import streamlit as st
import sqlite3
import json

st.set_page_config(page_title="全球留学系统", layout="wide")

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

def recommend_country(education, budget, goal):
    scores = {
        "Canada": 0,
        "Germany": 0,
        "Netherlands": 0,
        "USA": 0
    }

    if goal == "移民":
        scores["Canada"] += 3
        scores["Germany"] += 2
    else:
        scores["USA"] += 2
        scores["Netherlands"] += 1

    if budget == "低":
        scores["Germany"] += 3
    else:
        scores["USA"] += 2
        scores["Canada"] += 1

    if education == "本科":
        scores["Canada"] += 2
    elif education == "硕士":
        scores["Netherlands"] += 1
    elif education == "博士":
        scores["Germany"] += 1

    return max(scores, key=scores.get)

def generate_plan(country):
    return [
        "0-6个月：选国家、选学校、准备语言成绩、整理材料",
        "6-12个月：提交申请、跟进结果、准备签证和住宿",
        "12-24个月：入学、适应生活、做实习和项目经历",
        "24-36个月：准备毕业、投递工作、优化简历和面试",
        "36-48个月：办理工作签证/长期居留，规划永居路径"
    ]

st.title("🌍 全球留学一条龙系统")
st.caption("申请｜签证｜租房｜求医｜购物｜就业｜长期规划")

tab1, tab2, tab3 = st.tabs(["登录/注册", "生成规划", "查看我的规划"])

with tab1:
    st.subheader("用户登录 / 注册")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("注册"):
            if username and password:
                try:
                    cursor.execute(
                        "INSERT INTO users (username, password) VALUES (?, ?)",
                        (username, password)
                    )
                    conn.commit()
                    st.success("注册成功")
                except sqlite3.IntegrityError:
                    st.error("用户名已存在")
            else:
                st.warning("请填写用户名和密码")

    with col2:
        if st.button("登录"):
            if username and password:
                cursor.execute(
                    "SELECT id FROM users WHERE username=? AND password=?",
                    (username, password)
                )
                user = cursor.fetchone()
                if user:
                    st.session_state["user_id"] = user[0]
                    st.session_state["username"] = username
                    st.success(f"登录成功，你的用户ID是：{user[0]}")
                else:
                    st.error("用户名或密码错误")
            else:
                st.warning("请填写用户名和密码")

with tab2:
    st.subheader("生成留学路径")

    if "user_id" not in st.session_state:
        st.info("请先在“登录/注册”页登录")
    else:
        st.write(f"当前用户：{st.session_state['username']}（ID: {st.session_state['user_id']}）")

        education = st.selectbox("当前阶段", ["本科", "硕士", "博士"])
        budget = st.selectbox("预算水平", ["低", "高"])
        goal = st.selectbox("主要目标", ["移民", "就业"])

        if st.button("生成方案"):
            country = recommend_country(education, budget, goal)
            plan = generate_plan(country)

            cursor.execute(
                "INSERT INTO plans (user_id, country, content) VALUES (?, ?, ?)",
                (st.session_state["user_id"], country, json.dumps(plan, ensure_ascii=False))
            )
            conn.commit()

            st.success(f"推荐国家：{country}")
            for step in plan:
                st.write("• " + step)

with tab3:
    st.subheader("我的历史规划")

    if "user_id" not in st.session_state:
        st.info("请先登录")
    else:
        cursor.execute(
            "SELECT id, country, content FROM plans WHERE user_id=? ORDER BY id DESC",
            (st.session_state["user_id"],)
        )
        rows = cursor.fetchall()

        if not rows:
            st.warning("你还没有生成过规划")
        else:
            for row in rows:
                plan_id, country, content = row
                with st.expander(f"方案 #{plan_id} ｜ {country}", expanded=False):
                    items = json.loads(content)
                    for item in items:
                        st.write("• " + item)
