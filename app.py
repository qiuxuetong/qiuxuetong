import streamlit as st
import requests
import json

# 1. 核心：只调度 2.5 级旗舰大脑
def call_2_5_flagship(prompt):
    api_key = st.secrets["OPENROUTER_API_KEY"]
    
    # 既然充钱了，我们直接用目前逻辑最稳、深度最强的 ID
    # 第一个是 Claude 3.5 (逻辑天花板)，第二个是 Gemini 1.5 Pro (全能旗舰)
    models = [
        "anthropic/claude-3.5-sonnet", 
        "google/gemini-pro-1.5"
    ]
    
    for model_id in models:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "https://qiuxuetong.streamlit.app", 
                    "Content-Type": "application/json"
                },
                data=json.dumps({
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.5 # 降低随机性，提高逻辑严密性
                }),
                timeout=50
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except:
            continue
    return "⚠️ 商业节点响应超时，请刷新网页重试。"

# 2. 旗舰版全闭环 UI
st.title("🎓 求学通：Flagship 2.5 博士全闭环系统")
tabs = st.tabs(["🎯 导师匹配", "📄 简历润色", "✉️ 陶瓷信", "🤖 面试", "💼 就业", "🍎 生活", "🛡️ 百宝箱"])

with tabs[0]:
    st.header("🔍 全球导师深度匹配")
    kw = st.text_input("输入研究方向 (如: Medical Image Analysis):")
    if st.button("🚀 启动 2.5 级深度检索"):
        with st.spinner("正在通过付费商业节点进行深度推理..."):
            # 这里的 Prompt 已经过 2.5 级优化
            res = call_2_5_flagship(f"作为资深教授，请针对方向 {kw} 匹配 3 位全球顶级导师。要求：分析其近期研究逻辑，并给出具体的匹配建议。")
            st.markdown(res)
