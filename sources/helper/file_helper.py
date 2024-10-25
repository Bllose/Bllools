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
    # ('TPSH-SF489273252636659712', '{third_flow_id}', '{object_id}', 'TPSH008', '起租-租赁合同-附件二', 'e签宝短信签约', '', 3, '-', 2, 'CHECK', 0, '', '', NOW(), now(), 'TPSH-TPSHHY(2024)ZL00521', '', now(), now(), '{sign_url}', 'v1', 'TPSH008#image', 0, '{third_file_id}', '{cosign_url}'),
    # ('TPSH-SF489273252636659712', '{third_flow_id}', '{object_id}', 'TPSH007', '起租-供货合同-附件二', 'e签宝短信签约', '', 3, '-', 2, 'CHECK', 0, '', '', NOW(), NOW(), 'TPSH-TPSHHY(2024)ZL00521', '', NOW(), NOW(), '{sign_url}', 'v1', 'TPSH007#image', 0, '{third_file_id}', '{cosign_url}');
    absPath = r"C:\Users\bllos\Desktop\tpsh007008SignedFiles.xlsx"  
    datas = readExcelSheet1(absPath=absPath)
    
    values = []
    for data in datas:
        contractName = data['contractName']
        objectId = data['objectId']
        batchNo = data['batchNo']
        match contractName:
            case '起租-供货合同-附件二':
                # TPSH007
                values.append(f"('-', '-', '{objectId}', 'TPSH007', '起租-供货合同-附件二', 'e签宝短信签约', '', 3, '-', 2, 'CHECK', 0, '', '', NOW(), now(), 'TPSH-{batchNo}', '', now(), now(), '-', 'v1', 'TPSH007#image', 0, '-', '-')")
            case '起租-租赁合同-附件二':
                # TPSH008
                values.append(f"('-', '-', '{objectId}', 'TPSH008', '起租-租赁合同-附件二', 'e签宝短信签约', '', 3, '-', 2, 'CHECK', 0, '', '', NOW(), now(), 'TPSH-{batchNo}', '', now(), now(), '-', 'v1', 'TPSH008#image', 0, '-', '-')") 
    print('INSERT INTO `xk-contract`.`sf_sign_flow`')
    print("(sign_flow_no, third_flow_id, object_id, scene_code, scene_name, sign_type, signer, channel, template_code, sign_method, sign_flow_phase, is_delete, creator, updator, create_time, update_time, object_no, fill_element, flow_start_time, flow_end_time, sign_url, version, image_code, is_reuse, third_file_id, cosign_url)")
    print('values')
    for value in values:
        print(value + ',')
        