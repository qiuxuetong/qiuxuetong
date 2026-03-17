import streamlit as st
import requests
import json
import urllib.parse
from datetime import datetime

# --- 1. 商业级 AI 核心引擎 (双模型冗余) ---
def call_ai(prompt):
    api_key = st.secrets.get("OPENROUTER_API_KEY")
    if not api_key: return "❌ 错误：请先在 Secrets 中设置 API Key"
    models = ["anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5"]
    for model in models:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                data=json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}),
                timeout=50
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except: continue
    return "❌ 节点繁忙，建议稍后刷新。"

# --- 2. 全自动唤起工具库 ---
def google_maps(q): return f"https://www.google.com/maps/search/{urllib.parse.quote(q)}"
def google_search(q): return f"https://www.google.com/search?q={urllib.parse.quote(q)}"
def email_gen(to, sub, body): return f"mailto:{to}?subject={urllib.parse.quote(sub)}&body={urllib.parse.quote(body)}"

# --- 3. 界面布局与全闭环模块 ---
st.set_page_config(page_title="全球求学通·Flagship 2.5", layout="wide")
st.title("🎓 全球求学通：本硕博全生命周期自动化系统")
st.info("💎 商业授权版 | 全球签证·家属陪读·奖学金薪资·维权保障 | 2.5 级逻辑已锁死")

tabs = st.tabs([
    "🛂 居留/签证/全家", "🎯 导师/邮箱/主页", "✉️ 陶瓷/唤起/跟进", 
    "📄 文书/简历/防AI", "💼 找工/永居/身份", "🍎 健康/保险/医疗", 
    "🛡️ 法律/维权/举报", "🏗️ 48月全景规划"
])

# --- 1. 居留/签证 (全球&全自动方案) ---
with tabs[0]:
    st.subheader("🌐 全球身份直达引擎")
    c1, c2, c3 = st.columns(3)
    with c1: target_country = st.selectbox("目标国家:", ["比利时🇧🇪", "德国🇩🇪", "荷兰🇳🇱", "美国🇺🇸", "英国🇬🇧", "瑞典🇸🇪", "加拿大🇨🇦", "澳洲🇦🇺"])
    with c2: user_level = st.selectbox("阶段:", ["本科 (Bachelor)", "硕士 (Master)", "博士 (PhD)"])
    with c3: visa_event = st.selectbox("需求:", ["首次办理", "本地续签", "全家陪读", "毕业找工"])
    
    if st.button("🚀 自动生成方案与官方入口"):
        p = f"详细解析 {target_country} {user_level} 的 {visa_event} 政策。必须包含：资金证明要求、家属是否有权工作、博士工龄折算、以及移民局具体地址。"
        st.markdown(call_ai(p))
        sc1, sc2, sc3 = st.columns(3)
        with sc1: st.link_button("📍 定位当地移民局", google_maps(f"{target_country} immigration office"))
        with sc2: st.link_button("📜 VFS 全球预约中心", "https://visa.vfsglobal.com/")
        with sc3: st.link_button("📑 官方材料 Checklist 搜寻", google_search(f"{target_country} {visa_event} checklist official"))

# --- 2. 导师/邮箱/主页 (解决你“自己找”的痛点) ---
with tabs[1]:
    st.subheader("🔍 导师/邮箱/主页全自动搜寻")
    prof_info = st.text_input("输入教授姓名或研究关键词 (如: Medical AI):")
    if st.button("🔎 启动全自动背景挖掘"):
        res = call_ai(f"深度分析 {prof_info}。包括：其学术影响力、主要研究课题、以及在 {target_country} 的平均博士薪资标准。")
        st.markdown(res)
        bc1, bc2, bc3 = st.columns(3)
        with bc1: st.link_button("📧 搜寻教授 Email 地址", google_search(f"{prof_info} email address contact"))
        with bc2: st.link_button("🌐 搜寻实验室主页", google_search(f"{prof_info} laboratory homepage university"))
        with bc3: st.link_button("🔬 查看 Google Scholar", f"https://scholar.google.com/scholar?q={prof_info}")
        st.caption("⚠️ 提示：点击‘搜寻教授 Email’，AI 已帮你生成好搜索关键词，通常第一条就是官方通讯录。")

# --- 3. 陶瓷/唤起 (自动邮件) ---
with tabs[2]:
    p_email = st.text_input("在此粘贴你搜到的邮箱 (一键唤起使用):")
    if st.button("✍️ 自动撰写陶瓷信 (含多轮跟进逻辑)"):
        body = call_ai(f"作为一名申请 {target_country} 的 {user_level} 候选人，写一封针对 {prof_info} 的陶瓷信。")
        st.success(body)
        if p_email:
            st.link_button("📧 点击直接发邮件", email_gen(p_email, f"Inquiry from {user_level} Candidate", body))

# --- 5. 找工/永居 (长远规划) ---
with tabs[4]:
    st.subheader("💼 职业发展与移民闭环")
    if st.button("📊 自动计算永居路径"):
        st.markdown(call_ai(f"详细解释 {target_country} 针对 {user_level} 毕业生的永居(PR)时间线，包含起薪要求。"))
        st.link_button("💼 官方科研岗位网 (Euraxess)", "https://www.euraxess.be/")

# --- 7. 法律/维权 (救命模块) ---
with tabs[6]:
    st.subheader("🛡️ 法律维权与安全通道")
    st.error("遭受不公待遇、导师霸凌或合同欺诈时，请直达：")
    st.link_button("⚖️ 定位大学调解员 (Ombudsperson)", google_maps("University Ombudsperson Office"))
    st.link_button("📜 搜寻当地法律援助 (Legal Aid)", google_search(f"Legal aid for international students in {target_country}"))

# --- 8. 48月规划 (稳定版) ---
with tabs[7]:
    start_d = st.date_input("预计日期", value=datetime.now())
    if st.button("📅 生成全景图"):
        d_str = start_d.strftime('%Y-%m-%d')
        st.markdown(call_ai(f"从 {d_str} 开始，为 {target_country} 的 {user_level} 规划48个月，标注续签及论文关键月。"))
