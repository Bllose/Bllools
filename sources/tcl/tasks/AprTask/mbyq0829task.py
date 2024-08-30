from rich.console import Console
import os
import json

con = Console()

def taskProcess(mbyqClient):
    con.print("========================================================", style="pale_turquoise1")
    con.print("========================================================", style="pale_turquoise1")
    con.print("====>>>>>>>>1.流程规则处理<<<<<<<<<======================", style="pale_turquoise1")
    con.print("========================================================", style="pale_turquoise1")
    con.print("========================================================", style="pale_turquoise1")
    mbyqClient.set_fund_list = [129,133,135,131,134,132]
    jsonProcessRule = mbyqClient.fetchProcessRule(['待预审提交'])
    total = jsonProcessRule['total']
    print(f'一共找到规则:{total}条')
    records = jsonProcessRule['records']

    needCreateProcessRule = True
    for record in records:
        ruleName = record['ruleName']
        if not ruleName.startswith('活动授权书'):
            continue

        ruleItem = record['ruleItem']
        shell = record['shell']
        productIdList = record['productIdList']
        con.print(f'匹配到规则: id:{ruleItem} name:{ruleName} list:{productIdList} shell:{shell}', style="green1")
        needCreateProcessRule = False
        break

    if needCreateProcessRule:
        dictParam = {
            "productIdList" : [129,133,135,131,134,132],
            "scenesList": ["待预审提交"],
            "ruleName": "活动授权书未完成，请确认",
            "shell": '!gUtil.metaClass.respondsTo(gUtil, "rangeOfEffectiveTime") || !gUtil.rangeOfEffectiveTime(orderDetail) || gUtil.isExistImageCode(orderDetail, "OBO001_image")'
        }
        mbyqClient.saveNewProcessRule(dictParam)


    con.print("========================================================", style="pale_turquoise1")
    con.print("========================================================", style="pale_turquoise1")
    con.print("====>>>>>>>>2.模版引擎配置<<<<<<<<<======================", style="pale_turquoise1")
    con.print("========================================================", style="pale_turquoise1")
    con.print("========================================================", style="pale_turquoise1")    
    mbyqClient.get([129,133,135,131,134,132])

    root = mbyqClient.get_path()
    mbyqConfigHandler(root)
    

def mbyqConfigHandler(root: str):
    for root, dirs, files in os.walk(root):
        dirs[:] = [] # 阻止所有子目录的遍历
        for file in files:
            if 'OrderDetail' in file:
                orderDetailHandler(root + os.sep + file, file)
            elif 'preOrder' in file:
                preOrderhandler(root + os.sep + file, file)


def orderDetailHandler(absFileName: str, fileName: str):
    with open(absFileName, 'r', encoding='utf-8') as file:
        content = file.read()
        data = json.loads(content)
        for group in data['tabs'][0]['groups']:
            groupName = group['groupName']
            if groupName == '预审资料':
                for item in group['items']:
                    itemKey = item['itemKey']
                    if itemKey == 'OBO001_image':
                        labelName = item['labelName']
                        displayRule = item['displayRule']
                        itemIndex = item['itemIndex']
                        con.print(f'匹配到规则: file:{fileName} id:{itemKey} name:{labelName} index:{itemIndex} rule:{displayRule}', style="dark_sea_green2")
                        return
        con.print(f'file:{fileName} 未匹配到规则变化，需要配置!', style="dark_red")            
        



def preOrderhandler(absFileName: str, fileName: str):
    with open(absFileName, 'r', encoding='utf-8') as file:
        content = file.read()
        data = json.loads(content)

        contractSignModified = False
        contractImageModified = False
        for group in data['tabs'][0]['groups']:
            groupName = group['groupName']
            if groupName == '合同签约':
                for item in group['items']:
                    labelName = item['labelName']
                    if '沐光同行' in labelName:
                        displayRule = item['displayRule']
                        con.print(f'匹配到合同签署配置：file:{fileName} label:{labelName} displayRule:{displayRule}', style="medium_spring_green")
                        contractSignModified = True
                        break
            elif groupName == '影像件信息':
                for item in group['items']:
                    labelName = item['labelName']
                    if '沐光同行' in labelName:
                        displayRule = item['displayRule']
                        con.print(f'匹配到合同签影像件：file:{fileName} label:{labelName} displayRule:{displayRule}', style="spring_green2")
                        contractImageModified = True
                        break
        
        if not contractImageModified or not contractSignModified:
            con.print(f'file: {fileName} 还未完成配置！', style="dark_red")



if __name__ == '__main__':
    mbyqConfigHandler('D:\\workplace\\20240829')