"""
电站运维合同
TPSH003
97份合同重新生成
"""
from eqb.eqbHandler import eqb_sign as signer
from eqb.eqbHandler import environment
import json
import logging
from config_center.config import config

MY_CONFIG = None

def transforComponent(target:dict) -> list:
    """
    将 key : value 转化为 {'componentKey': key, 'componentValue': value}
    """
    return [{'componentKey': key, 'componentValue': value} for key, value in target.items()]

def createReq4FileId(fileName: str, docTemplateId: str, fillElement: dict):
    """
    {{host}}/v3/files/create-by-doc-template 
    通过e签宝合同文件请求报文 生产合同文件 fileId
    """
    components = transforComponent(fillElement)
    return {'fileName': fileName, 'docTemplateId': docTemplateId, 'components': components}

def createDocs4Req(fileId: str) -> dict:
    """
    创建合同签署任务的要素之一： 合同文件
    """
    return {'fileName': '电站运维合同', 'fileId': fileId}

def createSignFlowConfig4Req(notifyUrl: str) -> dict:
    """
    创建合同签署任务的要素之一： 签署流程配置
    @param notifyUrl: 回调地址配置
    """
    return {
            "autoFinish": True,
            "autoStart": True,
            "notifyUrl": notifyUrl,
            "signFlowTitle": "电站运维合同",
            "noticeConfig": {}
            }

def getTransactor(key: str) -> dict:
    """
    从配置项中获取经办人信息
    """
    global MY_CONFIG
    if MY_CONFIG is None:
        MY_CONFIG = config().load()
    
    personInfo = MY_CONFIG.get('person')[key]

    return {'psnAccount': personInfo['mobile'], 'psnInfo': {
        'psnIDCardType': 'CRED_PSN_CH_IDCARD',
        'psnIDCardNum': personInfo['idCard'],
        'psnName': personInfo['name']
    }}


def callbackUrlByEnv(env: str):
    """
    获取e签宝回调地址
    """
    global MY_CONFIG
    if MY_CONFIG is None:
        MY_CONFIG = config().load()
    env = env.lower()
    match env:
        case 'pro':
            return MY_CONFIG.get('eqb')['pro']['callbackUrl']
        case _:
            return MY_CONFIG.get('eqb')['test']['callbackUrl']
        
def getSigners(fileId: str, transactorInfo: dict, 
               companyName: str, orgIdCard: str,
               companySeal: str, representSeal: str,
               lastCompanySealPosition: dict,
               shanxiTclSeal: str, shanxiRepresentSeal: str) -> dict:
    return [{
                "signConfig": {
                "signOrder": 1
                },
                "orgSignerInfo": {
                    "orgName": companyName,
                    "transactorInfo": transactorInfo,
                    "orgInfo": {
                        "orgIDCardType": "CRED_ORG_USCC",
                        "orgIDCardNum": orgIdCard
                    }
                },
                "signFields": [
                    {
                        "normalSignFieldConfig": {
                        "signFieldPosition": {
                            "positionX": 80,
                            "positionY": 690.62213,
                            "positionPage": "16"
                        },
                        "autoSign": False,
                        "signFieldStyle": 1,
                        "assignedSealId": companySeal
                        },
                        "fileId": fileId
                    },
                    {
                        "normalSignFieldConfig": {
                        "signFieldPosition": lastCompanySealPosition,
                        "autoSign": False,
                        "signFieldStyle": 1,
                        "assignedSealId": companySeal
                        },
                        "fileId": fileId
                    },
                    {
                        "normalSignFieldConfig": {
                        "signFieldPosition": {
                            "positionX": 200.85641,
                            "positionY": 632.92,
                            "positionPage": "16"
                        },
                        "autoSign": False,
                        "signFieldStyle": 1,
                        "assignedSealId": representSeal
                        },
                        "fileId": fileId
                    },
                    {
                        "normalSignFieldConfig": {
                        "signFieldPosition": {
                            "positionY": 400,
                            "acrossPageMode": "ALL"
                        },
                        "autoSign": False,
                        "signFieldStyle": 2,
                        "assignedSealId": companySeal
                        },
                        "fileId": fileId
                    }
                ],
                "signerType": 1
            },
            {
                "signConfig": {
                "signOrder": 1
                },
                "orgSignerInfo": {
                "orgName": "TCL光伏智维科技（深圳）有限公司",
                "transactorInfo": transactorInfo,
                "orgInfo": {
                    "orgIDCardType": "CRED_ORG_USCC",
                    "orgIDCardNum": "91440300MA5HK4220R"
                }
                },
                "signFields": [
                {
                    "normalSignFieldConfig": {
                    "signFieldPosition": {
                        "positionX": 80,
                        "positionY": 535.5562,
                        "positionPage": "16"
                    },
                    "autoSign": False,
                    "signFieldStyle": 1,
                    "assignedSealId": shanxiTclSeal
                    },
                    "fileId": fileId
                },
                {
                    "normalSignFieldConfig": {
                    "signFieldPosition": {
                        "positionX": 200.85641,
                        "positionY": 474.857,
                        "positionPage": "16"
                    },
                    "autoSign": False,
                    "signFieldStyle": 1,
                    "assignedSealId": shanxiRepresentSeal
                    },
                    "fileId": fileId
                },
                {
                    "normalSignFieldConfig": {
                    "signFieldPosition": {
                        "positionY": 530,
                        "acrossPageMode": "ALL"
                    },
                    "autoSign": False,
                    "signFieldStyle": 2,
                    "assignedSealId": shanxiTclSeal
                    },
                    "fileId": fileId
                }
                ],
                "signerType": 1
            }]


def main(shanxiOrgId: str, template_id: str, env: str, person: str,
         target: dict, orgId: str, objectNo: str):
    keyResult = []
    keyResult.append(f'合同编号:objectNo:{objectNo}')

    req = createReq4FileId('电站运维合同', template_id, target)

    # 构建e签宝客户端，通过环境，选择生产客户端或者是测试客户端
    eqb = signer(*environment(env))

    # 通过客户端，推送前面组装的请求报文，最终获得合同文件ID
    fileId, _ = eqb.createByDocTemplate(json.dumps(req))
    keyResult.append(f'文件ID:third_file_id:{fileId}')

    import time

    seconds = 3
    logging.debug(f'延迟{seconds}秒，等待e签宝创建文档')
    time.sleep(seconds)
    
    # 在新获取的合同文件中定位关键字位置
    postionList = eqb.searchWordsPosition(fileId, 'projectKeyword')
    # 本次任务需要获取最后一页的唯一坐标位置
    # 通过所在页面编号和坐标，组装最后一个项目公司印章所在位置
    pageNum = postionList[-1]['pageIndex']
    postion = postionList[-1]['coordinateList'][0]
    theLastPosition = {'positionPage': pageNum, 'positionX': postion['posx'], 'positionY': postion['posy']}
    
    # 从 fill_element 中获取项目公司名称 和 统一社会信用代码
    # 通过这个信息获取项目公司ID 和相关的印章ID
    unifiedSocialCreditCode = target['unifiedSocialCreditCode']
    companyName = target['company1']
    
    sealList = eqb.fetchSealInfoByOrgId(orgId)
    gongzhang_sealId = [seal['sealId'] for seal in sealList if seal['alias'] == '公章'][0]
    fadingdaibiaoren_sealId = [seal['sealId'] for seal in sealList if seal['sealType'] == 2][0]

    shanxiSealList = eqb.fetchSealInfoByOrgId(shanxiOrgId)
    sx_gongzhang_sealId = [seal['sealId'] for seal in shanxiSealList if seal['alias'] == '公章'][0]
    sx_fadingdaibiaoren_sealId = [seal['sealId'] for seal in shanxiSealList if seal['sealType'] == 2][0]

    # 最终组装发起合同的三要素
    # 要素一 签署人信息
    transforPerson = getTransactor(person)
    signers = getSigners(fileId=fileId, transactorInfo=transforPerson, 
               companyName=companyName, orgIdCard=unifiedSocialCreditCode, 
               companySeal=gongzhang_sealId, representSeal=fadingdaibiaoren_sealId,
               lastCompanySealPosition=theLastPosition,
               shanxiTclSeal=sx_gongzhang_sealId, shanxiRepresentSeal=sx_fadingdaibiaoren_sealId)
    # 要素二 签署文件信息
    docs = createDocs4Req(fileId)
    # 要素三 签署流程配置
    signFlowConfig = createSignFlowConfig4Req(callbackUrlByEnv(env))
    
    request = {'signFlowConfig': signFlowConfig, 'signers': signers, 'docs': [docs]}
    signFlowId = eqb.createByFile(json.dumps(request))
    keyResult.append(f'e签宝签约流水号:third_flow_id:{signFlowId}')

    
    signUrl = eqb.getH5Url(transforPerson['psnAccount'], signFlowId)
    keyResult.append(f'签约地址:sign_url:{signUrl}')

    logging.warning('; '.join(keyResult))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # # 入参=======================================================================================
    # # 固定入参↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    # shanxiOrgId = '84be2e76366d4a0baa3636c1d595420f'
    # template_id = '40bb69dcca95484f91327ab417d63976'
    # env = 'test'
    # person = 'me'
    # # 固定入参↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
    # # 将数据库保存的 fill_element 组装成对应的请求报文
    # # 结合模版ID，创建具体的合同文件
    # target = {"unifiedSocialCreditCode":"91360430MACL8M6Q2B","contractNo":"TCLYWHT000023","legalRepresent":"邓国萍","yearMonth":"2024年09月","date6":"2024年09月19日","companyRepresent":"邓国萍","date4":"2024年09月19日","date3":"2024年09月19日","date1":"2024年09月19日","registerAddress":"广西壮族自治区梧州市岑溪市岑城镇思湖路天河广场斜对面（黄结玲、杨云秀、杨东澎屋6楼602室）","company1":"九江泰盈惠合新能源科技有限公司","company2":"九江泰盈惠合新能源科技有限公司","company3":"九江泰盈惠合新能源科技有限公司","registerAddress2":"广西壮族自治区梧州市岑溪市岑城镇思湖路天河广场斜对面（黄结玲、杨云秀、杨东澎屋6楼602室）","company4":"九江泰盈惠合新能源科技有限公司","company5":"九江泰盈惠合新能源科技有限公司","company6":"九江泰盈惠合新能源科技有限公司","dtbg":"[{\"row\":{\"column1\":\"\",\"column5\":\"\",\"column4\":\"\",\"column3\":\"\",\"column2\":\"\"}},{\"row\":{\"column1\":1,\"column5\":\"0408410140793028\",\"column4\":\"广西壮族自治区梧州市岑溪市糯垌镇糯三路57-19\",\"column3\":\"27.090\",\"column2\":\"阳光房\"}},{\"row\":{\"column1\":2,\"column5\":\"0408410140366240\",\"column4\":\"广西壮族自治区梧州市岑溪市糯垌镇古淡村三组21号\",\"column3\":\"12.600\",\"column2\":\"阳光房\"}},{\"row\":{\"column1\":3,\"column5\":\"0408410139800322\",\"column4\":\"广西壮族自治区梧州市岑溪市归义镇双贵村333号竹山六组\",\"column3\":\"22.050\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":4,\"column5\":\"0408410140599772\",\"column4\":\"广西壮族自治区梧州市岑溪市糯垌镇地麻村下地四组221号\",\"column3\":\"28.350\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":5,\"column5\":\"0408410140599293\",\"column4\":\"广西壮族自治区梧州市岑溪市糯垌镇地麻村下地四组169号\",\"column3\":\"39.690\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":6,\"column5\":\"0408410140793129\",\"column4\":\"广西壮族自治区梧州市岑溪市糯垌镇叶伦村叶的六组79号\",\"column3\":\"37.800\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":7,\"column5\":\"0408410140598287\",\"column4\":\"广西壮族自治区梧州市岑溪市糯垌镇地麻村下地四组170号\",\"column3\":\"34.020\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":8,\"column5\":\"0408410140551846\",\"column4\":\"广西壮族自治区梧州市岑溪市安平镇太平社区爱群十二组170号\",\"column3\":\"52.920\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":9,\"column5\":\"0408410140276479\",\"column4\":\"广西壮族自治区梧州市岑溪市安平镇太平社区爱群十二组80号\",\"column3\":\"15.120\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":10,\"column5\":\"0408410140879795\",\"column4\":\"广西壮族自治区梧州市岑溪市诚谏镇诚谏社区三角一组785号\",\"column3\":\"20.160\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":11,\"column5\":\"0408410140879535\",\"column4\":\"广西壮族自治区梧州市岑溪市诚谏镇诚谏社区米戌组874号\",\"column3\":\"39.060\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":12,\"column5\":\"0408410140580707\",\"column4\":\"广西壮族自治区梧州市岑溪市诚谏镇诚谏社区米戌组876号\",\"column3\":\"30.240\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":13,\"column5\":\"0408410141553146\",\"column4\":\"广西壮族自治区梧州市岑溪市三堡镇古堆村石冲1组25号\",\"column3\":\"44.100\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":14,\"column5\":\"0408410140375772\",\"column4\":\"广西壮族自治区梧州市岑溪市归义镇秋风村231号\",\"column3\":\"38.430\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":15,\"column5\":\"0408410140670819\",\"column4\":\"广西壮族自治区梧州市岑溪市三堡镇月田村樟木根组30号\",\"column3\":\"41.580\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":16,\"column5\":\"0408410139942673\",\"column4\":\"广西壮族自治区梧州市岑溪市归义镇垌头村111号\",\"column3\":\"62.370\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":17,\"column5\":\"0408410140743906\",\"column4\":\"广西壮族自治区梧州市岑溪市归义镇谢村村龙坡三组\",\"column3\":\"40.950\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":18,\"column5\":\"0408410140839456\",\"column4\":\"广西壮族自治区梧州市岑溪市筋竹镇筋竹街\",\"column3\":\"78.810\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":19,\"column5\":\"0408410141080376\",\"column4\":\"广西壮族自治区梧州市岑溪市筋竹镇大王村大王坪组127号\",\"column3\":\"31.950\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":20,\"column5\":\"0408410142319972\",\"column4\":\"广西壮族自治区梧州市岑溪市三堡镇月田村樟木根组\",\"column3\":\"17.750\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":21,\"column5\":\"0408410141243058\",\"column4\":\"广西壮族自治区梧州市岑溪市岑城镇山心村山心十五组\",\"column3\":\"22.010\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":22,\"column5\":\"0408410141139010\",\"column4\":\"广西壮族自治区梧州市岑溪市水汶镇旺公村瓦二组11号\",\"column3\":\"39.050\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":23,\"column5\":\"0408410142431090\",\"column4\":\"广西壮族自治区梧州市岑溪市水汶镇西河村草坡组2号\",\"column3\":\"22.720\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":24,\"column5\":\"0408410142325506\",\"column4\":\"广西壮族自治区梧州市岑溪市大隆镇西宁社区大冲组\",\"column3\":\"29.820\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":25,\"column5\":\"0408410141938011\",\"column4\":\"广西壮族自治区梧州市岑溪市岑城镇升平街73号\",\"column3\":\"14.200\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":26,\"column5\":\"0408410142343573\",\"column4\":\"广西壮族自治区梧州市岑溪市归义镇保太村365号\",\"column3\":\"55.380\",\"column2\":\"阳光房\"}},{\"insertRow\":true,\"row\":{\"column1\":27,\"column5\":\"0408410142029349\",\"column4\":\"广西壮族自治区梧州市岑溪市归义镇双贵村竹山七组\",\"column3\":\"42.600\",\"column2\":\"阳光房\"}}]","registerAddressProvince":"广西壮族自治区","orderStage":"并网"}
    # # 技术问题， orgId 单独获取， 然后以参数传递进来
    # orgId = 'c7512ed7332045f087c7028d551285a8'
    # objectNo = 'TPSH-TPSHHY(2024)ZL00028'
    # # 入参=======================================================================================
    
    # main(shanxiOrgId, template_id, env, person, target, orgId, objectNo)

    from helper.file_helper import readExcelSheet1
    absPath = r"D:\workplace\target.xlsx"  
    for each in readExcelSheet1(absPath):
        main(each['shanxiOrgId'], each['template_id'], 
             each['env'], each['person'], 
             json.loads(each['target']), 
             each['orgId'], each['objectNo'])
    
    print('DONE!')