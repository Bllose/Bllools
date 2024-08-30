import logging
import os
import json


def signContractHandler(group):
    """
    合同签署内容配置回滚
    """


def imageContractHandler(group):
    """
    合同影像件内容回滚
    """


def rollbackHandler(path:str):
    target_funds = ['光鑫宝-共富', '光瑞宝', '光悦宝', '整村汇流', '公共屋顶', '光煜宝-全款建站']
    position_stack = []

    for root, dirs, files in os.walk(path):
        dirs[:] = [] # 阻止所有子目录的遍历  
        for curFileName in files:
            if curFileName.split('_')[1] not in target_funds:
                logging.info(f"{curFileName}不在本次作业范围，跳过...")
                continue
            
            absFileName = root + os.sep + curFileName
            with open(absFileName, 'r') as file:
                content = file.read()
                data = json.loads(content)
                position_stack.append(curFileName)

                tabs = data['tabs']
                for tab in tabs:
                    position_stack.append(tab['tabName'])
                    for group in tab['groups']:
                        groupName = group['groupName']
                        position_stack.append(groupName)

                        if groupName == '合同签约':
                            signContractHandler(group)
                        elif groupName == '影像件信息':
                            imageContractHandler(group)


