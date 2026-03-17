import datetime
import time
import smtplib
from email.mime.text import MIMEText

# =========================
# 🌍 国家评分系统
# =========================
countries = {
    "Canada": {"immigration": 9, "job": 7, "risk": 3},
    "Germany": {"immigration": 7, "job": 8, "risk": 4},
    "Netherlands": {"immigration": 6, "job": 8, "risk": 5},
    "USA": {"immigration": 3, "job": 10, "risk": 8},
    "Australia": {"immigration": 8, "job": 7, "risk": 4}
}

def choose_best_country(countries):
    score = {}
    for c in countries:
        score[c] = countries[c]["immigration"] + countries[c]["job"] - countries[c]["risk"]
    return max(score, key=score.get)

# =========================
# 📋 任务系统（48个月）
# =========================
tasks = [
    {
        "id": 1,
        "country": "Germany",
        "task": "套磁导师",
        "date": "2026-03-20",
        "status": "pending",
        "email": "prof@example.com",
        "type": "follow_up"
    },
    {
        "id": 2,
        "country": "Canada",
        "task": "提交签证",
        "date": "2026-04-01",
        "status": "pending",
        "type": "deadline"
    },
    {
        "id": 3,
        "country": "Netherlands",
        "task": "投递简历",
        "date": "2026-03-22",
        "status": "pending",
        "type": "job"
    }
]

# =========================
# 📧 邮件发送
# =========================
def send_email(to_email, subject, content):
    try:
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = "your@email.com"
        msg['To'] = to_email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("your@email.com", "your_password")
            server.send_message(msg)

        print(f"📨 邮件已发送: {to_email}")
    except Exception as e:
        print("❌ 邮件发送失败:", e)

# =========================
# 🔔 自动提醒系统
# =========================
def check_tasks(tasks):
    today = datetime.date.today()

    for task in tasks:
        task_date = datetime.datetime.strptime(task["date"], "%Y-%m-%d").date()
        days_left = (task_date - today).days

        if task["status"] == "done":
            continue

        # ⏰ 提前提醒
        if days_left <= 2:
            print(f"⚠️ 即将到期: {task['task']} ({task['country']}) - {task['date']}")

        # 📧 自动跟进邮件
        if task["type"] == "follow_up" and days_left <= 0:
            send_email(
                task["email"],
                "Follow-up Reminder",
                f"Dear Professor,\n\nI would like to follow up on my previous email.\n\nBest regards"
            )
            task["status"] = "done"

# =========================
# 🔄 状态更新
# =========================
def update_task_status(task_id, new_status):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            print(f"✅ 任务 {task_id} 更新为 {new_status}")

# =========================
# 📊 打印任务面板
# =========================
def print_dashboard(tasks):
    print("\n📊 当前任务状态：")
    for task in tasks:
        print(f"[{task['status']}] {task['country']} - {task['task']} - {task['date']}")

# =========================
# 🚀 主循环（自动运行）
# =========================
def run_system():
    print("🌍 全球规划系统启动...")
    best = choose_best_country(countries)
    print(f"🎯 推荐优先国家: {best}")

    while True:
        print_dashboard(tasks)
        check_tasks(tasks)
        time.sleep(86400)  # 每天运行一次

# =========================
# ▶️ 启动
# =========================
if __name__ == "__main__":
    run_system()
