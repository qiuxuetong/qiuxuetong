import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# 1. 核心初始化
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. 页面配置
st.set_page_config(page_title="求学通-全能留学管家", layout="wide")
st.title("🎓 求学通：博士申请与海外生活全能系统")

# 3. 标签页增加：落地生活服务
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 导师与学术匹配", 
    "🏠 落地生活服务 (必看)", 
    "📄 简历与文书润色", 
    "✉️ 陶瓷信自动生成",
    "🤖 面试与日常口语模拟"
])

# --- Tab 1: 导师匹配 (略，保持原有功能) ---
with tab1:
    st.header("🔍 全球导师极速匹配")
    keywords = st.text_input("请输入研究方向:", key="prof_search")
    if st.button("🚀 寻找导师"):
        with st.spinner("检索中..."):
            prompt = f"Find 3 active professors for '{keywords}'. Include Name, University, and Research focus."
            st.markdown(model.generate_content(prompt).text)

# --- Tab 2: 落地生活服务 (全新升级版！) ---
with tab2:
    st.header("📍 到达后的 168 小时：落地服务指南")
    col1, col2 = st.columns([1, 2])
    with col1:
        city = st.text_input("输入你的目的城市 (如: Munich, Sydney, Toronto):")
        needs = st.multiselect(
            "哪些是你的当务之急？",
            ["本地手机卡 (SIM Card)", "银行开户 (Bank Account)", "医疗保险与GP注册", "市政厅/警察局注册", "学生交通卡办理", "二手家具/二手车渠道"],
            default=["本地手机卡 (SIM Card)", "银行开户 (Bank Account)"]
        )
    
    with col2:
        st.info("💡 提示：AI 会为你提供具体的操作步骤、所需材料清单以及本地评价最高的供应商。")
        if st.button("📋 生成我的落地清单"):
            if city:
                with st.spinner(f"正在准备 {city} 的生活手册..."):
                    prompt = f"""
                    Provide a 'First Week Survival Guide' for a student arriving in {city}. 
                    Focus on: {needs}.
                    For each selected item, provide:
                    1. **Where to go**: Specific locations or recommended providers (e.g., specific banks or telecom brands).
                    2. **What to bring**: A checklist of documents (Passport, Visa, Letter of Acceptance, etc.).
                    3. **Evaluation**: Why these providers are better for international students.
                    4. **Pro-tip**: One local secret to save money or time.
                    """
                    st.markdown(model.generate_content(prompt).text)
            else:
                st.warning("请输入城市名称")

# --- Tab 3: 简历润色 (略) ---
with tab3:
    st.header("📄 CV 深度诊断")
    uploaded_file = st.file_uploader("上传 PDF 简历", type="pdf")
    if st.button("✨ 开启 AI 润色"):
        if uploaded_file:
            reader = PdfReader(uploaded_file)
            cv_text = "".join([page.extract_text() for page in reader.pages])
            prompt = f"Critique and improve this academic CV text: {cv_text}"
            st.markdown(model.generate_content(prompt).text)

# --- Tab 4: 陶瓷信生成 (略) ---
with tab4:
    st.header("✉️ 陶瓷信生成")
    p_name = st.text_input("导师姓名:")
    my_bg = st.text_area("我的优势:")
    if st.button("✍️ 生成邮件"):
        prompt = f"Write a professional PhD inquiry email to {p_name} based on: {my_bg}"
        st.code(model.generate_content(prompt).text)

# --- Tab 5: 语言模拟 (新增日常场景) ---
with tab5:
    st.header("🗣️ 场景口语与面试模拟")
    scenario = st.selectbox("选择模拟场景", ["博士面试", "银行开户沟通", "与房东谈租约", "去诊所看医生"])
    if st.button("💬 开始模拟"):
        prompt = f"Act as a person in the scenario: {scenario}. Give me 3 common questions they might ask me and 3 suggested professional responses."
        st.markdown(model.generate_content(prompt).text)
