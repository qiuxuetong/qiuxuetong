import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import urllib.parse

# 1. 核心授权与模型初始化
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. 页面配置
st.set_page_config(page_title="求学通-全球留学全能管家", layout="wide")
st.title("🎓 求学通：全球博士申请、海外生存与终身发展全能系统")

# 3. 创建八大功能标签页 (严格检查：每一个 Tab 都有实质内容)
tabs = st.tabs([
    "🎯 导师匹配", "🏠 落地实战", "📄 简历润色", "✉️ 陶瓷信直达", 
    "🤖 模拟面试", "💼 就业居留", "🍎 健康生活", "🛡️ 留学生百宝箱"
])

# --- Tab 0: 导师匹配 ---
with tabs[0]:
    st.header("🔍 全球导师极速匹配")
    kw = st.text_input("研究方向 (如: NLP, Computer Vision):", key="t0_kw")
    if st.button("🚀 寻找导师", key="t0_btn"):
        with st.spinner("正在检索全球学术数据库..."):
            res = model.generate_content(f"Identify 3 active professors in {kw}. Provide: Name, University, Research focus.")
            st.markdown(res.text)

# --- Tab 1: 落地实战指南 ---
with tabs[1]:
    st.header("📍 落地前 7 天实战清单")
    c1, c2 = st.columns(2)
    with c1: t_cnt = st.text_input("目标国家 (如: 德国, 瑞士):", key="t1_cnt")
    with c2: t_cty = st.text_input("目标城市 (如: 慕尼黑, 苏黎世):", key="t1_cty")
    
    if st.button("📋 生成我的落地任务表", key="t1_btn"):
        if t_cnt and t_cty:
            with st.spinner("AI 正在制定详细路线图..."):
                p = f"为去 {t_cnt}{t_cty} 的留学生写一份首周实战清单。包含：24小时内必办、办卡必备材料清单、本地平价超市、安全避雷建议。"
                st.markdown(model.generate_content(p).text)
                st.divider()
                st.link_button("📕 小红书实时经验直达", f"https://www.xiaohongshu.com/search_result?keyword={urllib.parse.quote(t_cty)}留学落地")
        else:
            st.warning("请输入完整的国家和城市名称")

# --- Tab 2: 简历深度润色 ---
with tabs[2]:
    st.header("📄 CV 深度诊断与优化")
    up_file = st.file_uploader("上传 PDF 简历", type="pdf", key="t2_up")
    if st.button("✨ 开启 AI 润色", key="t2_btn"):
        if up_file:
            with st.spinner("AI 正在深度优化简历..."):
                reader = PdfReader(up_file)
                text = "".join([p.extract_text() for p in reader.pages])
                res = model.generate_content(f"Refine this academic CV for PhD application. Focus on logic, impact verbs, and academic formatting: {text}")
                st.markdown(res.text)
        else:
            st.warning("请先上传简历 PDF 文件")

# --- Tab 3: 陶瓷信一键直达 ---
with tabs[3]:
    st.header("✉️ 陶瓷信自动生成与直发")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        p_email = st.text_input("导师邮箱 (必填):", key="t3_em")
        p_name = st.text_input("导师姓名:", key="t3_nm")
    with col_e2:
        r_topic = st.text_input("拟申请课题:", key="t3_tp")
        my_high = st.text_area("简历亮点/背景简述:", key="t3_hi")

    if st.button("✍️ 生成陶瓷信内容", key="t3_btn"):
        if p_email and p_name:
            with st.spinner("AI 正在构思高回复率邮件..."):
                email_body = model.generate_content(f"Write a professional PhD inquiry email to Prof. {p_name} about {r_topic}. My highlights: {my_high}").text
                st.session_state['email_text'] = email_body
                st.markdown(email_body)
                
                # 生成跳转发件按钮
                subject = urllib.parse.quote(f"Inquiry: Potential PhD Application - {r_topic}")
                body = urllib.parse.quote(email_body)
                mailto_url = f"mailto:{p_email}?subject={subject}&body={body}"
                st.divider()
                st.link_button(f"📧 确认无误，一键发送至: {p_email}", mailto_url, use_container_width=True)
        else:
            st.error("请填入导师邮箱和姓名")

# --- Tab 4: 模拟面试助手 ---
with tabs[4]:
    st.header("🤖 深度定制 AI 面试官")
    u_name = st.text_input("申请大学 (如: ETH Zurich):", key="t4_u")
    u_topic = st.text_area("研究计划/课题简述:", key="t4_t")
    if st.button("🏁 生成面试挑战题", key="t4_btn"):
        if u_name and u_topic:
            with st.spinner("正在模拟教授思维..."):
                res = model.generate_content(f"You are a professor at {u_name}. Generate 5 tough PhD interview questions for a candidate researching {u_topic}. Provide answer tips for each.")
                st.markdown(res.text)
        else:
            st.warning("请输入大学和课题名称")

# --- Tab 5: 就业与长居规划 ---
with tabs[5]:
    st.header("💼 全球就业与永居路径分析")
    target_c = st.text_input("目标国家 (如: 瑞典, 新加坡, 日本):", key="t5_c")
    if st.button("📈 生成职业/身份报告", key="t5_btn"):
        if target_c:
            with st.spinner(f"正在调取 {target_c} 的最新人才政策..."):
                res = model.generate_content(f"Analyze PhD career path in {target_c}. Include: Post-study work visa, PR (Permanent Residency) requirements for high-skilled talent, and key industries.")
                st.markdown(res.text)
        else:
            st.warning("请输入国家名称")

# --- Tab 6: 健康生活品质 ---
with tabs[6]:
    st.header("🍎 留学品质生活：饮食、购物与旅游")
    l_city = st.text_input("所在城市 (如: 墨尔本, 巴黎):", key="t6_c")
    service = st.radio("你想发现什么？", ["健康饮食与亚超", "物价与购物商场", "周末短途旅游"], key="t6_s")
    if st.button("🌟 开启高品质生活", key="t6_btn"):
        if l_city:
            with st.spinner("正在搜罗本地资讯..."):
                res = model.generate_content(f"For a student in {l_city}, provide a detailed guide on {service}. Include specific spots and money-saving hacks.")
                st.markdown(res.text)
        else:
            st.warning("请输入城市名称")

# --- Tab 7: 留学生百宝箱 ---
with tabs[7]:
    st.header("🛡️ 留学生全能百宝箱")
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        tool_type = st.selectbox("隐藏挑战类型:", ["⚖️ 法律维权 (房东/合同纠纷)", "💰 省钱秘籍 (退税/优惠)", "🧠 心理树洞 (压力/孤独)", "🚨 紧急求助 (丢失/医疗)"], key="t7_tool")
    with b_col2:
        b_cnt = st.text_input("所在国家 (如: 意大利):", key="t7_cnt")
    
    if st.button("🔍 获取专家级对策", key="t7_btn"):
        if b_cnt:
            with st.spinner("正在调取应急预案..."):
                res = model.generate_content(f"As an expert for students in {b_cnt}, provide detailed professional advice for '{tool_type}'. Include steps and resources.")
                st.markdown(res.text)
        else:
            st.warning("请输入所在国家")
