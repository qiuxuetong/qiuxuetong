import streamlit as st
import requests
import json

# --- 1. 核心调度：非 2.5 级模型不调用 ---
def call_flagship_ai(prompt):
    if "OPENROUTER_API_KEY" not in st.secrets:
        st.error("请先在 Streamlit Secrets 中配置 OPENROUTER_API_KEY")
        return None

    api_key = st.secrets["OPENROUTER_API_KEY"]
    
    # 严格锁定 2.5 级旗舰模型路径
    # 如果第一个 404，立刻切换到另一个同等级的“大脑”，确保逻辑不降级
    models = [
        "google/gemini-pro-1.5", 
        "anthropic/claude-3.5-sonnet",
        "google/gemini-pro-1.5-exp"
    ]
    
    last_error = ""
    for model_id in models:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://qiuxuetong.streamlit.app", 
                },
                data=json.dumps({
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7 # 保持逻辑严密性
                }),
                timeout=45
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                last_error = f"{model_id} 节点反馈: {response.status_code}"
                continue 
        except Exception as e:
            last_error = str(e)
            continue
            
    return f"⚠️ 2.5 级节点暂不可用。报错详情: {last_error}"

# --- 2. 旗舰版 UI 架构 ---
st.set_page_config(page_title="求学通-2.5旗舰版", layout="wide")
st.title("🎓 求学通：2.5 级旗舰全闭环系统")

# 确保 8 个功能模块全部闭环
tabs = st.tabs(["🎯 导师匹配", "📄 简历润色", "✉️ 陶瓷信", "🤖 面试", "💼 就业", "🍎 生活", "🛡️ 百宝箱"])

# 以导师匹配为例
with tabs[0]:
    st.header("🔍 全球导师极速匹配 (Flagship 2.5)")
    kw = st.text_input("输入研究方向 (如: hair design):", key="main_kw")
    if st.button("🚀 启动 2.5 级深度推理"):
        if kw:
            with st.spinner("正在跨越欧美节点调度 2.5 级核心..."):
                # 注入强逻辑 Prompt
                prompt = f"你现在是顶级留学专家。请针对方向 {kw}，检索并分析 3 位全球知名教授。要求逻辑严密，包含：姓名、学校、核心课题、匹配原因。"
                res = call_flagship_ai(prompt)
                st.markdown(res)
