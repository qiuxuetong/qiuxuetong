import streamlit as st
import urllib.parse
from datetime import datetime

# --- 核心工具：自动化搜索引擎 ---
def get_search(q): return f"https://www.google.com/search?q={urllib.parse.quote(q)}"

st.set_page_config(page_title="全球求学通 7.0", layout="wide")
st.title("🎓 全球求学通：Flagship 7.0 全球自由定义版")
st.info("🌍 状态：已解除地域锁定 | 8大模块深度填充 | 全自动化唤起")

# 让用户自主定义目标
col_u, col_p, col_c = st.columns(3)
with col_u:
    u_name = st.text_input("1. 目标大学全名 (例如: ETH Zurich):", placeholder="请输入全球任意大学")
with col_p:
    p_name = st.text_input("2. 目标教授姓名:", placeholder="请输入教授姓名")
with col_c:
    target_country = st.selectbox("3. 目标国家/地区:", ["美国🇺🇸", "英国🇬🇧", "德国🇩🇪", "加拿大🇨🇦", "澳洲🇦🇺", "新加坡🇸🇬", "瑞士🇨🇭", "荷兰🇳🇱", "比利时🇧🇪", "波兰🇵🇱", "日本🇯🇵", "香港🇭🇰"])

# 定义 8 大核心标签
tabs = st.tabs([
    "🎯 导师/官网/邮箱", "🛂 居留/签证/全家", "✉️ 陶瓷/邮件唤起", 
    "📄 文书/简历/防AI", "💼 找工/永居/身份", "🍎 健康/心理/保险", 
    "🛡️ 法律/维权/举报", "📅 48月全程规划"
])

# --- 1. 导师/官网 (完全动态) ---
with tabs[0]:
    st.subheader("🎯 导师主页与官方信息追踪")
    if u_name and p_name:
        st.success(f"已生成针对 {u_name} - {p_name} 的专项检索")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**官方路径**")
            st.link_button("🌐 直达教职员/教授主页", get_search(f"{p_name} {u_name} official staff page profile"))
        with c2:
            st.markdown("**通讯录检索**")
            st.link_button("📧 查找官方办公邮箱", get_search(f"{p_name} {u_name} university email address contact"))
        with c3:
            st.markdown("**学术成果**")
            st.link_button("📚 查看最新研究论文", f"https://scholar.google.com/scholar?q={p_name}+{u_name}")
    else:
        st.warning("请在上方输入大学和教授姓名以激活自动化工具。")

# --- 2. 居留/签证 (全球通用深度解析) ---
with tabs[1]:
    st.subheader(f"🛂 {target_country} 居留、签证与全家方案")
    st.markdown(f"### 🛡️ {target_country} 核心办证指南")
    col1, col2 = st.columns(2)
    with col1:
        st.info("📌 办证标准流程")
        st.write("1. **签证申请**: 根据录取信(Offer)向该国使馆申请学生签证。")
        st.write("2. **居留转换**: 入境后根据当地法律，将签证转换为长期居留许可。")
        st.write("3. **资产证明**: 通常需要提供覆盖首年生活费的存款证明。")
        st.link_button(f"📜 {target_country} 官方签证要求", get_search(f"{target_country} immigration student visa official"))
    with col2:
        st.info("👨‍👩‍👧 全家搬迁 (Dependent Visa)")
        st.write("- **家属权利**: 多数主流国家允许博士生配偶申请随行，且部分国家允许配偶全职工作。")
        st.write("- **子女教育**: 随行子女通常可享受当地免费公立义务教育。")
        st.link_button(f"🔗 搜查 {target_country} 陪读签证政策", get_search(f"{target_country} family reunification visa for students"))

# --- 3. 陶瓷/邮件 (全场景增强版) ---
with tabs[2]:
    st.subheader("✉️ 陶瓷邮件、回复话术与发送时机")
    st.markdown("### 📝 场景化邮件模板")
    with st.expander("点击展开：学术陶瓷标准模板 (First Contact)"):
        st.code("""
Subject: Prospective PhD Inquiry: [Your Major] - [Your Name]
Dear Professor [Name],
I am writing to express my strong interest in your research on [Research Topic]. 
Currently, I am a [Master/Bachelor] student at [Your Univ]...
        """, language="markdown")
    with st.expander("点击展开：面试后的感谢信 (Follow-up)"):
        st.code("Dear Professor, Thank you for the inspiring interview today regarding the [Project Name]...")
    st.link_button(f"📅 自动化唤起：{u_name} 关键节假日校历", get_search(f"{u_name} academic calendar"))

# --- 4. 文书/简历 (工具大填充) ---
with tabs[3]:
    st.subheader("📄 文书/简历与防 AI 检测中心")
    st.markdown("### 🛠️ 全球认可的简历标准")
    st.write("- **学术 CV**: 强调科研产出、会议经历及导师推荐。")
    st.link_button("🚀 访问 Overleaf 全球学术简历模板库", "https://www.overleaf.com/gallery/tagged/cv")
    st.markdown("### 🛡️ AI 痕迹消除与检测")
    st.error("注意：顶尖大学会使用高级工具检测文书的 AI 生成率。")
    st.link_button("🔍 使用 GPTZero 自测文书 AI 率", "https://gptzero.me/")
    st.link_button("✍️ 学术润色参考工具 (Quillbot)", "https://quillbot.com/")

# --- 5. 找工/永居 (全球身份规划) ---
with tabs[4]:
    st.subheader(f"💼 {target_country} 找工、永居与身份转换")
    st.success(f"📊 {target_country} 典型毕业生政策概览")
    st.write("1. **找工假**: 大多数国家提供 1-2 年的签证延长期用于寻找本地工作。")
    st.write("2. **永居转换**: 在当地合法纳税并工作满一定年限，可申请永久居留。")
    st.link_button(f"🔍 搜查 {target_country} 的博士/博后职位 (LinkedIn)", f"https://www.linkedin.com/jobs/search/?keywords=PhD&location={target_country}")
    st.link_button(f"🛂 {target_country} 永居(PR)详细条件", get_search(f"{target_country} permanent residency requirements for postgraduates"))

# --- 6. 健康/心理 (安全指南) ---
with tabs[5]:
    st.subheader("🍎 留学生健康、心理与学生保险")
    st.markdown("### 🏥 全球就医建议")
    st.write("- **强制医保**: 务必在入学注册时购买当地要求的强制学生险。")
    st.write("- **心理热线**: 面对压力，首选校内 Wellbeing 办公室。")
    st.link_button(f"🆘 紧急搜索 {u_name} 心理援助服务", get_search(f"{u_name} student mental health counselling support"))

# --- 7. 法律/维权 (救助通道) ---
with tabs[6]:
    st.subheader("🛡️ 法律、维权与举报渠道")
    st.error("⚠️ 遭遇霸凌、歧视或科研成果被侵占？")
    st.markdown("### ⚖️ 官方纠纷解决通道")
    st.write("- **Ombudsman**: 大学法定的独立调查官，专门处理针对校方或导师的投诉。")
    st.link_button(f"🛡️ 自动唤起：{u_name} 调解员(Ombudsman)办公室", get_search(f"{u_name} student ombudsman office complaints"))

# --- 8. 48月规划 (全生命周期规划) ---
with tabs[7]:
    st.subheader("📅 全周期 48 个月深度规划")
    st.markdown("### 📈 博士生涯关键里程碑")
    st.write("- **Q1-Q4 (第1年)**: 课程学习、实验室轮转、确定最终选题。")
    st.write("- **Q5-Q8 (第2年)**: 资格考试 (Qualifying Exam)、发表首篇核心论文。")
    st.write("- **Q9-Q12 (第3年)**: 深度研究、参加大型国际学术会议、中后期考核。")
    st.write("- **Q13-Q16 (第4年)**: 撰写毕业论文、准备答辩、启动全球找工计划。")
    st.date_input("设定您的项目起始日期", value=datetime.now())
