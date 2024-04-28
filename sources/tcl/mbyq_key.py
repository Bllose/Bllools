import base64
# win32clipboard专门用来复制粘贴的
import win32clipboard as wcb
import win32con as wc
from datetime import datetime

name = "JG-PROD-PV-" + datetime.now().strftime('%Y%m%d')

# 编码
the_base_result = base64.b64encode(name.encode("ASCII"))  # b'amF2YXNjcmlwdA=='
print(the_base_result)




name = "JG-PROD-PV-" + datetime.now().strftime('%Y%m%d')
# 假设这是后台使用的密码
password = "password"
# 将用户名和密码合并，并进行Base64编码
credentials = f"{name}:{password}".encode("ASCII")
encoded_credentials = base64.b64encode(credentials)
# 构建HTTP基本认证头部
basic_auth_header = "Basic " + encoded_credentials.decode("ASCII")
print(basic_auth_header)

 
# 打开复制粘贴板
# wcb.OpenClipboard()
# # 我们之前可能已经Ctrl+C了，这里是清空目前Ctrl+C复制的内容。但是经过测试，这一步即使没有也无所谓
# wcb.EmptyClipboard()
# # 将内容写入复制粘贴板,第一个参数win32con.CF_TEXT不用管，我也不知道它是干什么的
# # 关键第二个参数，就是我们要复制的内容，一定要传入字节
# wcb.SetClipboardData(wc.CF_TEXT, the_base_result)
# # 关闭复制粘贴板
# wcb.CloseClipboard()