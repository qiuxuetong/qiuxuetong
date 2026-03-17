import streamlit as st
import requests
import json
import urllib.parse
from datetime import datetime

# --- 1. 核心商业引擎 ---
def call_ai(prompt):
    api_key = st.secrets.get("OPENROUTER_API_KEY")
    if not api_key: return "❌ 未检测到 API Key"
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
    return "❌ 逻辑节点繁忙，请重试。"

# --- 2. 直达工具函数 ---
def maps(q): return f"https://www.google.com/maps/search/{urllib.parse.quote(q)}"
def mail(to, sub, body): return f"mailto:{to}?subject={urllib.parse.quote(sub)}&body={urllib.parse.quote(body)}"

# --- 3. UI 界面 ---
st.set_page_config(page_title="求学通-Flagship 2.5", layout="wide")
st.title("🎓 求学通：2.5 级博士全闭环全自动系统")
st.caption(f"📍 当前：比利时 | 商业级链路已打通 | {datetime.now().strftime('%H:%M')}")

tabs = st.tabs(["🎯 导师匹配", "📄 简历润色", "✉️ 陶瓷直达", "🤖 模拟面试", "💼 居留就业", "🍎 生活健康", "🛡️ 申博保障", "📅 进度控制"])

# --- 1. 导师匹配 ---
with tabs[0]:
    kw = st.text_input("输入研究方向:", placeholder="如: Hair Design / Medical Imaging")
    if st.button("🚀 深度挖掘实验室"):
        res = call_ai(f"分析方向 {kw}，给出3位顶级教授及其最新论文逻辑。")
        st.markdown(res)
        st.link_button("🌐 直达 Google Scholar 深度搜索", f"https://scholar.google.com/scholar?q={kw}")

# --- 3. 陶瓷直达 (全自动唤起) ---
with tabs[2]:
    col1, col2 = st.columns(2)
    with col1: p_name = st.text_input("教授姓名:")
    with col2: p_email = st.text_input("教授邮箱:")
    if st.button("✍️ 自动写信并准备发送"):
        body = call_ai(f"给教授 {p_name} 写一封 2.5 级深度的陶瓷信，字里行间体现专业度。")
        st.info(body)
        if p_email:
            st.link_button("📧 一键唤起 Outlook/Gmail 发送", mail(p_email, f"Inquiry - {p_name}", body))

# --- 5. 居留就业 (全自动导航) ---
with tabs[4]:
    st.subheader("🇧🇪 比利时生存直达")
    city = st.selectbox("选择你的城市", ["Bruxelles", "Leuven", "Gent", "Antwerpen"])
    if st.button("📍 自动查找办事处与就业机会"):
        st.link_button(f"🚩 导航至 {city} 市政厅 (办理居留)", maps(f"Stadhuis {city}"))
        st.link_button(f"💼 查找 {city} 附近科技园", maps(f"Science Park in {city}"))
        st.markdown("建议：在比利时找博士后/企业 R&D 职位，首选 LinkedIn 联动。")

# --- 7. 申博保障 (维权/合规) ---
with tabs[6]:
    st.subheader("🛡️ 博士权益与合规查询")
    if st.button("🔍 自动检索维权入口"):
        st.markdown("欧洲博士通常被视为员工，受工会保护。")
        st.link_button("📜 查看比利时博士劳工合同规范", "https://www.belgium.be/en/education/research/researchers")
        st.link_button("⚖️ 搜索各大学调解员 (Ombudsperson)", maps("University Ombudsperson Belgium"))

# --- 8. 进度控制 (修复了语法错误的版本) ---
with tabs[7]:
    st.subheader("📅 48个月自动规避崩溃时间轴")
    start_date = st.date_input("预计入学日期", value=datetime.now())
    if st.button("🗓️ 生成全周期规划"):
        prompt = f"从 {start_date} 开始规划 4 年博士进度，详细到月，并指出第几个月是瓶颈期。"
        plan = call_ai(prompt) # 这里修复了之前的引号错误
        st.markdown(plan)
        st.link_button("📅 打开 Google 日历记录里程碑", "https://calendar.google.com/")
