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
import urllib

class eqb_sign():
    def __init__(self, app_id, app_key, host) -> None:
        self.header = {
            'X-Tsign-Open-App-Id': app_id,
            'X-Tsign-Open-Auth-Mode': 'Signature',
            'Host': host,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': '*/*',
            'Content-Type': 'application/json; charset=UTF-8',
            'Connection': 'keep-alive'
        }
        self.host = host
        self.app_key = app_key
        self.type = 'POST'

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
        self.establish_head_code(bodyRaw, current_path)
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
        self.establish_head_code(bodyRaw, current_path)
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
        self.establish_head_code(bodyRaw, current_path)
        response_json = self.getResponseJson(bodyRaw, current_path)
        if response_json['code'] == 0:
            data = response_json['data']
            return data['accountId']
        elif response_json['code'] == 53000000:
            data = response_json['data']
            return data['accountId']
        
    def getSignFlowDetail(self, signFlowId):
        """
        获取签署流程详情
        """
        current_path = f'/v3/sign-flow/{signFlowId}/detail'
        self.establish_head_code(None, current_path, 'GET')
        conn = http.client.HTTPSConnection(self.host)
        conn.request(method='GET', url=current_path, headers=self.header)
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
    
    def createFileByTemplate(self, bodyRaw: str) -> tuple:
        """
        通过 template_id 和相关的合同要素，制作合同文件

        返回 tuple(fileId, downloadUrl)
        """
        current_path = r'/v1/files/createByTemplate'
        self.establish_head_code(bodyRaw, current_path)
        response_json = self.getResponseJson(bodyRaw=bodyRaw, current_path=current_path)
        if response_json['code'] == 0:
            data = response_json['data']
            return data['fileId'], data['downloadUrl']
    
    def createByDocTemplate(self, req) -> tuple:
        """
        模版制作文件接口
        @param req: 组装好的请求报文，包含 fileName, docTemplateId, components
        返回 fileId, fileDownloadUrl
        """
        current_path = r'/v3/files/create-by-doc-template'
        self.establish_head_code(req, current_path)
        response_json = self.getResponseJson(bodyRaw=req, current_path=current_path)
        if response_json['code'] == 0:
            data = response_json['data']
            return data['fileId'], data['fileDownloadUrl']
        
    def createByFile(self, req: str) -> str:
        """
        （精简版）基于文件发起签署
        """
        current_path = r'/v3/sign-flow/create-by-file'
        self.establish_head_code(req, current_path)
        response_json = self.getResponseJson(bodyRaw=req, current_path=current_path)
        if response_json['code'] == 0:
            return response_json['data']['signFlowId']
        else:
            return ''
        
    def getH5Url(self, psnAccount: str, thirdFlowId: str) -> str:
        """
        通过账号和流水号获取签约地址
        """
        req = {
                    "needLogin": True,
                    "urlType": 2,
                    "operator": {
                        "psnAccount": psnAccount
                    }
                }
        current_path = f'/v3/sign-flow/{thirdFlowId}/sign-url'
        bodyRaw = json.dumps(req, ensure_ascii=False)
        self.establish_head_code(bodyRaw, current_path)
        response_json = self.getResponseJson(bodyRaw=bodyRaw, current_path=current_path)
        if response_json['code'] == 0:
            return response_json['data']['shortUrl']
        else:
            return ''


    def searchWordsPosition(self, fileId:str, keyword: str) -> list:
        """
        查询单个关键词位置
        直接返回这个关键词的所属位置列表
        否则返回空列表
        """
        query_string = urllib.parse.urlencode({'keywords': keyword})
        current_path = f'/v1/documents/{fileId}/searchWordsPosition?{query_string}'
        self.establish_head_code(None, current_path, 'GET')

        response_json = self.getResponseJson(bodyRaw=None, current_path=current_path)
        if response_json['code'] == 0:
            return response_json['data'][0]['positionList']
        else:
            logging.error(f'查询关键词位置失败,返回报文:{response_json}')
            return []

    def getOrganizationInfo(self, orgIdCard: str) -> dict:
        """
        通过社会统一信用代码
        获取项目公司在e签宝上的相关信息
        TODO 当前401，待解决
        """
        query_string = urllib.parse.urlencode({'orgIDCardType': 'CRED_ORG_USCC', 'orgIDCardNum': orgIdCard})
        current_path = f'/v3/organizations/identity-info?{query_string}'
        self.establish_head_code(None, current_path, 'GET')
        response_json = self.getResponseJson(bodyRaw=None, current_path=current_path)
        if response_json['code'] == 0:
            return response_json
        
    def fetchSealInfoByOrgId(self, orgId: str) -> list:
        """
        通过e签宝中注册的企业ID
        获取该企业下的印章ID信息
        若查询成功， 则返回印章信息列表
        否则返回空列表
        """
        current_path = f'/v1/organizations/{orgId}/seals'
        self.establish_head_code(None, current_path, 'GET')
        response_json = self.getResponseJson(bodyRaw=None, current_path=current_path)
        if response_json['code'] == 0:
            return response_json['data']['seals']
        else:
            return []


        
    def getResponseJson(self, bodyRaw, current_path) -> json:
        """
        通过请求地址和请求参数
        获取返回报文
        """
        conn = http.client.HTTPSConnection(self.host)
        if bodyRaw is not None:
            bodyRaw = bodyRaw.encode("utf-8").decode("latin1")
        conn.request(self.type, current_path, bodyRaw, self.header)
        response = conn.getresponse()

        match response.code:
            case 403:
                logging.warning(f'拒绝访问!')
                return json.loads({'code': 999})
            case 401:
                logging.warning('未授权!')
                return json.loads({'code': 999})
            case 404:
                logging.warning(f'请求路径不存在!{current_path}')
                return json.loads({'code': 999})
            # case _:
                # logging.info(f'返回报文:{response}')


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

    def establish_head_code(self, bodyRaw, pathAndQuery, method = 'POST'):
        """
        组装e签宝请求报文头中关键的几个编码
        """
        contentMd5 = ''
        if method == 'POST':
            contentMd5 = md5_base64_encode(bodyRaw)
            self.type = 'POST'
        elif method == 'GET':
            self.type = 'GET'
        else:
            logging.error(f"不支持的请求类型: {method}")
        self.header['Content-MD5'] = contentMd5
        accept = self.header['Accept']
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

myConfig = None
def environment(env: str):
    from helper.config_helper import config
    global myConfig
    if myConfig is None:
        myConfig = config().load()
    env = env.lower()
    match env:
        case 'pro':
            return str(myConfig.get('eqb')['pro']['appId']), myConfig.get('eqb')['pro']['appKey'], myConfig.get('eqb')['pro']['host']
        case _:
            return str(myConfig.get('eqb')['test']['appId']), myConfig.get('eqb')['test']['appKey'], myConfig.get('eqb')['test']['host']


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    client = eqb_sign(*environment('test'))
    client.fetchSealInfoByOrgId('c7512ed7332045f087c7028d551285a8')

