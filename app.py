import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import urllib.parse

# 1. 核心初始化
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. 页面配置
st.set_page_config(page_title="求学通-全球留学全能管家", layout="wide")
st.title("🎓 求学通：全球博士申请与海外生存全能系统")

# 3. 创建所有标签页
tabs = st.tabs([
    "🎯 导师匹配", 
    "🏠 落地生存", 
    "📄 简历润色", 
    "✉️ 陶瓷信直达", 
    "🤖 模拟面试", 
    "💼 就业居留", 
    "🍎 健康生活"
])

# --- Tab 1: 导师匹配 ---
with tabs[0]:
    st.header("🔍 全球导师极速匹配")
    kw = st.text_input("研究方向 (如: Computer Vision):", key="t1_kw")
    if st.button("🚀 寻找导师", key="t1_btn"):
        with st.spinner("检索中..."):
            st.markdown(model.generate_content(f"Find 3 professors in {kw}. Provide Name, University and Research focus.").text)

# --- Tab 2: 落地生存 (全球动态链接) ---
with tabs[1]:
    st.header("📍 全球落地生存传送门")
    c1, c2 = st.columns(2)
    with c1: g_country = st.text_input("输入国家 (如: 瑞士, 日本):", key="t2_cnt")
    with c2: g_city = st.text_input("输入城市:", key="t2_cty")
    
    if g_country and g_city:
        e_city = urllib.parse.quote(g_city)
        e_country = urllib.parse.quote(g_country)
        st.write(f"### 🔗 {g_city} 实时直达")
        l1, l2, l3, l4 = st.columns(4)
        l1.link_button("📕 小红书经验", f"https://www.xiaohongshu.com/search_result?keyword={e_city}{e_country}留学落地")
        l2.link_button("🛂 签证搜索", f"https://www.google.com/search?q={e_country}+student+visa+official")
        l3.link_button("🏠 租房搜索", f"https://www.google.com/search?q=best+rental+sites+in+{e_city}+{e_country}")
        l4.link_button("🏦 银行搜索", f"https://www.google.com/search?q=best+student+bank+in+{e_country}")
        
        if st.button("🧠 AI 落地建议", key="t2_ai"):
            st.markdown(model.generate_content(f"Student survival guide for {g_city}, {g_country}").text)

# --- Tab 3: 简历润色 ---
with tabs[2]:
    st.header("📄 CV 深度诊断")
    up = st.file_uploader("上传 PDF 简历", type="pdf", key="t3_up")
    if st.button("✨ 开启 AI 润色", key="t3_btn") and up:
        reader = PdfReader(up)
        text = "".join([p.extract_text() for p in reader.pages])
        st.markdown(model.generate_content(f"Refine this CV: {text}").text)

# --- Tab 4: 陶瓷信直达 (点击邮箱直达功能) ---
with tabs[3]:
    st.header("✉️ 陶瓷信一键直达")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        p_email = st.text_input("导师邮箱:", placeholder="example@uni.edu", key="t4_em")
        p_name = st.text_input("导师姓名:", key="t4_nm")
    with col_e2:
        r_topic = st.text_input("研究课题:", key="t4_tp")
        my_high = st.text_area("个人亮点:", key="t4_hi")

    if st.button("✍️ 生成陶瓷信", key="t4_btn"):
        if p_email and p_name:
            prompt = f"Write a professional PhD inquiry email to Prof. {p_name} about {r_topic}. My background: {my_high}."
            email_body = model.generate_content(prompt).text
            st.session_state['email_body'] = email_body
            st.subheader("📝 预览内容")
            st.markdown(email_body)
            
            # 核心功能：点击邮箱直达
            st.divider()
            subject = urllib.parse.quote(f"PhD Inquiry: {r_topic}")
            body = urllib.parse.quote(email_body)
            mailto_url = f"mailto:{p_email}?subject={subject}&body={body}"
            
            st.write(f"### 🚀 下一步：")
            st.link_button(f"📧 点击此处发送至: {p_email}", mailto_url, use_container_width=True)
        else:
            st.error("请先输入导师的邮箱和姓名")

# --- Tab 5: 模拟面试 ---
with tabs[4]:
    st.header("🤖 深度定制面试官")
    u_name = st.text_input("目标大学:", key="t5_u")
    u_topic = st.text_area("课题描述:", key="t5_t")
    if st.button("🏁 开始模拟", key="t5_btn"):
        st
