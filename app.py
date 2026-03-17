import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import urllib.parse

# 1. 初始化
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. 页面配置
st.set_page_config(page_title="求学通-全球留学全能管家", layout="wide")
st.title("🎓 求学通：博士申请、海外生存与直达链接系统")

# 3. 创建八大功能标签页
tabs = st.tabs([
    "🎯 导师匹配", "🏠 落地实战", "📄 简历润色", "✉️ 陶瓷信直达", 
    "🤖 模拟面试", "💼 就业居留", "🍎 健康生活", "🛡️ 留学生百宝箱"
])

# --- Tab 0: 导师匹配 (增强版：带直达链接) ---
with tabs[0]:
    st.header("🔍 全球导师极速匹配 & 直达链接")
    kw = st.text_input("输入研究方向 (如: Robot Learning, FinTech):", key="t0_kw")
    if st.button("🚀 寻找导师并生成链接", key="t0_btn"):
        with st.spinner("正在检索学术大咖..."):
            # 让 AI 返回结构化数据
            prompt = f"Find 3 active professors in {kw}. Format: Name|University|Research. (No extra text)"
            res = model.generate_content(prompt).text
            
            # 解析 AI 返回的内容并生成按钮
            profs = res.strip().split('\n')
            for p in profs:
                if '|' in p:
                    name, uni, research = p.split('|')
                    with st.container():
                        st.subheader(f"👨‍🏫 {name.strip()}")
                        st.write(f"🏫 **学校**: {uni.strip()}  |  🔬 **方向**: {research.strip()}")
                        
                        # 生成直达链接
                        q_name = urllib.parse.quote(f"{name.strip()} {uni.strip()}")
                        c1, c2 = st.columns(2)
                        c1.link_button(f"🔍 在 Google Scholar 搜论文", f"https://scholar.google.com/scholar?q={q_name}")
                        c2.link_button(f"🌐 搜大学官网主页", f"https://www.google.com/search?q={q_name}+official+website+faculty")
                        st.divider()

# --- Tab 1: 落地实战指南 ---
with tabs[1]:
    st.header("📍 落地前 7 天清单")
    c1, c2 = st.columns(2)
    with c1: t_cnt = st.text_input("国家:", key="t1_cnt")
    with c2: t_cty = st.text_input("城市:", key="t1_cty")
    if st.button("📋 生成清单", key="t1_btn"):
        if t_cnt and t_cty:
            st.markdown(model.generate_content(f"提供 {t_cnt}{t_cty} 留学生首周落地清单：办卡、租房、避雷、超市。").text)
            st.link_button("📕 小红书实时经验", f"https://www.xiaohongshu.com/search_result?keyword={urllib.parse.quote(t_cty)}留学落地")

# --- Tab 2: 简历润色 ---
with tabs[2]:
    st.header("📄 CV 深度诊断")
    up_file = st.file_uploader("上传 PDF 简历", type="pdf", key="t2_up")
    if st.button("✨ 开启润色", key="t2_btn") and up_file:
        reader = PdfReader(up_file)
        text = "".join([p.extract_text() for p in reader.pages])
        st.markdown(model.generate_content(f"优化这段简历的学术表达：{text}").text)

# --- Tab 3: 陶瓷信直达 (点击邮箱直发) ---
with tabs[3]:
    st.header("✉️ 陶瓷信一键直达")
    e1, e2 = st.columns(2)
    with e1:
        p_email = st.text_input("导师邮箱:", key="t3_em")
        p_name = st.text_input("导师姓名:", key="t3_nm")
    with e2:
        r_topic = st.text_input("拟申请课题:", key="t3_tp")
        my_high = st.text_area("个人亮点:", key="t3_hi")
    if st.button("✍️ 生成陶瓷信", key="t3_btn"):
        body = model.generate_content(f"Write PhD email to {p_name} about {r_topic}. Highlights: {my_high}").text
        st.markdown(body)
        mailto_url = f"mailto:{p_email}?subject={urllib.parse.quote('PhD Inquiry')}&body={urllib.parse.quote(body)}"
        st.link_button(f"📧 一键发送至: {p_email}", mailto_url, use_container_width=True)

# --- Tab 4: 模拟面试 ---
with tabs[4]:
    st.header("🤖 定制面试官")
    u_name = st.text_input("大学名称:", key="t4_u")
    u_topic = st.text_area("课题简介:", key="t4_t")
    if st.button("🏁 开始面试", key="t4_btn"):
        st.markdown(model.generate_content(f"Generate 5 interview questions for {u_name} on {u_topic}").text)

# --- Tab 5: 就业居留 ---
with tabs[5]:
    st.header("💼 全球就业与长居")
    target_c = st.text_input("目标国家 (就业分析):", key="t5_c")
    if st.button("📈 生成报告", key="t5_btn"):
        st.markdown(model.generate_content(f"PhD career and PR roadmap in {target_c}").text)

# --- Tab 6: 健康生活 ---
with tabs[6]:
    st.header("🍎 留学生活品质")
    l_city = st.text_input("所在城市 (饮食旅游):", key="t6_c")
    if st.button("🌟 发现美好", key="t6_btn"):
        st.markdown(model.generate_content(f"Student guide for food and lifestyle in {l_city}").text)

# --- Tab 7: 百宝箱 ---
with tabs[7]:
    st.header("🛡️ 留学生百宝箱")
    tool = st.selectbox("挑战类型:", ["法律维权", "省钱秘籍", "心理树洞", "紧急求助"], key="t7_tool")
    b_cnt = st.text_input("所在国家:", key="t7_cnt")
    if st.button("🔍 获取对策", key="t7_btn"):
        st.markdown(model.generate_content(f"Advice for {tool} in {b_cnt}").text)
