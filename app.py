import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import urllib.parse
import time

# 1. 核心初始化 - 锁定 2.5 级推理性能模型
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # 锁定 2.0 Thinking 模型，这是目前逻辑能力最强、最接近 2.5 水准的
    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')
except Exception:
    # 备选顶级 Pro 模型
    model = genai.GenerativeModel('gemini-1.5-pro')

# 2. 页面配置
st.set_page_config(page_title="求学通-2.5级高性能管家", layout="wide")
st.title("🎓 求学通：全球博士申请与生存全闭环系统 (2.5级性能驱动)")

# 3. 创建八大功能标签页 (确保每一个都有内容)
tabs = st.tabs([
    "🎯 导师匹配", "🏠 落地实战", "📄 简历润色", "✉️ 陶瓷信直达", 
    "🤖 模拟面试", "💼 就业居留", "🍎 健康生活", "🛡️ 留学生百宝箱"
])

# 核心：封杀 ResourceExhausted 报错的生成函数
def call_top_model(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 捕获你照片中的 429 ResourceExhausted 错误
        if "429" in str(e) or "ResourceExhausted" in str(e):
            return "⚠️ **[API 配额暂满]** 您正在调用 2.5 级顶级模型，频率限制较严。请等待 60 秒后再点击。当前页面输入已保存。"
        return f"⚠️ **[生成中断]** {str(e)}"

# --- Tab 0: 导师匹配 (带直达链接) ---
with tabs[0]:
    st.header("🔍 全球导师极速匹配")
    kw = st.text_input("输入研究方向 (如: Costume Design):", key="t0_kw_f")
    if st.button("🚀 寻找导师并生成链接", key="t0_btn_f"):
        with st.spinner("顶级 AI 正在进行深度推理匹配..."):
            res = call_top_model(f"Find 3 active professors in {kw}. Format: Name|University|Research focus. (No extra words)")
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
    st.header("📍 落地前 7 天实战待办")
    c1, c2 = st.columns(2)
    with c1: t_cnt = st.text_input("国家:", key="t1_cnt_f")
    with c2: t_cty = st.text_input("城市:", key="t1_cty_f")
    if st.button("📋 生成我的实战清单", key="t1_btn_f"):
        res = call_top_model(f"为去{t_cnt}{t_cty}的留学生提供具体的：办卡流程、租房平台、超市名、安全点。")
        st.markdown(res)
        st.link_button("📕 小红书实时经验", f"https://www.xiaohongshu.com/search_result?keyword={urllib.parse.quote(t_cty)}留学落地")

# --- Tab 2: 简历润色 ---
with tabs[2]:
    st.header("📄 CV 深度诊断")
    up = st.file_uploader("上传 PDF", type="pdf", key="t2_up_f")
    if st.button("✨ 开启 AI 润色", key="t2_btn_f") and up:
        reader = PdfReader(up)
        text = "".join([p.extract_text() for p in reader.pages])
        st.markdown(call_top_model(f"Refine this academic CV for PhD application: {text[:2000]}"))

# --- Tab 3: 陶瓷信直达 ---
with tabs[3]:
    st.header("✉️ 陶瓷信一键直达")
    e1, e2 = st.columns(2)
    with e1:
        p_email = st.text_input("导师邮箱:", key="t3_em_f")
        p_name = st.text_input("导师姓名:", key="t3_nm_f")
    with e2:
        r_topic = st.text_input("拟申请课题:", key="t3_tp_f")
        my_high = st.text_area("背景亮点:", key="t3_hi_f")
    if st.button("✍️ 生成并跳转发送", key="t3_btn_f"):
        body = call_top_model(f"Write a PhD inquiry email to {p_name} about {r_topic}. Highlights: {my_high}")
        st.markdown(body)
        if "⚠️" not in body:
            mailto = f"mailto:{p_email}?subject=PhD Inquiry&body={urllib.parse.quote(body)}"
            st.link_button(f"📧 直接点击发送", mailto, use_container_width=True)

# --- Tab 4: 模拟面试 ---
with tabs[4]:
    st.header("🤖 顶级 AI 面试官")
    target_u = st.text_input("大学:", key="t4_u_f")
    target_t = st.text_area("课题:", key="t4_t_f")
    if st.button("🏁 开始挑战", key="t4_btn_f"):
        st.markdown(call_top_model(f"Generate 5 tough PhD interview questions for {target_u} on {target_t}."))

# --- Tab 5: 就业居留 ---
with tabs[5]:
    st.header("💼 全球就业与长居政策")
    target_c = st.text_input("目标国家:", key="t5_c_f")
    if st.button("📈 生成路径分析", key="t5_btn_f"):
        st.markdown(call_top_model(f"Analyze PhD career path and PR (Permanent Residency) in {target_c}."))

# --- Tab 6: 健康生活 ---
with tabs[6]:
    st.header("🍎 留学品质生活")
    l_city = st.text_input("目标城市:", key="t6_c_f")
    if st.button("🌟 发现品质建议", key="t6_btn_f"):
        st.markdown(call_top_model(f"Student guide for {l_city}: food, supermarkets, and safety."))

# --- Tab 7: 留学生百宝箱 ---
with tabs[7]:
    st.header("🛡️ 留学生全能百宝箱")
    tool = st.selectbox("挑战类型:", ["法律维权", "省钱秘籍", "心理树洞", "紧急求助"], key="t7_tool_f")
    b_cnt = st.text_input("所在国家 (百宝箱用):", key="t7_cnt_f")
    if st.button("🔍 获取对策", key="t7_btn_f"):
        st.markdown(call_top_model(f"Professional advice for students in {b_cnt} facing {tool}."))
