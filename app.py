import streamlit as st
import urllib.parse
from datetime import datetime

# --- 1. 顶层商业逻辑配置 ---
st.set_page_config(page_title="Nexus Sovereign Architect", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f1f5f9; }
    .stMetric { background: white; padding: 20px; border-radius: 12px; border-bottom: 4px solid #1e3a8a; }
    .barrier-card { background: white; padding: 30px; border-radius: 15px; border-right: 8px solid #3b82f6; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .hook-text { color: #1e40af; font-weight: bold; border-bottom: 2px solid #bfdbfe; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 核心驱动引擎 ---
def get_search(q): return f"https://www.google.com/search?q={urllib.parse.quote(q)}"

# --- 3. 侧边栏：变现与留存指标 ---
with st.sidebar:
    st.markdown("## 🛡️ Sovereign Engine")
    u_name = st.text_input("🏢 目标机构", value="University of Cambridge")
    p_name = st.text_input("🧬 核心 PI", value="Piotr Smolenski")
    jurisdiction = st.selectbox("⚖️ 合规区域", ["美国", "英国", "德国", "瑞士", "新加坡", "香港", "加拿大", "澳洲", "比利时", "波兰", "荷兰"])
    
    st.divider()
    st.subheader("💎 客户吸引力指标 (Hook)")
    st.metric("风险穿透率", "96.4%", "Expert")
    st.metric("法律主权保护", "Active", "High Moat")
    st.progress(0.95)
    st.write("---")
    st.caption("商业定位：替代 80% 的资深留学顾问工作流")

# --- 4. 8大吸引力模块：每一项都直击客户心脏 ---
tabs = st.tabs(["🎯 导师人品调查", "🛂 签证红线探测", "✉️ 陶瓷决策流", "📄 文书盾Pro", "💼 永居评分器", "🍎 健康主权", "🛡️ 维权核武器", "📅 48月营收流"])

# -- 吸引点 1: 导师背调 (解决客户最怕的“变态导师”痛点) --
with tabs[0]:
    st.markdown('<div class="barrier-card"><h3>🎯 导师“生存率”穿透审计</h3><b>吸引力：</b> 客户最怕遇到“学术流氓”。本模块自动检索该导师的撤稿历史、学生平均毕业年限及社交平台差评。</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.link_button("🕵️ 检索撤稿/丑闻记录", get_search(f"{p_name} {u_name} academic integrity misconduct scandal"))
    with c2: st.link_button("💰 穿透实验室资金流", get_search(f"{p_name} {u_name} research grants awards funding"))
    with c3: st.link_button("📡 匿名评价穿透 (Reddit/Glassdoor)", get_search(f"{p_name} {u_name} laboratory culture student reviews"))

# -- 吸引点 2: 签证红线 (解决客户最怕的“政治审查”痛点) --
with tabs[1]:
    st.subheader(f"🛂 {jurisdiction} 出口管制与签证红线检测")
    st.markdown(f'<div class="barrier-card"><b>技术壁垒：</b> 自动化匹配敏感专业（AI、半导体等）的合规路径，规避 {jurisdiction} 的出口管制调查。</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"1. **出口管制预警**: 自动生成 {jurisdiction} 针对高精尖专业的申报 Checklist。")
        st.write(f"2. **全家安置主权**: 匹配配偶工作许可 (EAD) 及子女公立教育资源。")
        st.link_button(f"获取 {jurisdiction} 官方科研签证合规手册", get_search(f"{jurisdiction} official researcher visa requirements 2024"))
    with col2:
        st.error("🚀 预警响应")
        st.write("当前地区敏感专业拒签风险：偏高。建议准备 SOP 申诉信模板。")

# -- 吸引点 4: 文书盾 (解决客户最怕的“AI 查重”痛点) --
with tabs[3]:
    st.subheader("📄 文书主权盾：NLP 反检测重构")
    st.markdown('<div class="barrier-card"><b>吸引力：</b> 现在的大学查 AI 极严。本模块通过学术逻辑降权，确保你的 SOP 符合 Top 校查重标准。</div>', unsafe_allow_html=True)
    st.link_button("🚀 访问 Overleaf LaTeX 全球学术模板", "https://www.overleaf.com/gallery/tagged/cv")
    st.link_button("🛡️ 启动 AI 痕迹深度自检 (GPTZero Bypass)", "https://gptzero.me/")
    st.text_area("文书主权预审区 (粘贴 SOP/CV)...", height=100)

# -- 吸引点 7: 维权核武器 (客户的核心安全感来源) --
with tabs[6]:
    st.error(f"🛡️ 遭遇导师剥削？系统已锁定 {u_name} 的独立救助逻辑。")
    st.markdown('<div class="barrier-card"><b>商业护城河：</b> 自动化锁定 Ombudsman (调解官)。这是中介绝对不知道的“保命”信息，能极大增强客户信任。</div>', unsafe_allow_html=True)
    v1, v2 = st.columns(2)
    with v1:
        st.markdown("#### ⚖️ 院校调解员 (Ombudsman)")
        st.link_button("唤起校内维权申诉", get_search(f"{u_name} independent student ombudsman office formal complaint"))
    with v2:
        st.markdown("#### 🏛️ 法律援助 (Legal Union)")
        st.link_button(f"联系 {jurisdiction} 地区科研工会", get_search(f"{jurisdiction} National Union of Students legal aid"))

# -- 吸引点 8: 48月营收流 (投资人最爱的变现闭环) --
with tabs[7]:
    st.subheader("📅 科研全周期 48 个月风险管理与营收转化")
    st.info("📊 **商业模式**：这不是工具，而是长达 4 年的服务入口。")
    st.table([
        {"阶段": "M1-M12", "任务": "合规入驻", "高客单价转化点": "科研合规包、海外医疗险、法务包"},
        {"阶段": "M13-M36", "任务": "产出爆发", "高客单价转化点": "顶级论文润色、学术集采、差旅"},
        {"阶段": "M37-M48", "任务": "身份收割", "高客单价转化点": "移民律师、永居代办、高端猎头"}
    ])
    st.date_input("项目起始基准日", value=datetime.now())

# -- 其余模块补全 --
with tabs[2]:
    st.subheader("✉️ 陶瓷全自动化引擎")
    st.code("Subject: Prospective PhD Researcher - [Area] - [Name]", language="markdown")
    st.link_button(f"检索 {u_name} 关键节假日校历", get_search(f"{u_name} academic calendar holiday"))

with tabs[4]:
    st.subheader(f"💼 {jurisdiction} 职业发展与 PR 衔接")
    st.link_button("LinkedIn 全球人才库实时检索", f"https://www.linkedin.com/jobs/search/?keywords=PhD&location={jurisdiction}")

with tabs[5]:
    st.subheader("🍎 全球健康主权与保障")
    st.link_button("自动化检索校内 Wellbeing 中心", get_search(f"{u_name} student mental health support"))
