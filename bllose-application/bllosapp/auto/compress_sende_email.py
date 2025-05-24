from bllper.compress import compress_folder
from bllper.email.auto_email import send_a_email
import time
import os
from rich.console import Console
from dotenv import load_dotenv

def analysis_email_senders(config_str: str) -> list:
    sender_holder = []
    senders = config_str.split('|')
    for sender in senders:
        param = sender.split(',')
        sender_holder.append({'smtp_server': param[0], 'smtp_port': int(param[1]), 'email_sender': param[2], 'sender_password': param[3]})
    return sender_holder

load_dotenv()
auto_email_info_group = os.getenv('auto_email_info_group')
email_sender_list = analysis_email_senders(auto_email_info_group)

RETRY_MAX_TIMES = 3
console = Console()

compress_path = r'D:\temp\installer'
output_zip_path = r'D:\temp\installer'
zip_file_list = compress_folder(compress_path, output_zip_path)

counter = 0
for zip_file in zip_file_list:
    SEND_SUCCESS = False
    retry_times_recorder = 0
    while not SEND_SUCCESS and retry_times_recorder < RETRY_MAX_TIMES:
        sender = email_sender_list[counter%len(email_sender_list)]
        try:
            SEND_SUCCESS = send_a_email(zip_file, sender['smtp_server'],sender['email_sender'],sender['sender_password'], sender['smtp_port'])
        except:
            SEND_SUCCESS = False
            # 等待半分钟后重试
            time.sleep(30)
        counter += 1
        retry_times_recorder += 1
    if retry_times_recorder >= RETRY_MAX_TIMES:
        console.print(f'{zip_file} 重试过多，跳过 ...')
    