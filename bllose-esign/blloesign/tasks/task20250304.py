from blloesign.esign.Client import eqb_sign
import requests
from bllper.fileHelper import FileReader

def download_file(url, new_filename):
    try:
        # 发送HTTP GET请求获取文件内容
        response = requests.get(url, stream=True)
        # 检查请求是否成功
        response.raise_for_status()
        # 以二进制写入模式打开新文件
        with open(new_filename, 'wb') as file:
            # 分块写入文件，每块大小为1024字节
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"文件下载成功，已保存为 {new_filename}")
    except requests.exceptions.RequestException as e:
        print(f"下载文件时发生网络错误: {e}")
    except Exception as e:
        print(f"下载文件时发生其他错误: {e}")

def download(env, param):
    client = eqb_sign(env)

    fileId = param.split(',')[2]
    batchNo = param.split(',')[0]
    finalFileName = batchNo + '-' + param.split(',')[1] + '.pdf'

    fileName, fileDownloadUrl, fileStatus = client.fetchFileByFileId(fileId)

    download_file(fileDownloadUrl, finalFileName)

    return fileName, fileDownloadUrl, fileStatus

class task(FileReader):
    def each_row_handler(self, curRow:str):
        download('pro', curRow.strip())


if __name__ == '__main__':
    task().read_file(r'D:\temp\2025年3月4日task.txt')