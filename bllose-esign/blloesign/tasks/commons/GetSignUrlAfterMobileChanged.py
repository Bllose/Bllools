from blloesign.esign.Client import eqb_sign
import logging

def getTheNewSignUrl(name:str, mobile:str, creditId:str, flowId:str, env:str = 'test') -> str:
    """
    通过签署人、经办人的个人信息三要素和合同流水号，获取最新的签约地址
    Args:
        name(str): 三要素：人名
        mobile(str): 三要素：电话
        credit(str): 三要素：身份证号码
        flowId(str): 合同流水号
    Returns:
        shortUrl(str): 签约地址
    """
    if name is None or mobile is None or creditId is None or flowId is None:
        return ''
    client = eqb_sign(env)
    # 尝试使用三要素创建账户并返回账户ID，若存在则返回已经存在的账户ID
    accountId = client.getAccountId(name=name, idNumber=creditId, mobile=mobile)
    # 对目标账户ID更新用户三要素信息
    updatedData = client.updateAccountsByid(accountId=accountId, name=name, mobile=mobile)
    accountId = updatedData['accountId']
    # 通过最新的账户id结合签约流水号获取到签约地址
    shortUrl = client.getExeUrl(accountId=accountId, thirdFlowId=flowId)
    logging.info(flowId, mobile, name, accountId, ' -> ', shortUrl)
    return shortUrl

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    origin_info = r'GF250206094515012561,林乌番,13806943149,350625195301151535,林丽秀,13860807719,350625197711041549,0608e88a61704cc0a75d9ff01eb62c9b,PCI001,PC002_image'
    split_info = origin_info.split(',')

    lesseeSignUrl = getTheNewSignUrl(name=split_info[1], mobile=split_info[2], creditId=split_info[3], flowId=split_info[7], env='pro')
    cosignerSignUrl = getTheNewSignUrl(name=split_info[4], mobile=split_info[5], creditId=split_info[6], flowId=split_info[7], env='pro')
    logging.info(f'Lessee Sign URL: {lesseeSignUrl}')
    logging.info(f'Cosigner Sign URL: {cosignerSignUrl}')
