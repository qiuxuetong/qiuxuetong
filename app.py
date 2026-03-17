import streamlit as st
import requests
import json
import urllib.parse
from datetime import datetime

# --- 1. 商业级 AI 核心引擎 (2.5 级逻辑) ---
def call_ai(prompt):
    api_key = st.secrets.get("OPENROUTER_API_KEY")
    if not api_key: return "❌ 错误：请在 Streamlit 侧边栏/后台配置 OPENROUTER_API_KEY"
    
    # 锁定商业级逻辑模型：Claude 3.5 或 Gemini 1.5 Pro
    models = ["anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5"]
    for model in models:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                data=json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}),
                timeout=45
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except Exception: continue
    return "❌ 逻辑节点暂时繁忙，请稍后刷新重试。"

# --- 2. 自动化组件库 ---
def google_maps(q): return f"https://www.google.com/maps/search/{urllib.parse.quote(q)}"
def email_gen(to, sub, body): return f"mailto:{to}?subject={urllib.parse.quote(sub)}&body={urllib.parse.quote(body)}"

# --- 3. 界面布局 (极致精简+功能闭环) ---
st.set_page_config(page_title="全球求学通·Flagship 2.5", layout="wide", initial_sidebar_state="collapsed")

st.title("🎓 全球求学通：本硕博全生命周期闭环系统")
st.caption("🇧🇪 商业版已激活 | 定位：全球/比利时深度支持 | 逻辑等级：Commercial 2.5")

# 重新梳理后的八大核心模块
tabs = st.tabs([
    "🛂 居留/签证/全家", "🎯 导师/匹配/薪资", "✉️ 陶瓷/唤起/跟进", 
    "📄 文书/简历/防AI", "💼 找工/永居/身份", "🍎 健康/心理/保险", 
    "🛡️ 法律/维权/举报", "🏗️ 4年项目规划"
])

# --- 1. 居留/签证 (全球&本硕博全覆盖) ---
with tabs[0]:
    st.subheader("🌐 全球留学身份直达")
    col1, col2, col3 = st.columns(3)
    with col1:
        target_country = st.selectbox("目标国家:", ["比利时🇧🇪", "德国🇩🇪", "美国🇺🇸", "英国🇬🇧", "荷兰🇳🇱", "北欧🇸🇪/🇳🇴", "加拿大🇨🇦", "澳洲🇦🇺"])
    with col2:
        user_level = st.selectbox("学术阶段:", ["本科 (Bachelor)", "硕士 (Master)", "博士 (PhD)", "博士后 (Postdoc)"])
    with col3:
        visa_type = st.selectbox("事务类型:", ["首次签证办理", "本地续签/换发", "配偶陪读(全家)", "毕业找工签"])
    
    if st.button("🚀 深度解析办理逻辑"):
        p = f"详细解析在 {target_country} 读 {user_level} 的 {visa_type} 政策。要求包括：必备材料、该国特有的法律陷阱、博士是否算工龄、以及如何携带家属。"
        st.markdown(call_ai(p))
        st.divider()
        st.write("📍 **周边办理中心直达 (根据定位搜索):**")
        st.link_button(f"导航至 {target_country} 驻外/本地办理点", google_maps(f"{target_country} immigration office or embassy"))

# --- 2. 导师/匹配/薪资 ---
with tabs[1]:
    kw = st.text_input("输入研究关键词 (如: Quantum Cryptography):")
    if st.button("🔍 智能匹配导师与测算薪资"):
        p = f"列出 {kw} 方向全球 Top 3 教授及薪资水平(对比德比英荷)。说明该方向博后后的出路。"
        st.markdown(call_ai(p))
        st.link_button("🌐 Scholar 论文直达", f"https://scholar.google.com/scholar?q={kw}")

# --- 3. 陶瓷/跟进 (防石沉大海逻辑) ---
with tabs[2]:
    p_name = st.text_input("教授姓名:")
    p_mail = st.text_input("教授 Email:")
    if st.button("✍️ 自动撰写深度陶瓷信"):
        body = call_ai(f"给教授 {p_name} 写一封针对 {user_level} 申请的信，包含两轮跟进(Follow-up)的策略提示。")
        st.success(body)
        if p_mail:
            st.link_button("📧 一键唤起 Outlook/Gmail 发送", email_gen(p_mail, "Prospective Application Inquiry", body))

# --- 5. 找工/永居 (长远考虑) ---
with tabs[4]:
    st.subheader("💼 永居(PR)与职业路径")
    if st.button("📏 计算我的永居进度"):
        p = f"在 {target_country}，{user_level} 毕业后如何以最快速度拿到永居？列出时间线和税前薪资要求。"
        st.markdown(call_ai(p))
        st.link_button("💼 全欧科研职位搜索引擎 (Euraxess)", "https://www.euraxess.be/")

# --- 7. 法律维权 (你没考虑到但必须有的) ---
with tabs[6]:
    st.subheader("🛡️ 留学生/博士维权与安全")
    st.warning("如遇导师学术不端、克扣工资、职场霸凌，请使用以下渠道：")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("⚖️ 搜索各大学调解员 (Ombudsperson)", google_maps("University Ombudsperson"))
    with col2:
        st.link_button("📜 查看当地劳动保障局", google_maps("Labor department"))

# --- 8. 4年项目规划 (绝对无语法错误版) ---
with tabs[7]:
    start_date = st.date_input("预计开始日期", value=datetime.now())
    if st.button("🗓️ 生成全周期风险规避图"):
        # 严格修复变量引用，彻底规避 SyntaxError
        start_str = start_date.strftime('%Y-%m-%d')
        prompt_text = f"从 {start_str} 开始，为一名在 {target_country} 的 {user_level} 学生规划 48 个月的时间线。必须包含：签证续签点、论文发表关键节点、心理压力高发月、答辩准备月。"
        res_plan = call_ai(prompt_text)
        st.markdown(res_plan)
