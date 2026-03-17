import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import urllib.parse

# 1. 核心初始化
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. 页面配置
st.set_page_config(page_title="求学通-全球留学全能管家", layout="wide")
st.title("🎓 求学通：博士申请、海外生存与生活品质全能系统")

# 3. 创建七大功能标签页
tabs = st.tabs([
    "🎯 导师匹配", 
    "🏠 落地生存", 
    "📄 简历润色", 
    "✉️ 陶瓷信生成",
    "🤖 模拟面试",
    "💼 就业居留",
    "🍎 健康饮食与生活"
])

# --- Tab 1: 导师匹配 ---
with tabs[0]:
    st.header("🔍 全球导师极速匹配")
    keywords = st.text_input("研究方向 (如: NLP):", key="t1")
    if st.button("🚀 寻找导师", key="b1"):
        with st.spinner("检索中..."):
            st.markdown(model.generate_content(f"Find 3 professors in {keywords}.").text)

# --- Tab 2: 落地与实时搜索 ---
with tabs[1]:
    st.header("📍 落地生活传送门")
    city = st.text_input("目标城市:", key="t2")
    if city:
        encoded_city = urllib.parse.quote(city)
        c1, c2, c3 = st.columns(3)
        with c1: st.link_button("📕 小红书经验", f"https://www.xiaohongshu.com/search_result?keyword={encoded_city}留学落地")
        with c2: st.link_button("🏠 实时房源", f"https://www.rightmove.co.uk/property-to-rent/find.html?searchLocation={encoded_city}")
        with c3: st.link_button("🛂 签证官方", "https://www.gov.uk/browse/visas-immigration/student-visas")
        if st.button("🧠 获取 AI 指南", key="b2"):
            st.markdown(model.generate_content(f"Survival guide for {city}").text)

# --- Tab 3: 简历润色 ---
with tabs[2]:
    st.header("📄 CV 深度诊断")
    up_file = st.file_uploader("上传 PDF", type="pdf", key="t3")
    if st.button("✨ 开启润色", key="b3") and up_file:
        reader = PdfReader(up_file)
        text = "".join([p.extract_text() for p in reader.pages])
        st.markdown(model.generate_content(f"Refine this CV: {text}").text)

# --- Tab 4: 陶瓷信生成 ---
with tabs[3]:
    st.header("✉️ 陶瓷信自动生成")
    p_name = st.text_input("导师姓名:", key="t4_n")
    my_bg = st.text_area("你的亮点:", key="t4_b")
    if st.button("✍️ 生成邮件草稿", key="b4"):
        st.code(model.generate_content(f"Write PhD email to {p_name} background {my_bg}").text)

# --- Tab 5: 模拟面试 ---
with tabs[4]:
    st.header("🤖 AI 模拟面试官")
    if st.button("🏁 开始面试挑战", key="b5"):
        st.markdown(model.generate_content("Generate 5 PhD interview questions.").text)

# --- Tab 6: 就业与长期居留 ---
with tabs[5]:
    st.header("💼 就业与长期居留规划")
    target_country = st.selectbox("选择国家:", ["英国", "美国", "德国", "加拿大", "澳洲"], key="t6")
    if st.button("📈 生成路径报告", key="b6"):
        st.markdown(model.generate_content(f"Roadmap to job and PR in {target_country} for PhD").text)

# --- Tab 7: 留学健康饮食与生活 (新增！) ---
with tabs[6]:
    st.header("🍎 留学生活品质：饮食、购物与旅行")
    col_a, col_b = st.columns([1, 2])
    with col_a:
        current_city = st.text_input("输入当前所在/目标城市:", key="t7_city")
        service = st.radio("你想发现什么？", ["健康饮食 (中餐/亚超/健康菜谱)", "购物商场 (Outlets/折扣超市)", "旅游打卡 (周末游/短途旅行)"])
    
    if st.button("🌟 开启高品质生活", key="b7"):
        if current_city:
            with st.spinner("AI 正在为您搜罗本地生活资讯..."):
                lifestyle_prompt = f"""
                Provide a lifestyle guide for a Chinese student in {current_city} focusing on {service}.
                If Diet: Mention Asian supermarkets, authentic Chinese food spots, and healthy cooking tips for busy students.
                If Shopping: Mention local affordable supermarkets, premium shopping malls, and best outlet nearby.
                If Travel: List 3 nearby 'must-visit' spots for a weekend trip.
                Format with emojis and friendly tone.
                """
                st.markdown(model.generate_content(lifestyle_prompt).text)
        else:
            st.warning("请先输入城市名称")
