import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import urllib.parse  # 新增：用于处理网页链接

# 1. 核心初始化
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. 页面配置
st.set_page_config(page_title="求学通-全能留学助手", layout="wide")
st.title("🎓 求学通：博士申请与海外生活全能系统")

# 3. 标签页
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 导师匹配", "🏠 落地与实时搜索", "📄 简历润色", "✉️ 陶瓷信生成", "🤖 模拟面试"
])

# --- Tab 2: 落地生活与实时直达 (重点升级！) ---
with tab2:
    st.header("📍 落地生活指南 & 实时信息传送门")
    city = st.text_input("输入你的目标城市 (如: London, Boston, Munich):", key="city_input")
    
    if city:
        # 预先编码城市名，用于生成链接
        encoded_city = urllib.parse.quote(city)
        
        st.write(f"### 🔗 {city} 实时信息直达")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.link_button("📕 小红书搜索", f"https://www.xiaohongshu.com/search_result?keyword={encoded_city}留学落地")
        with c2:
            st.link_button("🏠 实时房源 (Rightmove)", f"https://www.rightmove.co.uk/property-to-rent/find.html?searchLocation={encoded_city}")
        with c3:
            st.link_button("🏦 银行开户指南", f"https://www.google.com/search?q={encoded_city}+student+bank+account+comparison")
        with c4:
            st.link_button("🛂 签证官方入口", "https://www.gov.uk/browse/visas-immigration/student-visas")

        st.divider()
        
        # AI 深度分析部分
        needs = st.multiselect("需要 AI 为你分析哪些细节？", ["办理流程", "物价评价", "安全区域建议", "超市分布"], default=["办理流程", "安全区域建议"])
        if st.button("🧠 获取 AI 深度建议"):
            with st.spinner("AI 正在结合经验为你分析..."):
                prompt = f"Provide detailed student advice for {city} focusing on {needs}. Include common pitfalls and pro-tips."
                st.markdown(model.generate_content(prompt).text)
    else:
        st.info("👆 请先输入城市名称，我们将为你生成专属的直达链接和 AI 指南。")

# (其他 Tab 1, 3, 4, 5 保持之前的逻辑即可...)
