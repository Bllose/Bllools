"""
e签宝补救措施
1、通过模版创建文件
2、创建角色账号
3、通过文件获取盖章位置
4、通过“文件”，“账号”，“盖章位置”组装成一个发起签约的请求报文，获取流水号
5、通过“流水号”获取到签约地址
"""

from datetime import datetime, timezone  
import hashlib  
import base64
import hmac
import http.client
import io
import gzip
import logging
import json


class eqb_sign():
    def __init__(self, app_id, app_key) -> None:
        self.header = {
            'X-Tsign-Open-App-Id': app_id,
            'X-Tsign-Open-Auth-Mode': 'Signature',
            'Host': 'openapi.esign.cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': '*/*',
            'Content-Type': 'application/json; charset=UTF-8',
            'Connection': 'keep-alive'
        }
        self.host = r'openapi.esign.cn'
        self.app_key = app_key

    def fetchSignUrl(self, flowId, mobile):
        current_path = f'/v3/sign-flow/{flowId}/sign-url'
        request_dict = {
                        "needLogin": True,
                        "urlType": 2,
                        "operator": {
                            "psnAccount": mobile
                        }
                    }
        bodyRaw = json.dumps(request_dict)
        response_json = self.getResponseJson(bodyRaw, current_path)
        if response_json['code'] == 0:
            data = response_json['data']
            return data['shortUrl']

    
    def createSignFlow(self, fileId, accountId) -> str:
        """
        通过创建的文件和账号ID， 获取签约流水
        """
        current_path = r'/api/v2/signflows/createFlowOneStep'
        request_dict = {
                        "docs": [
                            {
                            "fileId": fileId,
                            "fileName": "TCL光伏科技“沐光同行 家国共贺”活动授权书.pdf"
                            }
                        ],
                        "flowInfo": {
                            "autoArchive": True,
                            "autoInitiate": True,
                            "businessScene": "TCL光伏科技“沐光同行 家国共贺”活动授权书",
                            "flowConfigInfo": {
                            "noticeDeveloperUrl": "https://callback1-pv.tcl.com/api/app/contract/unify/signed/callback/eqb",
                            "noticeType": "",
                            "redirectUrl": "",
                            "signPlatform": "1",
                            "willTypes": [
                                "FACE_TECENT_CLOUD_H5"
                            ]
                            }
                        },
                        "signers": [
                            {
                            "platformSign": False,
                            "signOrder": 1,
                            "signerAccount": {
                                "signerAccountId": accountId
                            },
                            "signfields": [
                                {
                                "autoExecute": False,
                                "fileId": fileId,
                                "sealType": "0",
                                "signDateBean": {
                                    "posPage": 1,
                                    "posX": 410.04,
                                    "posY": 266.437
                                },
                                "posBean": {
                                    "posPage": "1",
                                    "posX": 458.0,
                                    "posY": 316.477
                                },
                                "signDateBeanType": 2
                                }
                            ]
                            }
                        ]
                        }
        bodyRaw = json.dumps(request_dict)
        response_json = self.getResponseJson(bodyRaw, current_path)
        if response_json['code'] == 0:
            data = response_json['data']
            return data['flowId']


    def getUserId(self, name, idNumber, mobile) -> str:
        """
        通过三要素，获取账号ID
        """
        current_path = r'/v1/accounts/createByThirdPartyUserId'
        request_dict = {
                            "thirdPartyUserId": idNumber,
                            "name": name,
                            "idType": "CRED_PSN_CH_IDCARD",
                            "idNumber": idNumber,
                            "mobile": mobile
                        }
        bodyRaw = json.dumps(request_dict)
        response_json = self.getResponseJson(bodyRaw, current_path)
        if response_json['code'] == 0:
            data = response_json['data']
            return data['accountId']
        elif response_json['code'] == 53000000:
            data = response_json['data']
            return data['accountId']


    def createFileByTemplate(self, bodyRaw: str) -> tuple:
        """
        通过 template_id 和相关的合同要素，制作合同文件

        返回 tuple(fileId, downloadUrl)
        """
        current_path = r'/v1/files/createByTemplate'
        response_json = self.getResponseJson(bodyRaw=bodyRaw, current_path=current_path)
        if response_json['code'] == 0:
            data = response_json['data']
            return data['fileId'], data['downloadUrl']
        

    def getResponseJson(self, bodyRaw, current_path) -> json:
        """
        通过请求地址和请求参数
        获取返回报文
        """
        self.establish_head_code(bodyRaw, current_path)

        conn = http.client.HTTPSConnection(self.host)
        conn.request("POST", current_path, bodyRaw.encode("utf-8").decode("latin1"), self.header)
        response = conn.getresponse()

        # 检查是否需要解压  
        if response.getheader('Content-Encoding') == 'gzip':  
            # 使用gzip解压  
            compressed_data = response.read()  
            compressed_stream = io.BytesIO(compressed_data)  
            gzipper = gzip.GzipFile(fileobj=compressed_stream)  
            decoded_data = gzipper.read().decode('utf-8')  # 假设解压后的数据是utf-8编码  
        else:  
            # 直接解码  
            decoded_data = response.read().decode('utf-8')  

        logging.debug(decoded_data)
        response_json = json.loads(decoded_data)
        return response_json


    def establish_head_code(self, bodyRaw, pathAndQuery):
        """
        组装e签宝请求报文头中关键的几个编码
        """
        self.header['Content-MD5'] = md5_base64_encode(bodyRaw)
        method = 'POST'
        accept = self.header['Accept']
        contentMd5 = self.header['Content-MD5']
        contentType = self.header['Content-Type']

        # 获取当前UTC时间 
        the_time = datetime.now(timezone.utc)
        date_format = the_time.strftime('%a, %d %b %Y %H:%M:%S GMT')  

        beforeSignature = method + '\n'\
                        + accept + '\n'\
                        + contentMd5 + '\n'\
                        + contentType + '\n'\
                        + date_format + '\n'\
                        + pathAndQuery
        signature = hmacSHA_base64_encode(self.app_key, beforeSignature)
        self.header['X-Tsign-Open-Ca-Signature'] = signature
        self.header['X-Tsign-Open-Ca-Timestamp'] = str(int(the_time.timestamp()*1000))
        self.header['Date'] = date_format

        # print("appKey: " + appKey)
        # print("beforeSignature: ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓\n" + beforeSignature)
        # print("↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑")
        # print("signature: " + signature)

  
def hmacSHA_base64_encode(app_key, before_signature):
    # 将app_key转换为bytes，如果它是字符串的话  
    if isinstance(app_key, str):  
        app_key = app_key.encode('utf-8')  
    # 同样，如果before_signature是字符串，也转换为bytes  
    if isinstance(before_signature, str):  
        before_signature = before_signature.encode('utf-8')  
      
    # 使用hmac和sha256创建新的hmac对象  
    signature = hmac.new(app_key, before_signature, hashlib.sha256)  
      
    # 返回十六进制格式的哈希值  
    return base64.b64encode(signature.digest()).decode('utf-8')


def md5_base64_encode(body_raw):
    """
    将纯字符转化为MD5，然后再将MD5转化为Base64编码
    """
    # 计算 MD5 哈希  
    md5_hash = hashlib.md5(body_raw.encode('utf-8')).digest()  
    # 将 MD5 哈希的字节串进行 Base64 编码  
    base64_encoded = base64.b64encode(md5_hash).decode('utf-8')  
    return base64_encoded  


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    client = eqb_sign(app_id='5111744642', app_key='0ad8ab801105ee700a16d2bfc287d6b2')
    request = '{"name":"TCL光伏科技 沐光同行家国共贺 活动授权书","templateId":"f880544a64b24b529d47a6df6d39b95b","simpleFormFields":{}}'
    fileId, downloadUrl= client.createFileByTemplate(request)
    logging.info(f'fileId: {fileId}')
    logging.info(f'downloadUrl: {downloadUrl}')


    accountId = client.getUserId(name='陈曦', idNumber='431026198801130018', mobile='18129705502')
    logging.info(f'accountId: {accountId}')

    flowId = client.createSignFlow(fileId=fileId, accountId=accountId)
    logging.info(f'flowId: {flowId}')

    shortUrl = client.fetchSignUrl(flowId=flowId, mobile='18129705502')
    logging.info(f'shortUrl: {shortUrl}')

    sql_pre = "INSERT INTO `xk-contract`.sf_sign_flow (sign_flow_no, third_flow_id, object_id, scene_code, scene_name, sign_type, signer, channel, template_code, sign_method, sign_flow_phase, is_delete, creator, updator, create_time, update_time, object_no, fill_element, flow_start_time, flow_end_time, sign_url, version, image_code, is_reuse, third_file_id, cosign_url) VALUES";
    sql_param_template = "('SF472618987600089088', '{{flowId}}', NULL, 'OBO001','TCL光伏科技“沐光同行家国同贺”活动授权书', 'e签宝短信签约', '{{accountId}}', 3,'f880544a64b24b529d47a6df6d39b95b', 1, 'NEW', 0, 'sys', 'sys',now(), now(), '{{orderNo}}', '{}', NULL, NULL,'{{shortUrl}}', 'v1', 'OBO001_image', 0, '{{fileId}}', null)"
  