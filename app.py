import streamlit as st
import requests
import json

# 1. 核心调用逻辑
def call_stable_ai(prompt):
    api_key = st.secrets["OPENROUTER_API_KEY"]
    
    # 依次尝试的模型列表（2.5级旗舰逻辑）
    models_to_try = [
        "google/gemini-pro-1.5", 
        "google/gemini-pro-1.5-exp",
        "anthropic/claude-3-sonnet"
    ]
    
    for model_id in models_to_try:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                data=json.dumps({
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}]
                }),
                timeout=30
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except:
            continue # 如果第一个模型 404，自动尝试下一个
            
    return "⚠️ 节点暂时忙碌。请确保 OpenRouter 账户有微量额度（如 $1），或稍后再试。"

# 2. UI 保持不变
st.title("🎓 求学通：2.5 级旗舰全闭环系统")
kw = st.text_input("研究方向 (如: hair design):", key="v5")

if st.button("🚀 开启旗舰级检索"):
    if kw:
        with st.spinner("正在通过全球高权重节点检索..."):
            res = call_stable_ai(f"请匹配关于 {kw} 的 3 位教授。格式：姓名|学校|研究方向")
            st.markdown(res)
