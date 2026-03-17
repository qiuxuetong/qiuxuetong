import streamlit as st
import requests
import json
import urllib.parse
from datetime import datetime

# --- 1. 核心商业级 AI 引擎 ---
def call_ai(prompt):
    api_key = st.secrets.get("OPENROUTER_API_KEY")
    if not api_key: return "❌ 错误：请在 Streamlit 后台配置 API Key"
    # 锁定全球最强逻辑：Claude 3.5 Sonnet (逻辑深度第一) 与 Gemini 1.5 Pro
    models = ["anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5"]
    for model in models:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                data=json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.4}),
                timeout=60
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except: continue
    return "❌ 逻辑节点繁忙，请重试。"

# --- 2. 自动化工具库 ---
def google_maps(q): return f"https://www.google.com/maps/search/{urllib.parse.quote(q)}"
def email_gen(to, sub, body): return f"mailto:{to}?subject={urllib.parse.quote(sub)}&body={urllib.parse.quote(body)}"
def scholar_gen(q): return f"https://scholar.google.com/scholar?q={urllib.parse.quote(q)}"

# --- 3. 界面布局 ---
st.set_page_config(page_title="求学通-全闭环旗舰版", layout="wide")
st.title("🎓 求学通：2.5 级博士申请全自动闭环系统")
st.info(f"🇧🇪 当前定位：比利时 | 商业额度：已激活 | 逻辑等级：Flagship 2.5")

tabs = st.tabs(["🎯 导师/实验室", "📄 简历/网页", "✉️ 陶瓷/邮件", "🤖 面试/压力", "💼 居留/签证", "🍎 健康/心理", "🛡️ 法律/维权", "🏗️ 项目规划"])

# --- 1. 导师/实验室：全自动检索 ---
with tabs[0]:
    kw = st.text_input("输入研究方向 (如: Medical Image Analysis):", key="t1_kw")
    if st.button("🚀 深度挖掘实验室与直达搜索"):
        res = call_ai(f"针对 {kw} 方向，精准列出 3 个全球顶尖实验室、核心教授及其研究主张。")
        st.markdown(res)
        st.divider()
        col1, col2 = st.columns(2)
        with col1: st.link_button("🌐 查看该方向顶级论文 (Scholar)", scholar_gen(f"{kw} high impact papers"))
        with col2: st.link_button("📍 定位欧洲相关大学", google_maps(f"Top Universities for {kw} in Europe"))

# --- 2. 简历/网页：全自动重构 ---
with tabs[1]:
    cv_input = st.text_area("粘贴你的简历或项目描述:", height=200)
    if st.button("✨ 2.5 级逻辑重构并直达 LinkedIn"):
        res = call_ai(f"请用 STAR 法则重写这段经历，并给出 LinkedIn Profile 的关键词优化建议：\n{cv_input}")
        st.write(res)
        st.link_button("🔗 前往 LinkedIn 更新档案", "https://www.linkedin.com/feed/")
        st.link_button("📂 查看欧洲标准 CV 模板 (Europass)", "https://europa.eu/europass/en/create-europass-cv")

# --- 3. 陶瓷/邮件：一键唤起 ---
with tabs[2]:
    p_name = st.text_input("教授姓名:")
    p_email = st.text_input("教授邮箱 (填入后可一键唤起):")
    p_paper = st.text_input("教授最近的一篇论文关键词:")
    if st.button("✍️ 自动撰写陶瓷信并准备发送"):
        body = call_ai(f"根据教授 {p_name} 在 {p_paper} 方面的研究，写一封深度的陶瓷信，要求逻辑严密，避免套话。")
        st.markdown("### 预览正文:")
        st.success(body)
        if p_email:
            st.link_button("📧 一键唤起邮件客户端发送 (Outlook/Mail)", email_gen(p_email, f"Prospective PhD Inquiry - {p_name}", body))

# --- 4. 面试/压力：全真模拟 ---
with tabs[3]:
    if st.button("🎙️ 启动 2.5 级学术压力面试模拟"):
        res = call_ai("模拟严厉面试官，针对我的‘研究可行性’提出三个刁钻问题。")
        st.markdown(res)
        st.link_button("🎥 参考：如何应对博士面试 (YouTube)", "https://www.youtube.com/results?search_query=phd+interview+tips")

# --- 5. 居留/签证：比利时专属直达 ---
with tabs[4]:
    st.subheader("🇧🇪 比利时生存与政策直达")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("🛂 比利时移民局官网 (Dofi)", "https://dofi.ibz.be/en")
        st.link_button("📍 导航：布鲁塞尔移民局总署", google_maps("Office des Étrangers Bruxelles"))
    with col2:
        st.link_button("📋 查找你所在城市的市政厅 (Commune)", google_maps("Commune Administration Belgium"))
        st.link_button("💼 比利时博士后/科研职位招聘 (Euraxess)", "https://www.euraxess.be/")

# --- 6. 健康/心理：紧急支持 ---
with tabs[5]:
    st.subheader("🍎 博士心理健康与紧急直达")
    st.warning("博士期间压力极大，请务必关注心理健康。")
    st.link_button("🆘 搜索附近全科医生 (GP/Huisarts)", google_maps("General Practitioner near me"))
    st.link_button("🧠 欧洲学术心理支持资源 (Mental Health)", "https://www.eurodoc.net/mental-health")
    st.link_button("🏥 搜索附近最近的医院 (Emergency)", google_maps("Hospital Emergency"))

# --- 7. 法律/维权：申博保障 ---
with tabs[6]:
    st.subheader("🛡️ 导师学术不端或合同纠纷直达")
    st.markdown("如果遇到导师拖欠工资或侵占学术成果：")
    st.link_button("⚖️ 搜索各大学调解员 (Ombudsperson)", google_maps("University Ombudsperson Belgium"))
    st.link_button("📜 比利时科研人员劳动法指南", "https://www.belgium.be/en/education/research/researchers")

# --- 8. 项目规划：48 个月闭环 ---
with tabs[7]:
    start_date = st.date_input("预计入学/开始日期", value=datetime.now())
    if st.button("🗓️ 生成全自动避坑时间轴"):
        # 修复了上一版引号未闭合的语法错误
        prompt = f"从 {start_date} 开始规划 4 年博士进度。要求细化到月，标注出‘签证续签月’、‘论文瓶颈月’、‘答辩准备期’。"
        plan = call_ai(prompt)
        st.markdown(plan)
        st.link_button("📆 同步到我的 Google Calendar", "https://calendar.google.com/calendar/render?action=TEMPLATE")
