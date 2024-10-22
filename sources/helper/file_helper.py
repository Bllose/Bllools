import hashlib  
import base64  
import pandas as pd

def readExcelSheet1(absPath: str, sheet_name: str = 'Sheet1') -> dict:
    """
    读取目标excel 的 sheet1
    并且将每行作为一条数据返回
    其中，表头为key, 每行对应的cell为value
    """
    df = pd.read_excel(absPath, sheet_name=sheet_name)  
    return df.to_dict(orient= 'records')
  
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
    absPath = r"C:\Users\bllos\Desktop\太平石化供货合同附件刷新\TPSHHY(2024)ZL00016\起租-租赁合同-附件二.pdf"  
    print(get_file_content_md5(absPath))