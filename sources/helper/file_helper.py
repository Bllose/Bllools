# import fitz

# pdf = r'D:\temp\target.pdf'
# doc = fitz.open(pdf)
# out = open(r"d:\temp\output.txt", "wb") 
# for page in doc: # iterate the document pages
# 	text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
# 	out.write(text) # write text of page
# 	out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
# out.close()
# print("done")


# import pdfplumber

# pdf = pdfplumber.open(r'D:\temp\target.pdf')
# pages = pdf.pages
# text = pages[0].extract_text()
# print("done")

import hashlib  
import base64  
  
def get_file_content_md5(file_path):  
    """  
    计算文件的Content-MD5，并以Base64编码返回  
    :param file_path: 文件路径  
    :return: Base64编码的MD5字符串  
    """  
    # 创建一个hash对象，使用md5算法  
    md5_hash = hashlib.md5()  
      
    try:  
        # 打开文件，准备读取  
        with open(file_path, "rb") as file:  
            # 分块读取文件，更新hash对象  
            for byte_block in iter(lambda: file.read(4096), b""):  
                md5_hash.update(byte_block)  
                  
        # 获取md5摘要的二进制数据  
        md5_bytes = md5_hash.digest()  
        # 对md5摘要进行base64编码  
        md5_base64 = base64.b64encode(md5_bytes).decode('utf-8')  
        return md5_base64  
    except FileNotFoundError:  
        print(f"文件未找到: {file_path}")  
        return None  
    except Exception as e:  
        print(f"发生错误: {e}")  
        return None  
  

if __name__ == '__main__':
    # 示例用法  
    file_path = r"C:\Users\bllos\Desktop\光煜宝-全款建站V1.2合同\光伏电站交付验收确认书.docx"  
    file_content_md5 = get_file_content_md5(file_path)  
    print(f"文件Content-MD5值: {file_content_md5}")