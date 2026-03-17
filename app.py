import streamlit as st
import requests
import json
import urllib.parse
from datetime import datetime

# --- 1. 商业级 AI 核心引擎 (2.5 级逻辑) ---
def call_ai(prompt):
    api_key = st.secrets.get("OPENROUTER_API_KEY")
    if not api_key: return "❌ 错误：请在 Secrets 配置 API Key"
    
    # 使用目前逻辑最强的商业模型，确保建议的深度
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
    return "❌ 逻辑节点繁忙，请稍后刷新重试。"

# --- 2. 自动化组件库 (极致唤起) ---
def google_maps(q): return f"https://www.google.com/maps/search/{urllib.parse.quote(q)}"
def email_gen(to, sub, body): return f"mailto:{to}?subject={urllib.parse.quote(sub)}&body={urllib.parse.quote(body)}"
def web_search(q): return f"https://www.google.com/search?q={urllib.parse.quote(q)}"

# --- 3. 界面布局 (本硕博全闭环设计) ---
st.set_page_config(page_title="全球求学通·Flagship 2.5", layout="wide")
st.title("🎓 全球求学通：本硕博全生命周期自动化系统")
st.caption("🌐 全球覆盖 | 比利时深度定制 | 商业逻辑已打通 | 唤起功能全开启")

# 重新设计的八大全面模块
tabs = st.tabs([
    "🛂 居留/签证/全家", "🎯 导师/网页/薪资", "✉️ 陶瓷/唤起/跟进", 
    "📄 文书/简历/润色", "💼 找工/永居/身份", "🍎 健康/心理/保险", 
    "🛡️ 法律/维权/举报", "📅 48月项目规划"
])

# --- 1. 居留/签证 (全球&本硕博全覆盖) ---
with tabs[0]:
    st.subheader("🌐 全球留学身份直达")
    c1, c2, c3 = st.columns(3)
    with c1: target_country = st.selectbox("目标国家:", ["比利时🇧🇪", "德国🇩🇪", "美国🇺🇸", "英国🇬🇧", "荷兰🇳🇱", "北欧🇸🇪", "加拿大🇨🇦", "澳洲🇦🇺"])
    with c2: user_level = st.selectbox("阶段:", ["本科 (Bachelor)", "硕士 (Master)", "博士 (PhD)", "博士后 (Postdoc)"])
    with c3: visa_event = st.selectbox("需求类型:", ["首次办理", "续签/换卡", "配偶陪读(全家)", "毕业找工签"])
    
    if st.button("🚀 深度解析政策并直达入口"):
        p = f"解析 {target_country} {user_level} 的 {visa_event} 政策。需包含：必备清单、家属陪读细则、本硕博权利差异、以及该国移民局地址。"
        st.markdown(call_ai(p))
        st.divider()
        sc1, sc2 = st.columns(2)
        with sc1: st.link_button(f"📍 直达 {target_country} 移民局/使馆地图", google_maps(f"{target_country} immigration office"))
        with sc2: st.link_button("📜 VFS 全球签证预约中心", "https://visa.vfsglobal.com/")

# --- 2. 导师/网页/薪资 (全自动搜索) ---
with tabs[1]:
    st.subheader("🔍 导师主页与学术背景全自动检索")
    prof_q = st.text_input("输入教授姓名或研究方向:")
    if st.button("🔎 一键搜索教授主页与实验室"):
        res = call_ai(f"分析关于 {prof_q} 的学术背景、所属实验室、以及该方向在欧洲的薪资标准。")
        st.markdown(res)
        bc1, bc2, bc3 = st.columns(3)
        with bc1: st.link_button("🌐 直达教授 Google Scholar", f"https://scholar.google.com/scholar?q={prof_q}")
        with bc2: st.link_button("💻 自动搜寻实验室主页", web_search(f"{prof_q} University Lab Homepage"))
        with bc3: st.link_button("💰 查看该国博士/博后薪资标准", web_search(f"PhD salary {target_country} net amount"))

# --- 3. 陶瓷/唤起/跟进 (全自动邮件) ---
with tabs[2]:
    st.subheader("✉️ 专家级陶瓷系统")
    p_name = st.text_input("教授姓名:", key="p_n")
    p_mail = st.text_input("教授邮箱 (填入后激活一键唤起):", key="p_m")
    if st.button("✍️ 撰写深度信件"):
        body = call_ai(f"给教授 {p_name} 写一封针对 {user_level} 申请的陶瓷信。要求：引用其研究，逻辑严密。")
        st.info(body)
        if p_mail:
            st.link_button("📧 一键唤起邮件客户端 (直接发送)", email_gen(p_mail, f"Inquiry from Prospective {user_level} Candidate", body))

# --- 5. 找工/永居 (身份闭环) ---
with tabs[4]:
    st.subheader("💼 职业发展与移民闭环")
    if st.button("📏 获取永居(PR)路径"):
        st.markdown(call_ai(f"详细解释 {target_country} 针对 {user_level} 毕业生的永居申请政策，包含时间线要求。"))
        st.link_button("💼 访问 Euraxess (欧洲官方科研招聘网)", "https://www.euraxess.be/")

# --- 7. 法律/维权 (全闭环保障) ---
with tabs[6]:
    st.subheader("🛡️ 留学生法律/维权一键直达")
    st.error("⚠️ 如果遭遇导师压榨、合同纠纷或学术不端，请点击下方直达：")
    st.link_button("⚖️ 定位大学调解员 (Ombudsperson) 办公室", google_maps("University Ombudsperson"))
    st.link_button("📜 了解比利时/欧洲研究人员劳工权利", "https://www.belgium.be/en/education/research/researchers")

# --- 8. 项目规划 (绝对稳定版) ---
with tabs[7]:
    st.subheader("📅 48个月全周期避坑时间轴")
    start_d = st.date_input("预计入学日期", value=datetime.now())
    if st.button("🗓️ 生成全闭环规划"):
        # 严格转换日期格式，彻底规避 f-string 报错
        d_str = start_d.strftime('%Y-%m-%d')
        st.markdown(call_ai(f"从 {d_str} 开始，为一名在 {target_country} 的 {user_level} 学生规划4年进度，标注签证续签及论文瓶颈。"))
