import win32com.client
import os
from pathlib import Path
from typing import List, Optional

def send_email_via_outlook(
    to: str,
    subject: str,
    body: str,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    attachments: Optional[List[str]] = None,
    html_body: bool = False,
    save_draft: bool = False,
    show_email: bool = False,
) -> None:
    """
    使用 Outlook 客户端发送邮件
    
    参数:
    - to: 收件人邮箱，多个邮箱用分号分隔
    - subject: 邮件主题
    - body: 邮件正文
    - cc: 抄送邮箱，多个邮箱用分号分隔
    - bcc: 密送邮箱，多个邮箱用分号分隔
    - attachments: 附件路径列表
    - html_body: 是否使用 HTML 格式的正文
    - save_draft: 是否保存到草稿箱而非发送
    - show_email: 是否显示邮件窗口（用于确认）
    """
    # 创建 Outlook 应用实例
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)  # 0 表示邮件项
    
    # 设置邮件基本信息
    mail.To = to
    mail.Subject = subject
    
    # 设置正文
    if html_body:
        mail.HTMLBody = body
    else:
        mail.Body = body
    
    # 设置抄送和密送
    if cc:
        mail.CC = cc
    if bcc:
        mail.BCC = bcc
    
    # 添加附件
    if attachments:
        for attachment_path in attachments:
            if os.path.exists(attachment_path):
                mail.Attachments.Add(Source=os.path.abspath(attachment_path))
            else:
                print(f"警告: 附件不存在 - {attachment_path}")
    
    # 保存到草稿箱或发送
    if save_draft:
        mail.Save()
        print("邮件已保存到草稿箱")
    else:
        if show_email:
            mail.Display()  # 显示邮件窗口但不发送
            input("按回车键发送邮件...")
        mail.Send()
        print("邮件已发送")

if __name__ == "__main__":
    # 示例：发送带附件的 HTML 邮件
    send_email_via_outlook(
        to="chenbx@hkbea.com",
        subject="测试邮件 - 带附件",
        body="<h1>你好！</h1><p>这是一封测试邮件，包含附件。</p>",
        cc="bllose@qq.com",
        attachments=[
            r"D:\repository\python_package\simple1.part001"
        ],
        html_body=True,
        show_email=True  # 显示邮件窗口供确认
    )