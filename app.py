import streamlit as st
import google.generativeai as genai
import urllib.parse
import re

# 1. 配置 Gemini (Gemini 1.5 Flash 是目前的标准稳定版)
# 配置 API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 设置模型 (根据你之前的成功测试，确保是 gemini-2.5-flash)
model = genai.GenerativeModel('gemini-2.5-flash')

# 【新增调试行】用来在网页上确认钥匙是否生效
st.write(f"🔑 当前系统使用的 Key 开头是: {st.secrets['GOOGLE_API_KEY'][:4]}")

st.set_page_config(page_title="导师套磁专家", layout="wide")
st.title("🎓 博士申请导师匹配系统")

keywords = st.text_input("请输入具体研究方向 (如: Medical Image Analysis):")

if st.button("🚀 极速匹配 3 位导师"):
    if not keywords:
        st.warning("请输入方向")
    else:
        try:
            with st.spinner("正在扫描全球顶尖实验室..."):
                prompt = f"""
                Identify 3 active professors specializing in '{keywords}'.
                Format each strictly:
                [PROF]
                NAME: 姓名
                UNI: 学校
                EMAIL: 邮箱
                SITE: 官网URL
                LETTER: 
                Subject: Prospective PhD - [Your Name] - {keywords}
                
                Dear Prof. [Name],
                I am a student interested in your work on {keywords}... (200 words)
                [END]
                """
                response = model.generate_content(prompt)
                blocks = re.findall(r"\[PROF\](.*?)\[END\]", response.text, re.DOTALL)

            tabs = st.tabs([f"导师 {i+1}" for i in range(len(blocks))])
            for i, tab in enumerate(tabs):
                with tab:
                    b = blocks[i].strip()
                    p_name = re.search(r"NAME:\s*(.*)", b).group(1) if "NAME:" in b else "Unknown"
                    p_uni = re.search(r"UNI:\s*(.*)", b).group(1) if "UNI:" in b else "Unknown"
                    p_email = re.search(r"EMAIL:\s*(.*)", b).group(1) if "EMAIL:" in b else ""
                    p_site = re.search(r"SITE:\s*(.*)", b).group(1).strip() if "SITE:" in b else "#"
                    p_letter = b.split("LETTER:")[1].strip() if "LETTER:" in b else ""

                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.success(f"### {p_name}\n**{p_uni}**")
                        st.write(f"📧 邮箱: `{p_email}`")
                        
                        # 重点优化：双保险链接
                        st.link_button("🌐 点击直达官网 (若404请用下方按钮)", p_site)
                        
                        google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(p_name + ' ' + p_uni + ' faculty page')}"
                        st.link_button("🔍 在 Google 中搜索该教授", google_search_url)
                        
                    with c2:
                        final_msg = st.text_area("文书预览：", value=p_letter, height=300, key=f"t{i}")
                        subj = urllib.parse.quote(f"Inquiry: PhD position in {keywords}")
                        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={p_email}&su={subj}"
                        st.link_button("🚀 一键唤起 Gmail 发送", gmail_url)

        except Exception as e:
            st.error(f"生成失败，请刷新页面重试: {e}")
import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

# 1. 配置 (沿用你的 Key)
API_KEY = "AIzaSyA034xj5H-cGARDWleYIDLJ23etQKE_IDc".strip()
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.header("📄 AI 简历(CV) 深度润色专家")
st.info("上传你的 PDF 版简历，AI 将根据学术标准为你提供润色建议。")

# 2. 文件上传
uploaded_file = st.file_uploader("选择你的 CV (PDF格式)", type="pdf")

if uploaded_file is not None:
    try:
        # 读取 PDF 文本
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        cv_text = ""
        for page in pdf_reader.pages:
            cv_text += page.extract_text()
        
        if st.button("✨ 开始 AI 诊断"):
            with st.spinner("正在逐句分析你的科研经历..."):
                # 润色 Prompt
                refine_prompt = f"""
                You are a senior professor at a top university. Analyze and refine the following CV text:
                {cv_text}
                
                Please provide:
                1. **Overall Score**: (Out of 10)
                2. **Weak Spots**: Identiy phrasing that is too casual or vague.
                3. **Refined Bullet Points**: Rewrite at least 3 research/project descriptions using strong action verbs (e.g., 'Spearheaded', 'Optimized').
                4. **Academic Tone**: Suggest 3 keywords to add to make it sound more professional for a PhD application.
                """
                
                response = model.generate_content(refine_prompt)
                
                st.subheader("✅ 诊断报告")
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"简历读取失败: {e}")

# 3. 接下来怎么做？
st.divider()
st.subheader("💡 你的“求学通”网站蓝图")
st.write("""
1. **第一步 (当前)**：把『导师查找』和『CV 润色』做成两个 Tab 标签页。
2. **第二步**：增加一个『生活指南』板块，放几个你觉得对比利时生活最有用的链接。
3. **第三步**：尝试把这个代码部署到 **Streamlit Cloud**，发给同学试用。
""")
