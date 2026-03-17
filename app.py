import streamlit as st
import requests
import json

# --- 1. 配置与核心引擎 ---
st.set_page_config(page_title="求学通-Flagship 2.5", layout="wide")

def call_ai(prompt):
    api_key = st.secrets["OPENROUTER_API_KEY"]
    # 付费用户锁死最强两个模型：Claude 3.5 Sonnet 和 Gemini 1.5 Pro
    models = ["anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5"]
    for model in models:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                data=json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.4}),
                timeout=60
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except: continue
    return "❌ 节点繁忙，请重试。"

# --- 2. UI 界面与 8 大细致模块 ---
st.title("🎓 求学通：Flagship 2.5 博士申请全闭环系统")
st.caption("当前状态：商业级 Paid Tier 已激活 | 逻辑等级：2.5 级旗舰")

tabs = st.tabs(["🎯 导师匹配", "📄 简历润色", "✉️ 陶瓷信", "🤖 模拟面试", "💼 就业居留", "🍎 生活健康", "🛡️ 申博保障", "🏗️ 项目规划"])

# --- 模块 1: 导师匹配 ---
with tabs[0]:
    st.subheader("🔍 深度学术画像与导师匹配")
    research = st.text_input("输入你的细分研究方向:", placeholder="例如: Medical Image Analysis using Diffusion Models")
    if st.button("启动 2.5 级检索"):
        prompt = f"针对方向 {research}，请列出3位全球顶级教授。要求：1.分析其近3年核心研究逻辑；2.提供具体的‘套磁切入点’；3.给出申请建议。"
        with st.spinner("正在检索商业数据库..."):
            st.markdown(call_ai(prompt))

# --- 模块 2: 简历润色 ---
with tabs[1]:
    st.subheader("📄 2.5 级科研简历重构")
    cv_text = st.text_area("粘贴你的简历片段:")
    if st.button("进行逻辑重构"):
        prompt = f"请用 STAR 法则重构以下简历内容。要求：逻辑严密，突出独立解决问题的能力，使用强有力的动词，符合 2.5 级学术审美。\n{cv_text}"
        st.markdown(call_ai(prompt))

# --- 模块 3: 陶瓷信 ---
with tabs[2]:
    st.subheader("✉️ 极高回复率陶瓷信生成")
    prof_info = st.text_input("输入导师姓名或最近的一篇论文标题:")
    if st.button("生成深度陶瓷信"):
        prompt = f"基于导师信息 {prof_info}，撰写一封陶瓷信。要求：第一段直接切入学术痛点，第二段展示我如何能解决他的课题，拒绝套话。"
        st.markdown(call_ai(prompt))

# --- 模块 4: 模拟面试 ---
with tabs[3]:
    st.subheader("🤖 2.5 级 AI 博士面试官")
    if st.button("开始压力面试测试"):
        prompt = "请模拟一位严厉的欧洲博士面试官，针对我的研究计划提出三个具有挑战性的学术问题，并解释这些问题背后的逻辑。"
        st.markdown(call_ai(prompt))

# --- 模块 5: 就业居留 ---
with tabs[4]:
    st.subheader("💼 比利时/欧洲就业与居留咨询")
    job_q = st.text_input("输入你想了解的政策（如：比利时求职签，荷兰高技术移民）:")
    if st.button("获取深度政策分析"):
        prompt = f"请详细分析针对中国博士生在 {job_q} 的居留政策。要求：包含时间线、关键门槛和避坑指南。"
        st.markdown(call_ai(prompt))

# --- 模块 6: 生活健康 ---
with tabs[5]:
    st.subheader("🍎 博士心理健康与生活助手")
    if st.button("获取压力应对方案"):
        prompt = "作为博士心理专家，请针对学术压力（Burnout）提供一套基于认知行为疗法的自我调节方案，并推荐3个在欧洲生活的解压方式。"
        st.markdown(call_ai(prompt))

# --- 模块 7: 申博保障 ---
with tabs[6]:
    st.subheader("🛡️ 博士申请避坑与法律保障")
    if st.button("获取避坑指南"):
        prompt = "列举在欧洲（尤其是比利时）申请博士时可能遇到的3大法律或行政陷阱，例如合同细节、知识产权归属等。"
        st.markdown(call_ai(prompt))

# --- 模块 8: 项目规划 ---
with tabs[7]:
    st.subheader("🏗️ 4年博士项目全周期规划")
    if st.button("生成 48 个月规划图"):
        prompt = "请详细规划一份 48 个月的博士研究时间轴。包含：选题期、数据采集期、论文产出期、论文提交与答辩期。每阶段要有 KPI。"
        st.markdown(call_ai(prompt))
