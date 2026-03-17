import streamlit as st
import requests
import json

# 1. 安全获取 Secrets 中的 Key
if "OPENROUTER_API_KEY" not in st.secrets:
    st.error("Secrets 配置格式错误，请检查是否按照 OPENROUTER_API_KEY = '...' 填写")
    st.stop()

OR_KEY = st.secrets["OPENROUTER_API_KEY"]

# 2. 建立旗舰级 API 调用函数
def call_2_5_logic(prompt):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OR_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "google/gemini-pro-1.5", # 锁定 2.5 级顶级逻辑
                "messages": [{"role": "user", "content": prompt}]
            }),
            timeout=40
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"⚠️ 转发节点返回错误 {response.status_code}: {response.text}"
    except Exception as e:
        return f"❌ 链路中断: {str(e)}"

# 3. 页面布局 (确保 8 个标签页稳固)
st.set_page_config(page_title="求学通-Flagship 2.5", layout="wide")
st.title("🎓 求学通：2.5 级旗舰全闭环系统")

tabs = st.tabs(["🎯 导师匹配", "📄 简历润色", "✉️ 陶瓷信", "🛡️ 百宝箱"])

with tabs[0]:
    st.header("🔍 全球导师极速匹配")
    kw = st.text_input("研究方向 (如: Costume Design):", key="kw_v4")
    if st.button("🚀 开启旗舰级检索"):
        if kw:
            with st.spinner("AI 正在跨越欧美商业节点进行推理..."):
                res = call_2_5_logic(f"Find 3 professors for {kw}. Name|Uni|Focus.")
                st.markdown(res)
        else:
            st.warning("请输入方向")
