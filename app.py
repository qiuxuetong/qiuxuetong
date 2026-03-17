import streamlit as st
import urllib.parse
from datetime import datetime

# --- 1. 基础工具 ---
def get_search(q): return f"https://www.google.com/search?q={urllib.parse.quote(q)}"

st.set_page_config(page_title="全球求学通 5.0", layout="wide")
st.title("🎓 全球求学通：Flagship 5.0 终极全填充系统")
st.info("✅ 状态：8项内容强制预加载 | 拒绝空置 | 自动唤起已就绪")

# --- 2. 核心 8 大模块 (强制渲染，绝不留空) ---
tabs = st.tabs([
    "🎯 导师/官网/邮箱", "🛂 居留/签证/全家", "✉️ 陶瓷/邮件唤起", 
    "📄 文书/简历/防AI", "💼 找工/永居/身份", "🍎 健康/心理/保险", 
    "🛡️ 法律/维权/举报", "📅 48月全程规划"
])

# 模块 1: 导师/官网
with tabs[0]:
    st.subheader("🎯 全球导师与官网全自动追踪")
    u_name = st.text_input("大学名:", value="University of Wrocław")
    p_name = st.text_input("教授名:", value="Piotr Smoleński")
    st.success(f"📍 目标锁定：{p_name} (化学系专家)")
    st.markdown("### ✨ 自动化工具")
    st.link_button(f"🌐 访问 {u_name} 教职名单", get_search(f"{p_name} {u_name} staff"))
    st.link_button(f"📧 探测官方联系邮箱", get_search(f"{p_name} {u_name} email"))

# 模块 2: 居留/签证 (强制显示政策)
with tabs[1]:
    st.subheader("🛂 全球居留与签证方案")
    country = st.selectbox("选择目标国家:", ["波兰🇵🇱", "比利时🇧🇪", "德国🇩🇪", "美国🇺🇸", "英国🇬🇧"])
    st.markdown(f"### 🛡️ {country} 办证干货")
    st.write("- **办证逻辑**: 博士录取后即可办理 D 类学生签，抵达后换领居留卡(TRC)。")
    st.write("- **全家政策**: 博士通常支持家属陪读并享有合法工作权。")
    st.link_button("📜 查看该国官方签证指南", get_search(f"{country} student visa requirements"))

# 模块 3: 陶瓷/邮件 (预置模板)
with tabs[2]:
    st.subheader("✉️ 陶瓷邮件模板与发送")
    st.info("💡 这是一个标准的学术陶瓷模板，复制即可使用：")
    st.code("Dear Professor [Name], I am highly interested in your research on [Topic]...")
    st.link_button("📅 查询该校当前放假安排", get_search(f"{u_name} academic calendar"))

# 模块 4: 文书/简历 (强制显示工具)
with tabs[3]:
    st.subheader("📄 文书、简历与防 AI 检测")
    st.markdown("### 🛠️ 必备工具链")
    st.link_button("🚀 Overleaf 学术简历模板", "https://www.overleaf.com/gallery/tagged/cv")
    st.link_button("🛡️ 文本 AI 率检测 (GPTZero)", "https://gptzero.me/")
    st.text_area("在此粘贴您的文书内容进行自检...", height=100)

# 模块 5: 找工/永居 (解决图片 53e9a807 的空置)
with tabs[4]:
    st.subheader("💼 全球找工与永居身份")
    st.success("📊 预载数据：波兰、比利时、德国等国均提供 12-18 个月找工假。")
    st.link_button(f"🔍 搜查 {country} 博士职位 (LinkedIn)", f"https://www.linkedin.com/jobs/search/?keywords=PhD&location={country}")

# 模块 6: 健康/心理 (强制填充)
with tabs[5]:
    st.subheader("🍎 健康、心理与学生保险")
    st.markdown("### 🏥 紧急救助指南")
    st.write("1. **保险**: 抵达后请立即办理当地公费医保 (如波兰 NFZ)。")
    st.write("2. **心理**: 大多数大学提供免费的心理咨询 (Psychological Counselling)。")
    st.link_button("🆘 搜索该大学心理健康服务", get_search(f"{u_name} student mental health support"))

# 模块 7: 法律/维权 (解决图片 21a82d8d 的空置)
with tabs[6]:
    st.subheader("🛡️ 法律、维权与举报渠道")
    st.error("⚠️ 遭遇霸凌、学术不端或导师剥削？不要沉默。")
    st.link_button(f"⚖️ 自动搜索 {u_name} 的 Ombudsman (调解员)", get_search(f"{u_name} ombudsman"))
    st.write("💡 Ombudsman 是专门保护学生、处理导生矛盾的独立机构。")

# 模块 8: 48月规划 (修复报错逻辑)
with tabs[7]:
    st.subheader("📅 博士 48 个月全周期避坑规划")
    st.info("🗓️ 博士生涯关键节点：")
    st.write("- **0-12月**: 确定选题，完成文献综述。")
    st.write("- **13-36月**: 实验/调研，发表核心期刊论文。")
    st.write("- **37-48月**: 论文撰写，答辩准备，找工/博后申请。")
    s_date = st.date_input("预计起始日期", value=datetime.now())
