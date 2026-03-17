import streamlit as st
import datetime
import json
import os
import smtplib
from email.mime.text import MIMEText

DATA_FILE = "tasks.json"

# 初始化
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_tasks():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# =========================
# 📧 邮件发送函数
# =========================
def send_email(to_email, subject, content):
    try:
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = "your@email.com"
        msg['To'] = to_email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("your@email.com", "your_app_password")
            server.send_message(msg)

        return True
    except Exception as e:
        return str(e)

# =========================
# 🌍 UI
# =========================
st.title("🌍 全球48个月规划系统（升级版）")

# =========================
# ➕ 添加任务
# =========================
st.header("➕ 添加任务")

with st.form("task_form"):
    country = st.selectbox("国家", ["Canada", "Germany", "Netherlands", "USA", "Australia"])
    task_name = st.text_input("任务")
    date = st.date_input("截止日期")
    task_type = st.selectbox("类型", ["normal", "email"])
    email = st.text_input("邮箱（邮件任务用）")

    submitted = st.form_submit_button("添加")

    if submitted and task_name:
        tasks = load_tasks()
        tasks.append({
            "country": country,
            "task": task_name,
            "date": str(date),
            "status": "pending",
            "type": task_type,
            "email": email
        })
        save_tasks(tasks)
        st.success("✅ 添加成功")

# =========================
# 📊 显示任务
# =========================
st.header("📊 当前任务")

tasks = load_tasks()
today = datetime.date.today()

for i, t in enumerate(tasks):
    task_date = datetime.datetime.strptime(t["date"], "%Y-%m-%d").date()
    days_left = (task_date - today).days

    st.divider()
    st.subheader(f"{t['country']} - {t['task']}")

    # ⏰ 提醒
    if days_left <= 0:
        st.error(f"❗ 已到期：{t['date']}")
    elif days_left <= 2:
        st.warning(f"⚠️ 即将到期：{t['date']}")
    else:
        st.write(f"📅 截止日期：{t['date']}")

    # 状态
    new_status = st.selectbox(
        "状态",
        ["pending", "doing", "done"],
        index=["pending", "doing", "done"].index(t["status"]),
        key=f"status_{i}"
    )

    if new_status != t["status"]:
        tasks[i]["status"] = new_status
        save_tasks(tasks)

    # 📧 邮件功能
    if t["type"] == "email" and t["email"]:
        if st.button(f"📧 发送跟进邮件 #{i}"):
            result = send_email(
                t["email"],
                "Follow-up",
                f"Dear Professor,\n\nI would like to follow up on my previous email regarding {t['task']}.\n\nBest regards"
            )
            if result == True:
                st.success("邮件发送成功")
            else:
                st.error(result)

# =========================
# 🗑️ 删除
# =========================
st.header("🗑️ 删除任务")

if len(tasks) > 0:
    delete_index = st.number_input("输入编号", 0, len(tasks)-1)
    if st.button("删除"):
        tasks.pop(delete_index)
        save_tasks(tasks)
        st.success("删除成功")
