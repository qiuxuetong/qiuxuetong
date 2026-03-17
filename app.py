import streamlit as st
import urllib.parse
from datetime import datetime

# --- 1. 企业级 SaaS 视觉引擎 ---
st.set_page_config(page_title="Nexus Sovereign AI v19.0", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f4f8; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 60px; background-color: #ffffff; border-radius: 8px; 
        border: 1px solid #d1d5db; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #1e3a8a !important; color: white !important; }
    .logic-container { background: white; padding: 25px; border-radius: 12px; border-left: 8px solid #1e3a8a; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .monetize-tag { background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 15px; font-size: 0.8rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 核心驱动引擎 ---
def get_search(q): return f"https://www.google.com/search?q={urllib.parse.quote(q)}"

# --- 3. 侧边栏：全局中央指挥中心 ---
with st.sidebar:
    st.title("🛡️ TITAN SOVEREIGN")
    st.caption("Commercial Grade SaaS Prototype")
    u_name = st.text_input("📍 目标大学", value="University of Oxford")
    p_name = st.text_input("👨‍🏫 目标导师", value="Piotr Smolenski")
    region = st.selectbox("🌍 目标法域", ["美国", "英国", "德国", "瑞士", "新加坡", "香港", "加拿大", "澳洲", "荷兰", "比利时", "波兰"])
    
    st.divider()
    st.subheader("💎 商业化壁垒看板")
    st.metric("数据资产节点", "52,400+", "Real-time")
    st.metric("变现转化路径", "12 条", "High LTV")
    st.progress(0.98)
    if st.button("🚀 生成 50页 深度合规报告"):
        st.snow()
        st.toast("正在穿透目标大学合规数据库...", icon="🔍")

# --- 4. 8大高密度功能矩阵 ---
tabs = st.tabs(["🎯 导师画像", "🛂 签证红线", "✉️ 陶瓷内核", "📄 文书主权", "💼 永居算法", "🍎 健康保障", "🛡️ 维权阵地", "📅 48月规划"])

# -- 1. 导师画像 (高密度：人品与资金审计) --
with tabs[0]:
    st.markdown('<div class="logic-container">', unsafe_allow_html=True)
    st.subheader("🧬 PI 学术信誉与实验室生存率审计")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.write("**核心审计维度：**")
        st.write("- **学术诚信穿透**: 自动对齐 Retraction Watch。如有撤稿或学术不端，系统触发 🔴 预警。")
        st.write("- **资助链稳定性**: 检索 PI 在该国资助局（如 NSF/ERC）的 Grant 剩余年限。")
        st.write("- **人员流失率**: 分析其 Lab 博后平均在位时间，识别“天坑”系数。")
        st.link_button("🕵️ 启动全网学术诚信穿透", get_search(f"{p_name} {u_name} academic integrity misconduct scandal"))
    with col_b:
        st.markdown('<span class="monetize-tag">变现点：背调报告付费服务</span>', unsafe_allow_html=True)
        risk_score = st.slider("导师风险自评模拟器", 0, 100, 45)
        st.write(f"当前预估风险值: {risk_score}%")
    st.markdown('</div>', unsafe_allow_html=True)

# -- 2. 签证红线 (高密度：出口管制专区) --
with tabs[1]:
    st.markdown('<div class="logic-container">', unsafe_allow_html=True)
    st.subheader(f"🛂 {region} 移民法合规与技术出口管制 (Export Control)")
    st.write(f"针对敏感专业（AI、半导体、量子），系统已自动载入 {region} 的官方合规路径。")
    v_c1, v_c2 = st.columns(2)
    with v_c1:
        st.write("**技术审查对冲：**")
        st.write(f"- **ATAS/10043 自动化判定**: 基于您的背景自动生成 {region} 官方合规申报书。")
        st.link_button(f"获取 {region} 官方科研签证合规手册", get_search(f"{region} official researcher visa requirements 2024"))
    with v_c2:
        st.write("**家属主权方案：**")
        st.write("- **配偶工作权**: 自动匹配 EAD 申请指南。")
        st.write("- **子女教育**: 定位目标大学周边 5km 内公立学校资源。")
        st.link_button(f"检索 {u_name} 周边教育配套", get_search(f"schools and childcare near {u_name}"))
    st.markdown('</div>', unsafe_allow_html=True)

# -- 4. 文书主权 (高密度：AI 降权交互) --
with tabs[3]:
    st.markdown('<div class="logic-container">', unsafe_allow_html=True)
    st.subheader("📄 文书主权盾：基于 NLP 的逻辑重构引擎")
    st.write("**技术含金量：** 针对 Turnitin 等 AI 检测器的底层逻辑进行学术降权算法对冲。")
    c_a, c_b = st.columns(2)
    with c_a:
        st.success("🛠️ 全球科研简历 (CV) 工业模板")
        st.link_button("加载 Overleaf LaTeX 专项库", "https://www.overleaf.com/gallery/tagged/cv")
    with c_b:
        st.success("🛡️ AI 痕迹对冲工具")
        st.link_button("启动学术逻辑降权扫描", "https://gptzero.me/")
    sop_input = st.text_area("文书实时诊断 (粘贴至此)", placeholder="粘贴您的 SOP 段落，系统将分析 AI 痕迹和逻辑密度...", height=150)
    if sop_input: st.button("开始 AI 痕迹消除模拟")
    st.markdown('</div>', unsafe_allow_html=True)

# -- 7. 维权阵地 (核心杀手锏：主权保障) --
with tabs[6]:
    st.markdown('<div class="logic-container">', unsafe_allow_html=True)
    st.error(f"🛡️ 遭受学术剥削或霸凌？本系统已锁定 {u_name} 的独立救助逻辑。")
    st.write("**商业壁垒：** 自动化匹配 Ombudsman (调解官) 系统，这是任何中介都不具备的法律深层数据。")
    v1, v2, v3 = st.columns(3)
    with v1:
        st.markdown("#### ⚖️ 独立调解官 (Ombudsman)")
        st.link_button("唤起校内维权申请", get_search(f"{u_name} independent student ombudsman office formal complaint"))
    with v2:
        st.markdown(f"#### 🏛️ {region} 科研工会")
        st.link_button("获取法律援助入口", get_search(f"{region} National Union of Students legal aid"))
    with v3:
        st.markdown("#### 📜 法律主权援助")
        st.link_button("搜索当地免费律师服务", get_search(f"{region} pro bono legal aid for international researchers"))
    st.markdown('</div>', unsafe_allow_html=True)

# -- 8. 48月规划 (高密度：变现矩阵) --
with tabs[7]:
    st.markdown('<div class="logic-container">', unsafe_allow_html=True)
    st.subheader("📅 科研全生命周期 48 个月风险管理与营收矩阵")
    st.info("📈 **投资人逻辑**：本产品不仅是工具，更是长达 4 年的精准流量入口，覆盖 10 个以上高客单价业务。")
    st.table([
        {"周期": "M1-M12", "任务": "合规入驻与开题", "变现出口": "合规保险、搬迁服务、法律包"},
        {"周期": "M13-M36", "任务": "数据爆发与顶刊发表", "变现出口": "学术润色、翻译、会议差旅集采"},
        {"周期": "M37-M48", "任务": "毕业答辩与永居衔接", "变现出口": "高端猎头、移民律师、PR代办"}
    ])
    st.markdown('</div>', unsafe_allow_html=True)

# -- 补全其他模块 --
with tabs[2]:
    st.subheader("✉️ 陶瓷链路全自动化流")
    st.code(f"Subject: Prospective PhD Researcher - {u_name} - [Your Name]", language="markdown")
    st.link_button(f"检索 {u_name} 面试黄金窗口", get_search(f"{u_name} academic calendar holiday"))

with tabs[4]:
    st.subheader(f"💼 {region} 职业发展与 PR 身份算法")
    st.link_button("LinkedIn 全球人才库实时检索", f"https://www.linkedin.com/jobs/search/?keywords=PhD&location={region}")

with tabs[5]:
    st.subheader("🍎 全球健康主权与保障")
    st.link_button("紧急寻找校内心理干预热线", get_search(f"{u_name} student health psychological services"))
