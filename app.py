import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import urllib.parse

# 1. 核心初始化
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. 页面配置
st.set_page_config(page_title="求学通-全球留学全能管家", layout="wide")
st.title("🎓 求学通：全链路博士申请与海外生存系统")

# 3. 创建标签页
tabs = st.tabs(["🎯 导师匹配", "🏠 落地生存", "📄 简历润色", "✉️ 陶瓷信直达", "🤖 模拟面试", "💼 就业居留", "🍎 健康生活"])

# --- [Tab 1-3 保持原有逻辑，此处略以节省空间，实际代码中请保留] ---

# --- Tab 4: 陶瓷信一键直达 (重点升级！) ---
with tabs[3]:
    st.header("✉️ 陶瓷信自动生成与一键发送")
    st.info("填写信息生成草稿后，点击“🚀 唤起邮件客户端”即可直接发送。")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        prof_email = st.text_input("导师邮箱 (必填):", placeholder="professor@university.edu", key="t4_email")
        prof_name = st.text_input("导师姓名:", key="t4_name")
    with col_m2:
        research_topic = st.text_input("拟申请的研究课题:", key="t4_topic")
        tone = st.selectbox("邮件语气:", ["Professional & Formal", "Enthusiastic", "Short & Direct"])

    my_highlights = st.text_area("你的研究亮点/简历核心 (建议从 Tab 3 复制):", key="t4_highlights")

    if st.button("✍️ 生成陶瓷信内容", key="b4_gen"):
        if prof_email and prof_name:
            with st.spinner("AI 正在构思高回复率邮件..."):
                email_prompt = f"""
                Write a PhD inquiry email to Prof. {prof_name}. 
                Topic: {research_topic}. 
                My background: {my_highlights}. 
                Tone: {tone}.
                Please provide a clear Subject Line and the Email Body.
                """
                response = model.generate_content(email_prompt).text
                
                # 将生成的正文存入 session_state 以便后面调用
                st.session_state['generated_email'] = response
                st.subheader("📝 预览邮件内容")
                st.markdown(response)
        else:
            st.warning("请填写导师邮箱和姓名")

    # 一键直达逻辑
    if 'generated_email' in st.session_state:
        st.divider()
        # 提取主题和正文（简单处理：取第一行为主题，其余为正文）
        email_content = st.session_state['generated_email']
        subject = f"PhD Inquiry - {research_topic} - Your Name"
        body = email_content
        
        # 对字符进行 URL 编码，防止空格和特殊字符导致链接失效
        mailto_link = f"mailto:{prof_email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        
        st.write("### 🚀 准备好了？")
        st.link_button("📬 一键唤起邮箱直达", mailto_link, use_container_width=True)
        st.caption("注：点击后将自动打开你电脑自带的邮箱软件。")

# --- [Tab 5-7 保持原有逻辑] ---
