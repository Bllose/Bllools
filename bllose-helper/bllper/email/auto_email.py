import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart  # 多部分邮件容器
from email.header import Header
import os
import traceback

from dotenv import load_dotenv
def analysis_email_senders(config_str: str) -> list:
    sender_holder = []
    senders = config_str.split('|')
    for sender in senders:
        param = sender.split(',')
        sender_holder.append({'smtp_server': param[0], 'email_sender': param[1], 'sender_password': param[2]})
    return sender_holder

load_dotenv()
auto_email_info_group = os.getenv('auto_email_info_group')
email_sender_list = analysis_email_senders(auto_email_info_group)

def send_a_email(attachment_path: str, 
                 smtp_server: str, 
                 sender_email: str, 
                 sender_password: str,
                 smtp_port: int = 587) -> bool:
    """
    根据附件发送邮件
    """
    receiver_email  = os.getenv('email_receiver')

    # 创建邮件内容
    message =  MIMEMultipart()
    # MIMEText("这是一封测试邮件", "plain", "utf-8")
    message["From"] = Header(sender_email)
    message["To"]   = Header(receiver_email)

    fileName = os.path.basename(attachment_path)
    extension = os.path.splitext(attachment_path)[1]  # 输出: ".pdf"

    message["Subject"] = Header(f"auto - {fileName}", "utf-8")
    # 2. 添加邮件正文（作为多部分的第一个子部分）
    text_part = MIMEText("自动推送", "plain", "utf-8")
    message.attach(text_part)  # 附件前必须先添加正文或其他子部分

    # 添加附件（关键部分）
    with open(attachment_path, "rb") as file:
        # 创建附件对象，指定文件类型（可选）
        attachment = MIMEApplication(file.read(), _subtype=extension)
        # 设置附件文件名，需使用 Header 处理中文
        attachment.add_header(
            "Content-Disposition", 
            "attachment", 
            filename=("utf-8", "", fileName)  # 中文文件名需指定编码
        )
        message.attach(attachment)

    # 连接 SMTP 服务器并发送邮件
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用 TLS 加密
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"邮件发送成功 {fileName} - {sender_email} -> {receiver_email}")
    except Exception as e:
        print(f"邮件发送失败: {e}")
        traceback.print_exc()
        return False
    finally:
        server.quit()
    return True


def send_simple_email(smtp_server, sender_email, sender_password, receiver_email, smtp_port = 465):
    # 创建邮件
    message = MIMEText("这是测试邮件", "plain", "utf-8")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "测试邮件"

    # 使用 SMTP_SSL 建立 SSL 连接
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("邮件发送成功")
    except Exception as e:
        print(f"发送失败: {e}")


if __name__ == '__main__':
    path = r'D:\repository\python_package'

    smtp_server     = os.getenv("163_smtp_server")
    sender_email    = os.getenv('163_email_sender')
    sender_password = os.getenv('163_sender_password')
    email_receiver  = os.getenv('email_receiver')
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                send_a_email(entry.path, smtp_server, sender_email, sender_password)
    # send_simple_email(smtp_server, sender_email, sender_password, email_receiver)