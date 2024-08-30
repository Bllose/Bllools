from Crypto.Cipher import AES  
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes  
from base64 import b64decode  
  
# 假设这是你的加密数据和密钥（经过Base64解码）  
encrypted_data = b64decode('P-XRM60/dL1yFJewQTcr5Z9w==')[3:]  # 去掉前面不需要的字符，这里假设MySQL的substr和from_base64已经处理  
key = b64decode('XDM4Vvla+6kxP++4yOXb5A==')  
  
# AES通常需要块大小为16（AES-128）、24（AES-192）或32（AES-256）字节的密钥  
# 这里假设密钥长度是合适的（MySQL的AES_DECRYPT可能会自动截断或填充密钥）  
  
# MySQL的AES_DECRYPT默认使用ECB模式，但通常不推荐（因为它不提供消息认证）  
# 这里也使用ECB模式作为示例  
cipher = AES.new(key, AES.MODE_ECB)  
  
# 注意：这里我们假设数据已经是正确填充的，但实际上MySQL的AES_DECRYPT可能会使用PKCS#7或其他填充  
# 如果你知道具体的填充方式，你应该相应地调整它  
decrypted_data = cipher.decrypt(encrypted_data)  
  
# 尝试去除填充（如果知道填充方式的话）  
# 在这个例子中，我们不知道填充方式，所以我们只是打印原始解密的数据  
# 如果需要，可以使用Crypto.Util.Padding.unpad来去除填充，但你需要知道填充的长度  
# decrypted_data = unpad(decrypted_data, AES.block_size)  # 这可能会引发一个错误，因为填充可能不正确  
  
print(decrypted_data)  # 这将打印解密后的字节串  
  
# 如果需要，可以将字节串转换为字符串（注意：这可能会失败，除非你知道原始数据的编码）  
# try:  
#     print(decrypted_data.decode('utf-8'))  # 假设原始数据是UTF-8编码的  
# except UnicodeDecodeError:  
#     print("解码失败，可能不是UTF-8编码")