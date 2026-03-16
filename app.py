import streamlit as st
import google.generativeai as genai
import urllib.parse
import re
from PyPDF2 import PdfReader

# 1. 核心配置：使用 Secrets 安全加载 API Key
# 调试信息（运行成功后可以删掉下面这一行）
if "GOOGLE_API_KEY" in st.secrets:
    st.write(f"🔑 系统状态：API Key 已成功加载 (开头: {st.secrets['GOOGLE_API_KEY'][:4]})")
else:
    st.error("❌ 错误：未在 Streamlit Secrets 中找到 GOOGLE_API_KEY")

# 初始化全局模型
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. 页面设置
st.set_page_config(page_title="导师套磁专家", layout="wide")
st.title("🎓 博士申请导师匹配系统")

# --- 第一部分：导师匹配 ---
keywords = st.text_input("请输入具体研究方向 (如: Medical Image Analysis):")

if st.button("🚀 极速匹配 3 位导师"):
    if not keywords:
        st.warning("请输入研究方向")
    else:
        try:
            with st.spinner("正在扫描全球顶尖实验室..."):
                prompt = f"Identify 3 active professors specializing in '{keywords}'. Format each strictly: 1. Name, 2. University, 3. Research focus."
                response = model.generate_content(prompt)
                st.subheader("📍 推荐导师列表")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"导师查找失败: {e}")

st.divider()

# --- 第二部分：简历润色 ---
st.header("📄 AI 简历 (CV) 深度润色专家")
uploaded_file = st.file_uploader("上传你的 PDF 版简历", type="pdf")

if st.button("✨ 开始 AI 诊断"):
    if uploaded_file is not None:
        try:
            with st.spinner("正在分析简历并生成润色建议..."):
                # 读取 PDF 内容
                reader = PdfReader(uploaded_file)
                cv_text = ""
                for page in reader.pages:
                    cv_text += page.extract_text()
                
                # 再次确保 API 连接（防止 Streamlit 运行丢失状态）
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                temp_model = genai.GenerativeModel('gemini-2.5-flash')
                
                refine_prompt = f"""
                You are a senior professor. Analyze and refine the following CV text:
                {cv_text}
                
                Please provide:
                1. Overall Score (Out of 10)
                2. Weak Spots
                3. Refined Bullet Points (using strong action verbs)
                4. Academic Tone Keywords
                """
                
                response = temp_model.generate_content(refine_prompt)
                st.subheader("✅ 诊断报告")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"简历诊断过程中出现错误: {e}")
    else:
        st.warning("请先上传 PDF 简历")

# --- 第三部分：网站蓝图 ---
with st.expander("💡 你的“求学通”网站蓝图"):
    st.write("1. 第一步：导师查找和 CV 润色已激活。")
    st.write("2. 第二步：未来可加入自动生成套磁信功能。")
