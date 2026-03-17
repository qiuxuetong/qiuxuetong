import streamlit as st
import requests
import json
import urllib.parse
from datetime import datetime

# --- 1. 核心引擎与环境检查 ---
def call_ai(prompt):
    api_key = st.secrets.get("OPENROUTER_API_KEY")
    if not api_key:
        st.error("🔑 请先在 Secrets 中设置 OPENROUTER_API_KEY")
        return ""
    
    # 付费用户尊享：Claude 3.5 Sonnet (逻辑之王) + Gemini 1.5 Pro
    models = ["anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5"]
    for model in models:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                data=json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}),
                timeout=60
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except: continue
    return "❌ 逻辑节点繁忙，请点击按钮重试。"

# --- 2. 全自动链接生成器 ---
def get_map_url(q): return f"https://www.google.com/maps/search/{urllib.parse.quote(q)}"
def get_mail_url(to, sub, body): return f"mailto:{to}?subject={urllib.parse.quote(sub)}&body={urllib.parse.quote(body)}"
def get_scholar_url(q): return f"https://scholar.google.com/scholar?q={urllib.parse.quote(q)}"

# --- 3. 界面架构 ---
st.set_page_config(page_title="求学通-商业全闭环", layout="wide", initial_sidebar_state="collapsed")
st.title("🎓 求学通：Flagship 2.5 商业全闭环博士系统")
st.info(f"📍 当前位置：比利时 🇧🇪 | 时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")

tabs = st.tabs(["🎯 导师/实验室", "📄 文献/简历", "✉️ 陶瓷唤起", "🤖 模拟面试", "💼 居留/就业", "🍎 健康/心理", "🛡️ 法律/维权", "📅 进度控制"])

# --- 1. 导师/实验室 (学术闭环) ---
with tabs[0]:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        research = st.text_input("输入研究关键词:", placeholder="例如: AI in Drug Discovery")
        if st.button("🚀 挖掘全球顶级实验室"):
            res = call_ai(f"针对 {research}，列出 3 个顶级实验室及其核心教授，并分析其‘给钱是否大方’。")
            st.markdown(res)
            st.divider()
            st.link_button("🌐 直接去 Google Scholar 搜论文", get_scholar_url(f"{research} lab professor"))
            st.link_button("📍 地图定位相关大学", get_map_url(f"Universities research in {research}"))

# --- 3. 陶瓷唤起 (邮件闭环) ---
with tabs[2]:
    st.subheader("✉️ 专家级陶瓷信 - 自动填充")
    p_name = st.text_input("教授姓名:")
    p_email = st.text_input("教授邮箱:")
    tone = st.select_slider("信件语气", options=["谦逊", "平级探讨", "学术挑战"])
    
    if st.button("✍️ 自动撰写并准备唤起"):
        email_body = call_ai(f"给教授 {p_name} 写一封陶瓷信，语气要 {tone}，内容要包含对其最新研究的深度见解。")
        st.info(body := email_body)
        if p_email:
            # 这就是你想要的“唤起”功能：点击即打开 Outlook/Gmail
            st.link_button("📧 一键唤起邮件客户端发送", get_mail_url(p_email, f"PhD Application Inquiry - {p_name}", body))

# --- 5. 居留/就业 (现实闭环) ---
with tabs[4]:
    st.subheader("💼 比利时/欧洲身份与就业规划")
    action = st.radio("你的当前需求:", ["办理签证", "换发居留卡", "博士毕业找工作", "配偶陪读"])
    if st.button("📍 获取官方入口与导航"):
        res = call_ai(f"详细解释在比利时如何执行: {action}。")
        st.markdown(res)
        # 自动定位布鲁塞尔签证处/市政厅
        st.link_button("📍 一键导航至布鲁塞尔移民局 (Office des Étrangers)", get_map_url("Boulevard Pacheco 44, 1000 Bruxelles"))
        st.link_button("🔗 进入比利时官方居留办理预约网页", "https://dofi.ibz.be/en")

# --- 8. 进度控制 (时间闭环) ---
with tabs[7]:
    st.subheader("📅 博士 48 个月全自动避坑时间轴")
    start_date = st.date_input("预计入学日期")
    if st.button("🗓️ 生成高压预警时间表"):
        plan = call_ai(f"从 {start_date} 开始，规划 4 年博士进度，标注出第几个月会遇到
