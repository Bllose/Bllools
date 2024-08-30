import os
import json
import logging
import time
import re

def handler(path:str):
    target_funds = ['光鑫宝-共富', '光富宝-同裕', '光瑞宝', '光悦宝', '整村汇流', '公共屋顶']
    position_stack = []
    done_file_path = path + os.sep + 'finish_' + str(int(time.time() * 10000000))
    loadBankInfoConfig = {"id": 6401,"itemKey": "tempCode","itemType": "INPUT","labelName": "项目公司结算账户加载","tipName": None,"tipInfo": None,"description": "用于加载信息到上下文 orderDetail","imagesCheck": None,"isMust": False,"isEdit": False,"isListenonchange": False,"isStandard": False,"displayRule": "False","computerRule": "return gUtil.metaClass.respondsTo(gUtil, 'loadBankInfoByOrderNo') ? gUtil.loadBankInfoByOrderNo(orderDetail) : \"加载方法不存在\";","config": None,"createTime": None,"updateTime": None,"isDelete": None,"value": None,"isDisplay": False,"itemIndex": 9999,"tableName": None,"columnName": None,"isEncrypt": False,"rowIndex": None,"isComponents": True}

    for root, dirs, files in os.walk(path):
        dirs[:] = [] # 阻止所有子目录的遍历  
        for curFileName in files:
            if curFileName.split('_')[1] not in target_funds:
                logging.info(f"{curFileName}不在本次作业范围，跳过...")
                continue
            if re.match(r'_bak\d{16}\.txt$', curFileName) is not None:
                continue
            depositBank4imageCheck = False # 是否有更新此字段
            bankNo4imageCheck = False      # 是否有更新此字段
            absFileName = root + os.sep + curFileName
            
            with open(absFileName, 'r') as file:
                needLoader = True
                content = file.read()
                data = json.loads(content)

                position_stack.append(curFileName)

                tabs = data['tabs']
                for tab in tabs:
                    position_stack.append(tab['tabName'])

                    for group in tab['groups']:
                        position_stack.append(group['groupName'])
                        '''
                        每个页面添加一次数据加载组件
                        '''
                        if needLoader:
                            group['items'].append(loadBankInfoConfig)
                            needLoader = False

                        for item in group['items']:
                            itemKey = item['itemKey']
                            itemType = item['itemType']
                            labelName = item['labelName']
                            if (itemKey == 'gouShouDianHeTong' and itemType == 'IMAGES_CHECK') or (labelName == '购售电合同' and itemType == 'IMAGES_CHECK'):
                                id = item['id']
                                position_stack.append('id:' + str(id))
                                logging.info(f'匹配到目标:购售电合同;位置:  {' -> '.join(position_stack)} mayKey: {itemKey}')
                                
                                imagesCheck = item['imagesCheck']
                                deposit = any(t['itemKey'] == 'depositBank4imageCheck' for t in imagesCheck if 'itemKey' in t)
                                bankNo = any(t['itemKey'] == 'bankNo4imageCheck' for t in imagesCheck if 'itemKey' in t)
                                
                                if deposit and bankNo:
                                    logging.info(f'==========> 已经配置过 {' -> '.join(position_stack)}')
                                else:
                                    """
                                    1、添加对应配置
                                    2、原配置文件下载重命名为 _bak 文件
                                    3、重新写入新的文件，作为推送文件
                                    """
                                    if not deposit:
                                        imagesCheck.append({'itemKey': 'depositBank4imageCheck', 'labelName': '项目公司结算账户-开户银行'})
                                        depositBank4imageCheck = True
                                    if not bankNo:
                                        imagesCheck.append({'itemKey': 'bankNo4imageCheck', 'labelName': '项目公司结算账户-银行账号'})
                                        bankNo4imageCheck = True
                                position_stack.pop()

                        position_stack.pop()
                    position_stack.pop()
                # 将内存中的json写回到str中, 若需要则写入新的文件中
                content = json.dumps(data)
            position_stack.pop()

            if depositBank4imageCheck or bankNo4imageCheck:
                if not os.path.exists(done_file_path):
                    os.mkdir(done_file_path)
                logging.debug(f'{curFileName} 有更新，制作推送文件...')
                done_file_abs_name = done_file_path + os.sep + curFileName
                with open(done_file_abs_name, 'w') as file:
                    file.write(content)
                logging.info(f'更新后的json已经保存到文件: {done_file_abs_name}')

                        