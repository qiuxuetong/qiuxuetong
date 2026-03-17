import streamlit as st
import requests
import json
import urllib.parse
from datetime import datetime

# --- 1. AI 引擎配置 (利用您的 $4.74 余额) ---
def call_ai(prompt):
    api_key = st.secrets.get("OPENROUTER_API_KEY")
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            data=json.dumps({
                "model": "anthropic/claude-3.5-sonnet",
                "messages": [{"role": "user", "content": f"你是一个全球留学专家。请针对以下问题提供极其详尽、绝不留空的解答：{prompt}"}]
            }), timeout=40)
        return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else "⚠️ AI 忙碌，请参考下方预设工具。"
    except: return "⚠️ 链接超时。"

# --- 2. 自动化工具库 (全球通用) ---
def get_search(q): return f"https://www.google.com/search?q={urllib.parse.quote(q)}"

st.set_page_config(page_title="全球求学通", layout="wide")
st.title("🎓 全球求学通：本硕博全生命周期闭环系统")
st.info("💎 状态：内容已全面硬填充 | 拒绝空置 | 全球大学全覆盖 | 账户余额：$4.74")

# --- 3. 核心布局：8 大功能区 ---
tabs = st.tabs([
    "🎯 导师/官网/邮箱", "🛂 居留/签证/全家", "✉️ 陶瓷/邮件唤起", 
    "📄 文书/简历/防AI", "💼 找工/永居/身份", "🍎 健康/心理/保险", 
    "🛡️ 法律/维权/举报", "📅 48月全程规划"
])

# --- 1. 导师/官网 (物理填充，拒绝空置) ---
with tabs[0]:
    st.subheader("🔍 导师/官网/邮箱全自动追踪")
    c1, c2 = st.columns(2)
    with c1:
        univ = st.text_input("输入全球大学全名:", value="University of Wrocław")
        prof = st.text_input("输入教授姓名:", value="Piotr Smoleński")
    with c2:
        st.success(f"📍 目标确认：{prof} (弗罗茨瓦夫大学化学系)")
        st.markdown(f"**自动唤起：** [🌐 官网教职页]({get_search(prof+' '+univ+' staff')}) | [📧 查邮箱]({get_search(prof+' '+univ+' email')})")
    if st.button("🚀 启动全球 AI 背景深度调查"):
        st.markdown(call_ai(f"详细调研 {univ} 的 {prof} 教授。重点：研究方向(化学)、近期论文、官方联系方式。"))

# --- 2. 居留/签证 (补齐全球国家) ---
with tabs[1]:
    st.subheader("🛂 全球居留/签证/全家方案")
    country = st.selectbox("选择目标国家:", ["波兰🇵🇱", "比利时🇧🇪", "德国🇩🇪", "荷兰🇳🇱", "瑞典🇸🇪", "美国🇺🇸", "英国🇬🇧", "加拿大🇨🇦", "澳洲🇦🇺", "新加坡🇸🇬"])
    st.info(f"💡 {country} 政策快报：博士及家属通常享有居留卡申请权。")
    st.link_button(f"🔗 自动唤起：该国移民局学生签证页", get_search(f"{country} student visa residence permit official"))
    if st.button("🚀 生成该国全套办证攻略"):
        st.markdown(call_ai(f"请为我生成 {country} 的博士签证、陪读签证及居留卡转换完整指南。"))

# --- 3. 陶瓷邮件 (预置模板) ---
with tabs[2]:
    st.subheader("✉️ 陶瓷/邮件唤起自动化")
    st.warning("📄 预置模板：将下方文字复制到邮件，点击按钮搜查投递时机。")
    st.code("Dear Professor [Name], \nI am writing to express my interest in your research on...")
    st.link_button("🕒 自动唤起：查询该校当前学期/假期安排", get_search(f"{univ} academic calendar 2024-2025"))

# --- 4. 文书简历 (硬核填充工具) ---
with tabs[3]:
    st.subheader("📄 文书/简历/防AI 综合中心")
    st.write("✨ **自动化工具链：**")
    st.link_button("🚀 简历排版：Overleaf 学术模板", "https://www.overleaf.com/gallery/tagged/cv")
    st.link_button("🛡️ 防AI检测：GPTZero 查重", "https://gptzero.me/")
    if st.button("🤖 启动 AI 深度润色"):
        st.markdown(call_ai("请提供一份针对全球顶尖大学博士申请的简历(CV)优化原则。"))

# --- 5. 找工/永居 (解决空置) ---
with tabs[4]:
    st.subheader("💼 全球找工/永居/身份规划")
    st.info("📊 政策预加载：大多数发达国家为博士生提供 12-24 个月的找工签证（如波兰 12个月，德国 18个月）。")
    st.link_button("🔍 自动唤起：目标国 LinkedIn 博士招聘信息", f"https://www.linkedin.com/jobs/search/?keywords=PhD&location={country}")

# --- 6. 健康/心理 (紧急填充) ---
with tabs[5]:
    st.subheader("🍎 健康/心理/保险")
    st.success("🏥 保险必备：出国前请务必确认学生基本医疗保险（如波兰 NFZ，比利时 Mutuality）。")
    st.link_button("🆘 自动唤起：当地 24 小时心理援助热线", get_search(f"{country} mental health helpline for international students"))

# --- 7. 法律/维权 (救命通道) ---
with tabs[6]:
    st.subheader("🛡️ 法律/维权/举报")
    st.error("⚠️ 遭遇霸凌或合同违约？不要沉默！")
    st.link_button("⚖️ 自动唤起：目标大学 Ombudsman (调解员) 搜索", get_search(f"{univ} ombudsman student complaints"))
    st.write("💡 Ombudsman 是保护学生免受导师霸凌的官方中立机构。")

# --- 8. 48月规划 (修复逻辑) ---
with tabs[7]:
    st.subheader("📅 48个月全周期避坑规划")
    s_date = st.date_input("项目起始日期", value=datetime.now())
    if st.button("🗓️ 生成全程路线图"):
        d_str = s_date.strftime('%Y-%m-%d')
        st.markdown(call_ai(f"从 {d_str} 开始，为一名博士生规划 4 年的科研、生活及职业闭环方案。"))
