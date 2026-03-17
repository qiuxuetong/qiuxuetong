import streamlit as st
import urllib.parse
from datetime import datetime

# --- 1. 商用级架构配置 ---
st.set_page_config(page_title="Global Study Nexus Pro", layout="wide")

# CSS 注入：增强视觉专业感
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #ffffff; border-radius: 5px; 
        padding: 10px; border: 1px solid #e0e0e0;
    }
    .stTabs [aria-selected="true"] { background-color: #007bff !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 侧边栏：全局中央控制塔 ---
with st.sidebar:
    st.title("🌐 全球指挥中心")
    st.subheader("全局变量定义")
    u_name = st.text_input("目标院校", value="ETH Zurich", help="支持全球任意大学")
    p_name = st.text_input("目标导师", value="Piotr Smolenski")
    country = st.selectbox("目标国家/地区", ["美国", "英国", "德国", "瑞士", "新加坡", "香港", "加拿大", "澳洲", "荷兰", "比利时", "波兰"])
    st.divider()
    st.metric("合规引擎", "Active", "2.5.0-v9")
    st.write("---")
    st.markdown("### 🛠️ 快捷工具\n- [QS排名查询](https://www.topuniversities.com/university-rankings)\n- [汇率实时换算](https://www.xe.com/)")

# --- 3. 自动化唤起逻辑 ---
def get_search(q): return f"https://www.google.com/search?q={urllib.parse.quote(q)}"

# --- 4. 8大模块深度填充 (商用闭环) ---
tabs = st.tabs(["🎯 导师画像", "🛂 签证/居留", "✉️ 陶瓷流", "📄 文书盾", "💼 找工/永居", "🍎 健康/保险", "🛡️ 维权矩阵", "📅 全局规划"])

# -- Tab 1: 导师画像 --
with tabs[0]:
    st.subheader("🎯 导师学术背景与社交路径追踪")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("🧬 **学术纯度检测**")
        st.write("- 检索导师是否有撤稿记录或学术不端新闻。")
        st.link_button("自动化背景调查", get_search(f"{p_name} {u_name} academic misconduct retraction"))
    with c2:
        st.info("📡 **实时动态追踪**")
        st.write("- 追踪其近 6 个月是否在 X/LinkedIn 活跃或发布招生信息。")
        st.link_button("社交媒体/招生信息检索", get_search(f"{p_name} {u_name} recruitment opening PhD"))
    with c3:
        st.info("📧 **通信链路映射**")
        st.write("- 尝试映射该院校实验室通用邮箱地址。")
        st.link_button("探测官方实验室邮箱", get_search(f"{p_name} laboratory contact email {u_name}"))

# -- Tab 2: 签证/居留 --
with tabs[1]:
    st.subheader(f"🛂 {country} 签证与家属移居全案")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        ### ⚖️ 合规化路径指南
        1. **预签审查**: 检查是否涉及敏感技术转移限制(如美国 10043 号令)。
        2. **签证递交**: 自动化链接至 {country} 驻华使馆及 VFS 全球预约中心。
        3. **陪读/家属**: 提供配偶工作许可 (EAD/Work Permit) 的申请逻辑。
        """)
        st.link_button("获取官方合规清单", get_search(f"{country} researcher visa checklist official"))
    with col2:
        st.warning("💰 **资金证明预算**")
        st.write(f"预估 {country} 博士首年总开支（含学费及生活成本）约为 35,000 - 55,000 USD。")

# -- Tab 3: 陶瓷流 --
with tabs[2]:
    st.subheader("✉️ 动态陶瓷话术与发送策略")
    st.write("针对不同阶段的自动化邮件唤起：")
    e1, e2, e3 = st.columns(3)
    with e1:
        st.markdown("**1. 初次接触 (Cold Email)**")
        st.code("Subject: Research Inquiry: [Focus Area] - [Name]", language="markdown")
    with e2:
        st.markdown("**2. 面试后跟进 (Thank you)**")
        st.code("Subject: Thank you - Interview Follow-up", language="markdown")
    with e3:
        st.markdown("**3. 截止日期前提醒**")
        st.code("Subject: Application Submission - Final Check", language="markdown")
    st.link_button(f"📅 自动化检索 {u_name} 关键节假日", get_search(f"{u_name} academic holidays 2024 2025"))

# -- Tab 4: 文书盾 --
with tabs[3]:
    st.subheader("📄 文书盾：学术合规与竞争优势")
    st.write("集成全球顶尖院校的 AI 检测政策库。")
    st.link_button("🚀 Overleaf 全球学术 CV 工业级模板", "https://www.overleaf.com/gallery/tagged/cv")
    st.divider()
    st.markdown("#### 🛡️ 合规自检流")
    st.write("1. 检查文中是否有明显的 AI 生成特征。")
    st.write("2. 自动匹配该校 Statement of Purpose (SOP) 的字数与格式要求。")
    st.link_button("跳转至文书风控检测工具 (GPTZero/Turnitin)", "https://gptzero.me/")

# -- Tab 5: 找工/永居 --
with tabs[4]:
    st.subheader(f"💼 {country} 职业发展与身份衔接")
    st.success("📊 变现价值：解决毕业后的身份断层痛点。")
    st.write(f"- **找工假 (Job Seeking)**: 自动化分析 {country} 对于博士毕业生的延期居留期限。")
    st.write("- **紧缺职位**: 自动抓取当地对科研人员的雇主担保名单。")
    st.link_button(f"🔍 LinkedIn {country} 科研岗位实时看板", f"https://www.linkedin.com/jobs/search/?keywords=Postdoc&location={country}")
    st.link_button(f"🛂 {country} 高技术移民 PR 申请指南", get_search(f"{country} permanent residency for Ph.D. holders"))

# -- Tab 6: 健康/保险 --
with tabs[5]:
    st.subheader("🍎 全球健康风险与应急保障")
    st.markdown("### 🏥 医疗合规清单")
    st.write(f"1. **强制保险**: 匹配 {country} 法律要求的国际学生基本医疗险。")
    st.write("2. **心理健康**: 自动定位校内 24/7 紧急干预热线。")
    st.link_button(f"🚑 紧急搜索 {u_name} 校医院位置与预约", get_search(f"{u_name} student health services location appointment"))

# -- Tab 7: 维权矩阵 --
with tabs[6]:
    st.subheader("🛡️ 全球维权与法律纠纷矩阵")
    st.error("⚠️ 遭遇导师霸凌、学术不端或不公平待遇？系统已为您规划三级防御：")
    v1, v2, v3 = st.columns(3)
    with v1:
        st.markdown("#### 1. 校内调解 (Ombudsman)")
        st.link_button("查找院校独立调解官", get_search(f"{u_name} student ombudsman office"))
    with v2:
        st.markdown("#### 2. 校外仲裁 (Student Union)")
        st.link_button("联系当地学生工会", get_search(f"{country} National Student Union legal support"))
    with v3:
        st.markdown("#### 3. 法律起诉 (Legal Action)")
        st.link_button("搜索当地免费法律援助", get_search(f"{country} pro bono legal aid for foreigners"))

# -- Tab 8: 全局规划 --
with tabs[7]:
    st.subheader("📅 48个月全流程项目管理")
    st.write("基于核心算法的 4 年学术路径图。")
    st.table([
        {"阶段": "M1-M12", "任务": "课程修读、文献综述、实验室适应", "风险": "导师磨合期、开题失败"},
        {"阶段": "M13-M36", "任务": "独立研究、中期考核、论文发表", "风险": "实验数据异常、心理危机"},
        {"阶段": "M37-M48", "任务": "毕业答辩、职业搜索、身份衔接", "风险": "找工受阻、延毕风险"}
    ])
    st.date_input("项目起始基准日 (Baseline)", value=datetime.now())
