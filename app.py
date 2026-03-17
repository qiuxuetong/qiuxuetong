import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import urllib.parse

# 1. 核心初始化 - 使用最稳定的旗舰模型标识符
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # 使用 -latest 后缀通常能解决 v1beta 版本下的 404 找不到模型问题
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
except Exception as e:
    st.error(f"初始化失败: {e}")

# 2. 页面配置
st.set_page_config(page_title="求学通-2.5旗舰系统", layout="wide")
st.title("🎓 求学通：博士申请与生存全闭环系统 (Flagship 2.5)")

# 3. 创建八大功能标签页 (全功能完全对齐)
tabs = st.tabs([
    "🎯 导师匹配", "🏠 落地实战", "📄 简历润色", "✉️ 陶瓷信直达", 
    "🤖 模拟面试", "💼 就业居留", "🍎 健康生活", "🛡️ 留学生百宝箱"
])

# AI 调用封装：解决 ResourceExhausted 和 404 崩溃
def call_top_ai(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        err = str(e)
        if "429" in err or "ResourceExhausted" in err:
            return "⚠️ [配额限制] 您正在使用 2.5 级顶级模型，请等 60 秒后再点击，输入已保存。"
        if "404" in err:
            return "⚠️ [路径错误] 当前模型接口调整中，请检查 API Key 权限。"
        return f"⚠️ [生成中断] {err}"

# --- Tab 0: 导师匹配 ---
with tabs[0]:
    st.header("🔍 全球导师极速匹配")
    kw = st.text_input("输入研究方向 (如: costume design):", key="t0_kw_f")
    if st.button("🚀 寻找导师并生成链接", key="t0_btn_f"):
        with st.spinner("顶级 AI 正在分析全球库..."):
            res = call_top_ai(f"Find 3 professors in {kw}. Format: Name|University|Research. (No extra text)")
            if "⚠️" not in res:
                for line in res.strip().split('\n'):
                    if '|' in line:
                        n, u, r = line.split('|')
                        st.subheader(f"👨‍🏫 {n.strip()}")
                        st.write(f"🏫 **学校**: {u.strip()}  |  🔬 **方向**: {r.strip()}")
                        q = urllib.parse.quote(f"{n.strip()} {u.strip()}")
                        c1, c2 = st.columns(2)
                        c1.link_button("🔍 Google Scholar", f"https://scholar.google.com/scholar?q={q}")
                        c2.link_button("🌐 大学官网", f"https://www.google.com/search?q={q}+official+page")
                        st.divider()
            else: st.warning(res)

# --- Tab 1: 落地实战 ---
with tabs[1]:
    st.header("📍 落地前 7 天清单")
    c1, c2 = st.columns(2)
    with c1: t_cnt = st.text_input("国家:", key="t1_cnt_f")
    with c2: t_cty = st.text_input("城市:", key="t1_cty_f")
    if st.button("📋 生成清单", key="t1_btn_f"):
        st.markdown(call_top_ai(f"为去{t_cnt}{t_cty}的留学生提供：办卡、租房、超市、避雷点。"))

# --- Tab 2: 简历润色 ---
with tabs[2]:
    st.header("📄 CV 旗舰润色")
    up = st.file_uploader("上传 PDF", type="pdf", key="t2_up_f")
    if st.button("✨ 开启润色", key="t2_btn_f") and up:
        reader = PdfReader(up)
        text = "".join([p.extract_text() for p in reader.pages])
        st.markdown(call_top_ai(f"Refine this CV with academic verbs: {text[:2000]}"))

# --- Tab 3: 陶瓷信直达 ---
with tabs[3]:
    st.header("✉️ 陶瓷信一键直达")
    e1, e2 = st.columns(2)
    with e1:
        p_email = st.text_input("导师邮箱:", key="t3_em_f")
        p_name = st.text_input("导师姓名:", key="t3_nm_f")
    with e2:
        r_topic = st.text_input("申请课题:", key="t3_tp_f")
        my_high = st.text_area("背景亮点:", key="t3_hi_f")
    if st.button("✍️ 生成并发送", key="t3_btn_f"):
        body = call_top_ai(f"Write PhD Inquiry to {p_name} about {r_topic}. Highlights: {my_high}")
        st.markdown(body)
        if "⚠️" not in body:
            mailto = f"mailto:{p_email}?subject=Inquiry&body={urllib.parse.quote(body)}"
            st.link_button(f"📧 跳转发送", mailto, use_container_width=True)

# --- 其余 4 个 Tab 补全 ---
with tabs[4]:
    st.header("🤖 模拟面试")
    if st.button("🏁 生成面试题", key="t4_btn"):
        st.markdown(call_top_ai("Generate 5 tough PhD interview questions."))

with tabs[5]:
    st.header("💼 就业居留")
    tc = st.text_input("国家:", key="t5_c")
    if st.button("📈 分析路径", key="t5_btn"):
        st.markdown(call_top_ai(f"Analyze PhD career and PR path in {tc}."))

with tabs[6]:
    st.header("🍎 健康生活")
    lc = st.text_input("城市:", key="t6_c")
    if st.button("🌟 生活建议", key="t6_btn"):
        st.markdown(call_top_ai(f"Lifestyle guide for students in {lc}."))

with tabs[7]:
    st.header("🛡️ 百宝箱")
    tool = st.selectbox("类型:", ["法律", "省钱", "心理", "求助"], key="t7_tool")
    if st.button("🔍 获取对策", key="t7_btn"):
        st.markdown(call_top_ai(f"Advice for {tool}."))
