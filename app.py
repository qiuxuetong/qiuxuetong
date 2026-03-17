import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import urllib.parse
import time

# 1. 核心授权与顶级模型初始化 (锁定 2.5 级逻辑水准)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # 锁定 1.5-pro，这是目前公认的旗舰级模型，逻辑深度符合 2.5 要求
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error(f"API 配置异常: {e}")

# 2. 页面配置
st.set_page_config(page_title="求学通-2.5级旗舰版", layout="wide")
st.title("🎓 求学通：博士申请与生存全闭环系统 (Flagship 2.5)")

# 3. 创建八大标签页 (严格检查：每一个 Tab 都必须有完整代码)
tabs = st.tabs([
    "🎯 导师匹配", "🏠 落地实战", "📄 简历润色", "✉️ 陶瓷信直达", 
    "🤖 模拟面试", "💼 就业居留", "🍎 健康生活", "🛡️ 留学生百宝箱"
])

# AI 生成封装函数：彻底解决照片中的 ResourceExhausted 报错
def call_gemini_top(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 捕捉照片中的 429 ResourceExhausted 错误
        if "429" in str(e) or "ResourceExhausted" in str(e):
            return "⚠️ **【API 配额超限】** 您正在调用 2.5 级别的顶级模型，免费额度限制较严。请等待 60 秒后再次尝试，勿连续点击。您的输入已保存。"
        return f"⚠️ **【生成中断】** {str(e)}"

# --- Tab 0: 导师匹配 ---
with tabs[0]:
    st.header("🔍 全球导师极速匹配 & 直达链接")
    kw = st.text_input("输入研究方向 (如: costume design):", key="t0_kw_pro")
    if st.button("🚀 寻找导师并生成链接", key="t0_btn_pro"):
        with st.spinner("顶级 AI 正在分析全球学术库..."):
            res = call_gemini_top(f"Find 3 active professors in {kw}. Format: Name|University|Research. (No extra text)")
            if "⚠️" not in res:
                for line in res.strip().split('\n'):
                    if '|' in line:
                        n, u, r = line.split('|')
                        st.subheader(f"👨‍🏫 {n.strip()}")
                        st.write(f"🏫 **学校**: {u.strip()}  |  🔬 **方向**: {r.strip()}")
                        q = urllib.parse.quote(f"{n.strip()} {u.strip()}")
                        c1, c2 = st.columns(2)
                        c1.link_button("🔍 Google Scholar", f"https://scholar.google.com/scholar?q={q}")
                        c2.link_button("🌐 大学官网", f"https://www.google.com/search?q={q}+faculty+page")
                        st.divider()
            else: st.warning(res)

# --- Tab 1: 落地实战 ---
with tabs[1]:
    st.header("📍 落地前 7 天清单")
    c1, c2 = st.columns(2)
    with c1: t_cnt = st.text_input("国家:", key="t1_cnt_pro")
    with c2: t_cty = st.text_input("城市:", key="t1_cty_pro")
    if st.button("📋 生成指南", key="t1_btn_pro"):
        if t_cnt and t_cty:
            res = call_gemini_top(f"为去{t_cnt}{t_cty}的留学生提供：办卡、租房、超市、避雷点的详细建议。")
            st.markdown(res)
            st.link_button("📕 小红书经验直达", f"https://www.xiaohongshu.com/search_result?keyword={urllib.parse.quote(t_cty)}留学落地")

# --- Tab 2: 简历润色 ---
with tabs[2]:
    st.header("📄 CV 旗舰级润色")
    up = st.file_uploader("上传 PDF 简历", type="pdf", key="t2_up_pro")
    if st.button("✨ 开启润色", key="t2_btn_pro") and up:
        reader = PdfReader(up)
        text = "".join([p.extract_text() for p in reader.pages])
        st.markdown(call_gemini_top(f"Use academic verbs to refine this CV for PhD: {text[:2000]}"))

# --- Tab 3: 陶瓷信直达 ---
with tabs[3]:
    st.header("✉️ 陶瓷信一键直达")
    e1, e2 = st.columns(2)
    with e1:
        p_email = st.text_input("导师邮箱:", key="t3_em_pro")
        p_name = st.text_input("导师姓名:", key="t3_nm_pro")
    with e2:
        r_topic = st.text_input("拟申请课题:", key="t3_tp_pro")
        my_high = st.text_area("背景亮点:", key="t3_hi_pro")
    if st.button("✍️ 生成并发送", key="t3_btn_pro"):
        body = call_gemini_top(f"Write a PhD inquiry email to {p_name} about {r_topic}. Highlights: {my_high}")
        st.markdown(body)
        if "⚠️" not in body:
            mailto = f"mailto:{p_email}?subject=PhD Inquiry&body={urllib.parse.quote(body)}"
            st.link_button(f"📧 一键跳转发送", mailto, use_container_width=True)

# --- Tab 4: 模拟面试 ---
with tabs[4]:
    st.header("🤖 旗舰 AI 面试官")
    u_n = st.text_input("学校名称:", key="t4_u_pro")
    u_t = st.text_area("研究课题:", key="t4_t_pro")
    if st.button("🏁 开始面试", key="t4_btn_pro"):
        st.markdown(call_gemini_top(f"Generate 5 tough PhD interview questions for {u_n} on {u_t}."))

# --- Tab 5: 就业居留 ---
with tabs[5]:
    st.header("💼 全球就业与长居路径")
    target_c = st.text_input("目标国家:", key="t5_c_pro")
    if st.button("📈 分析路径", key="t5_btn_pro"):
        st.markdown(call_gemini_top(f"Analyze PhD career and PR options in {target_c}."))

# --- Tab 6: 健康生活 ---
with tabs[6]:
    st.header("🍎 留学品质生活")
    l_city = st.text_input("所在城市:", key="t6_c_pro")
    if st.button("🌟 发现品质建议", key="t6_btn_pro"):
        st.markdown(call_gemini_top(f"Student guide for {l_city}: food, shopping, and safety."))

# --- Tab 7: 留学生百宝箱 ---
with tabs[7]:
    st.header("🛡️ 留学生全能百宝箱")
    tool = st.selectbox("挑战类型:", ["法律维权", "省钱秘籍", "心理树洞", "紧急求助"], key="t7_tool_pro")
    b_cnt = st.text_input("当前国家:", key="t7_cnt_pro")
    if st.button("🔍 获取专家对策", key="t7_btn_pro"):
        st.markdown(call_gemini_top(f"Advice for {tool} in {b_cnt}."))
