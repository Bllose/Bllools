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
    def __init__(self, app_id, app_key, host) -> None:
        self.header = {
            'X-Tsign-Open-App-Id': app_id,
            'X-Tsign-Open-Auth-Mode': 'Signature',
            'Host': 'openapi.esign.cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': '*/*',
            'Content-Type': 'application/json; charset=UTF-8',
            'Connection': 'keep-alive'
        }
        self.host = host
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

    def establish_head_code(self, bodyRaw, pathAndQuery, method = 'POST'):
        """
        组装e签宝请求报文头中关键的几个编码
        """
        if method == 'POST':
            contentMd5 = md5_base64_encode(bodyRaw)
            self.header['Content-MD5'] = contentMd5
        elif method == 'GET':
            contentMd5 = ''
        else:
            logging.error(f"不支持的请求类型: {method}")
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    from helper.config_helper import config

    myConfig = config()
    myConfig.load()
    if myConfig.hasConfig('eqb'):
        appId = str(myConfig.get('eqb')['pro']['appId'])
        appKey = myConfig.get('eqb')['pro']['appKey']
        host = myConfig.get('eqb')['pro']['host']
    else:
        logging.warning('加载配置文件失败!')
        exit(1)

    if myConfig.hasConfig('person'):
        name = myConfig.get('person')['me']['name']
        idCard = myConfig.get('person')['me']['idCard']
        mobile = myConfig.get('person')['me']['mobile']
    # client = eqb_sign(app_id=appId, app_key=appKey, host=host)
    # request = '{"name":"TCL光伏科技 沐光同行家国共贺 活动授权书","templateId":"f880544a64b24b529d47a6df6d39b95b","simpleFormFields":{}}'
    # fileId, downloadUrl= client.createFileByTemplate(request)
    # logging.info(f'fileId: {fileId}')
    # logging.info(f'downloadUrl: {downloadUrl}')


    # accountId = client.getUserId(name=name, idNumber=str(idCard), mobile=str(mobile))
    # logging.info(f'accountId: {accountId}')

    # flowId = client.createSignFlow(fileId=fileId, accountId=accountId)
    # logging.info(f'flowId: {flowId}')

    # shortUrl = client.fetchSignUrl(flowId=flowId, mobile=str(mobile))
    # logging.info(f'shortUrl: {shortUrl}')

    client = eqb_sign(app_id=appId, app_key=appKey, host=host)

    targetMap = {'GF240906112545205218' : 'a054ef27d6424ff9b8d95340814f241c','GF240906115931228435' : '82d144fa635341368e2c43e27d3a5ca5','GF240907140200151323' : 'f9712b171f8b4c0d84c1e7649e0cd7bc','GF240907153153186636' : '76b17b134ed14299be2b9592ff65d5f6','GF240907154123190083' : 'bec95df6bddf42c0b2c2a9a4ced5cb95','GF240908104235061092' : '1be4b8646172445080b259b055502dc2','GF240910103024073949' : '974dca57e0364b259addb8f2032a2510','GF240912095226047848' : '8f9a2bf664254fc2a188be144e0d4f79','GF240912105856090290' : '372678c42abf4b28bdf3ee386ff3008d','GF240912113925112778' : '1f2f274eaf9242bf8c83a23143c8acbf','GF240912123619137756' : '7b83572d8f3c43ffb17efe0d4d1fb5c1','GF240912202142322311' : 'd4c8e81016f84325b01b8383ae821792','GF240913152547274628' : '56645b4902b24a889a2547a7369a38ae','GF240913153723281123' : '08b052a6d6304fc28cb342da80cd64fc','GF240916173225145707' : 'b91cf6cc69064b04b7008593365957b0','GF240916181106152940' : 'a5e748960e544ca48b7ac07dde08c4b7','GF240919153134225967' : '961b53ff9b294d629df0b7ef15d7356c','GF240920112422111315' : 'c243432917ac4a749c4b5e5190899770','GF240921133230156279' : '5ac7a184e4794960830268c056c37bbb','GF240922152658177432' : '3f4e60e9db9141da95e41d00db60459e','GF240922173257224596' : '1c8573f49c574c91afecdfebab0e0afa','GF240922203948257376' : '954bdb96cbdf453699918ddf3942b676','GF240923100902047035' : 'e5c69f0b3ce24185acb8d54772a941f9','GF240923162701241551' : '92e6685bdbac4b419c313756b5ff02e6','GF240923183350293468' : '4db785e1e9514645bdf847c79e49829a','GF240926120201123038' : '3b5d2bc23eff4c61b47c498e75d3f96f','GF240926132705159500' : '3fb090f116cc4936966dcbae476a2db1','GF240926120811126872' : '5b62278894d84f489a6c603b08d9f51f','GF240926135615172156' : '039e786385fa4a1292244bb59806e34f','GF240926140825176486' : '6750fd8b39a24cd0ae3f04d0db4e48b8','GF240926152220211769' : '441be9de3008483fa6449b34082f7fda','GF240926160915231209' : '77776bed5075432aaf4a90b57c81c1d7','GF240927115709117079' : 'e6a67515439744d999fcbbccfc99358d','GF240927155437220544' : '8f8e8c5188bf4ca39615cc2fee7bb5ce','GF240927161317230280' : '5dcaed4d311e475fbed43fd5a8eda7ca','GF240928101450056838' : 'aa3a8400616d462c830a88cbef3b6337','GF240928111612093262' : 'f40f24d1d9f648cf9b4b59c8d492f8c1','GF240928145541179923' : '519b22788efe4d44be66e1e809186a10','GF240928133148150616' : '45519e67f67a4ba482c200eb05550ae7','GF240928150258183864' : '8a416ac43d3649988e0499df86b8923e','GF240928152924196026' : '06073eb0cdb84fe2bcebdc6c74ee23eb','GF240928155819211166' : '57188e99648745878bf6d3f81aef71a0','GF240928161341218946' : 'f097d3611bd847cfaca51a0110437da3','GF240928141329163973' : '7e74f00aab8b4409a8af1164fc312935','GF240928170815238339' : 'd90438f756964f6ea0831ae7bc891ec2','GF240929093134024676' : 'e315df6861584207b32d51b58017b362','GF240929142732158254' : '8931c200d8de447cbf96c454663b439c','GF241001122146069268' : 'cfe6d40c92dc4e7cbc25c297d999522e','GF241001175611139449' : '3564d8395ffe45178a7206797350a9a2','GF241002102017031459' : 'eafb7f09468043188eb2c0e5f6172680','GF241003120748064013' : '803a2de5c9c64ee2843ee2deefeed2e6','GF241004100020030584' : '7624fc4bb706480f97baa80f22051119','GF241004144659112078' : 'daee9548493942619c988e9d295edd72','GF241005120142074240' : '20bc70b58eee4beea8a2a0e238cda78e','GF241005140751108233' : '7a448150dbe446cb9fc9d8b8d575e3cd','GF241005155725144403' : '5820abd5c65248ddb2c6af74152dae79','GF241005164739161462' : '48bdc2f3ae474cddb094d52e1b9efbc4','GF241006095145024147' : 'e1c453eefc284a6c97d45a09f1cf8e6b','GF241007141052118226' : '51b349046be4449a8f8ec133a6fc4ac5','GF241007144708130488' : '32297d14074c4b3d98b99e95f0671410','GF241008152259208009' : '9af9676fb2b84285a17566f5d12276b9','GF241008165012260715' : '3604c4393e074328bc72dae5f29f16cb','GF241009103306075691' : '52dbd7d9982f4a8581261f2788a811cd','GF241009140927195943' : 'e81c4cb99fdc4f8b9e445d00d7a0d96f','GF241009154253250379' : '552bb4b47398432094a4ba0144bb94e9','GF241010094749044287' : 'd45ff2b8b52e42bbb356858a5f3f3591','GF241010102156069821' : '365a50b4a5f64ae6997e6a4784e8113a','GF241010124343151060' : '3b70b4cc375b4bbda05a7da87859beb2','GF241010152344227736' : '02285ebc5dbf4548956dac58af38ccf3','GF241011090445017804' : '8b383a2065214b65a92f812a56c7adfc','GF241011102437056592' : 'e6b56137dcaa4073b0b93ee106595d7d','GF241011134657167494' : 'fc6e1fa3f61b40f48e4d013e07a285d6','GF241011153855223512' : 'd37b798d2e5c4a22b6323e6ff5242267','GF241012170927272980' : 'bf014bf7763b49748f0d8543509f977a','GF241012181650293282' : '9d0a9af1efc84ae9ba4ef1a7404abf8a','GF241013113239094957' : '812a9631f9e74c51ba79d284da78838a','GF241013131725145555' : '2c0392622783434ab7855469dc073503','GF241014100909047594' : '28453d7f6b2a43f7b981f0f3ddcb3e78','GF241014105009076278' : 'df74cdfdad724d55a74e408c30710b9a','GF241014110825087136' : '28d339b3e22047878e5e4e01e2e24a77','GF241014140805180662' : '1b07dbb2c8734270bd07283079740141','GF241014161144249248' : '5fdf3ea4b4504d239993c4fc29749c7d','GF241014161627251307' : '0b526f28c206408994704047fdea0369','GF241015073958004445' : '13687dec91e04961ab088a2acd032437','GF241015112055117228' : '20986eb80a024a53a9481dabfcad9008','GF241015120948150498' : 'a1c57eb07ef9413e81c826bc18e38ad8','GF241015122722160592' : 'ee6fb02951b94e0997e1b0b073d12dce','GF241015134751201367' : 'ae3e8259b17b492dbf4408c862002718','GF241015142222219229' : 'cba1f2f5c20b44ec9f8dce3a1703bee2','GF241015142942222939' : '4cc7ad80bbd244a78bf2417ef6bc9791','GF241015150807246418' : 'eff4187985974e4a98b0b858bc039d12','GF241015180720340746' : '5b0382335bba4ff9b4512614d5c89125','GF241015104710092248' : 'db6259da33a341b8980a89ea23512a45','GF241016102114054535' : '17e99fb606f24ba7ba079fd2921df0b9','GF241016113319101781' : '6d5e0af49e7f45c4a7091b270680261a','GF241016144436202025' : '9463274a36f84ea1a831c8eaf3e0fca9','GF241016152350224438' : 'efd54d1871fd4431932881bc7c7d2d5a','GF241016153107228688' : 'a805a95f296e4f97a847f0fd319126c1'}

    for orderNo, flowId in targetMap.items():
        
        response_json = client.getSignFlowDetail(flowId)

        if response_json is not None and response_json['code'] == 0:
            data = response_json['data']
            signers = data['signers']
            for signer in signers:
                psnSigner = signer['psnSigner'] # 自然人签约主体
                orgSigner = signer['orgSigner'] # 项目公司签约主体
                signFields = signer['signFields'] # 签署位置信息
                if orgSigner is not None:
                    for signField in signFields:
                        normalSignFieldConfig = signField['normalSignFieldConfig'] # 普通印章配置
                        sealId = normalSignFieldConfig['sealId'] # 印章ID
                        if sealId == '11ceebca-12ac-4e03-8c6e-7c138f1b5e5e':
                            print(f'{orderNo}\t{flowId}\t泰安沛辉太阳能发电有限公司')
                        elif sealId == '730bbf23-b193-4413-8cae-155a2c24da62':
                            print(f'{orderNo}\t{flowId}\t惠州TCL光伏科技有限公司')
        else:
            print(json.dumps(response_json))

