import datetime

class OverseasSuccessBot:
    def __init__(self, start_date):
        self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        self.current_month = self._get_current_month()

    def _get_current_month(self):
        now = datetime.datetime.now()
        return (now.year - self.start_date.year) * 12 + now.month - self.start_date.month

    def trigger_action(self):
        month = self.current_month
        print(f"--- 当前处于第 {month} 个月 ---")
        
        if month <= 12:
            return self.template_early_stage()
        elif 13 <= month <= 36:
            return self.template_mid_stage()
        else:
            return self.template_late_stage()

    def template_early_stage(self):
        return """
        [✉️ 邮件唤起] 导师初次陶瓷模板:
        Subject: Inquiry regarding Potential Research Collaboration - [Your Name]
        Body: Dear Prof. [Name], I am writing to express my strong interest in your work on...
        
        [🛂 身份提醒] 请检查您的居留卡是否在3个月内过期。
        """

    def template_mid_stage(self):
        return """
        [📄 文书防AI] 提示词: "Please rephrase the following CV summary to be more human-centric, 
        avoiding typical AI buzzwords while maintaining professional impact."
        
        [💼 找工] 检查 LinkedIn 个人资料，确保 Headline 包含最新关键词。
        """

    def template_late_stage(self):
        return """
        [💼 永居申请] 检查清单:
        1. 连续居住证明 (Utility bills, Council Tax)
        2. 无犯罪证明
        3. 语言考试成绩单 (if applicable)
        
        [🛡️ 法律] 检查雇佣合同中的解雇补偿金 (Severance) 与竞业协议条款。
        """

# 使用方法：输入你的开始日期 (格式: YYYY-MM-DD)
# bot = OverseasSuccessBot("2024-09-01")
# print(bot.trigger_action())
