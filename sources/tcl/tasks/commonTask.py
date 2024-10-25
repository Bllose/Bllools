import logging
from eqb.eqbHandler import eqb_sign



logging.basicConfig(level=logging.INFO)
client: eqb_sign = eqb_sign()

# from helper.file_helper import get_file_content_md5
# import os

# file_path = r'C:\Users\bllos\Desktop\浦银二期合同'
# fileName = r'买卖合同（二次结算）_new.pdf'
# absPath = file_path + os.sep + fileName

# file_stat = os.stat(absPath)  
# file_size = file_stat.st_size 

# md5 = get_file_content_md5(absPath)

# fileId, fileUploadUrl = client.fetchUpdateFileUrl(md5, fileName, file_size)
# print(f'md5: {md5}')
# print(f'fileId: {fileId}')
# print(fileUploadUrl)

# code, reason = client.uploadFile(fileUploadUrl, md5, absPath)
# if code != 200:
#     print(f'上传失败! 失败原因{code}: {reason}')

client.searchWordsPosition('7ef9c75d5dec4604a3c929f0be52c0bc', '法定代表人或授权代理人（签字或盖章）')