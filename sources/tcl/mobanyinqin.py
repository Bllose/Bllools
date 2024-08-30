import ijson
from urllib.request import Request, urlopen
from urllib.error import URLError
from requests.exceptions import SSLError  
import json
import os
import logging
from rich.console import Console
from rich import inspect
import time
import shutil

logger = logging.getLogger(__name__)

class mbyq():
    def __init__(self, 
                 token: str,
                 host: str = None,
                 origin: bool = False,
                 path: str = '/workplace',
                 page_key_list = [],
                 funds = []):
        """
        @param log_level: 日志等级，默认20： INFO;
        """
        self.myConsole = Console()
        self.authorization = token
        self.origin = origin
        self.path = path
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        self.page_key_list = page_key_list
        self.host = host
        self.funds_dict = {112: '光富宝',115: '光鑫宝',128: '光盈宝',129: '光鑫宝-共富',130: '光富宝-同裕',131: '光瑞宝',132: '整村汇流',133: '公共屋顶',134: '光悦宝',135: '光煜宝-全款建站',136: '光煜宝-融资建站'}
        if funds is not None and len(funds) > 0:
            self.funds = funds
        else:
            self.funds = [112, 115, 128, 129, 130, 131, 132, 133, 134, 135, 136]
    
    def set_path(self, path:str):
        if path is not None and len(path) > 0:
            if os.path.exists(path):
                self.path = path

    def get_path(self):
        return self.path

    def set_log_level(self, level: int):
        if level is None or not isinstance(level, int):
            return
        if level < 1 or level > 60:
            return
        logger.setLevel(level=level)
        logger.debug(f'当前日志等级: {logger.level}') 

    def set_host(self, host: str):
        if host is not None and len(host) < 1:
            return
        self.host = host
    
    def set_token(self, token: str):
        if token is not None and len(token) < 1:
            return
        self.authorization = token

    def set_page_key_list(self, pageKeyList):
        """
        重新定义pageKey列表
        """
        if pageKeyList is not None and len(pageKeyList) > 0:
            self.page_key_list = pageKeyList

    def set_fund_list(self, fundIdList):
        if fundIdList is not None and len(fundIdList) > 0:
            self.funds = fundIdList

    def get(self,
            fund_list = []):
        """
        从模版引擎中获取tabs信息
        fund_list 控制产品范围，优先直接输入，其次配置文件读取
        self.page_key_list 指定pageKey范围, 由配置文件读取。或者在调用该方法之前使用 set_page_key_list 方法指定
        """
        
        if len(self.page_key_list) == 0:
            print('需要指定pageKey!')
            return 
        elif len(fund_list) == 0:
            fund_list = [key for key in self.funds_dict]

        headers = {
            'Authorization': self.authorization
        }

        cur_backup_path = self.path + os.sep + 'backup_' + str(int(time.time() * 10000000))
        if not os.path.exists(cur_backup_path):
            os.mkdir(cur_backup_path)
        for fundId in fund_list:
            currect_url = 'http://'+ self.host +'/api/order2/pageV2/getPages?fundId=' + str(fundId)
            try:
                logger.debug(f'获取pageKey内容, url: {currect_url}')
                f = Request(currect_url, headers=headers)
                s = urlopen(f)
            except (SSLError,URLError) as e:
                self.myConsole.print(f'尝试请求地址失败: {currect_url}', style="bold red")
                inspect(e)
                continue
            except Exception as exc:
                logger.error(f'尝试请求地址未知异常失败: {currect_url}')
                inspect(exc)
                continue

            content = s.read()
            cur_file_name = str(fundId) + '_' + self.funds_dict[int(fundId)] +'_origin.json'
            if self.origin:
                with open(cur_file_name, 'w', encoding='UTF-8') as f:
                    f.write(str(content, 'UTF-8'))

            objects = ijson.items(content, 'data.item')
            tab_list = [x for x in objects]
            # key_list = [x['pageKey'] for x in tab_list]

            for tab in tab_list:
                key = tab['pageKey']
                if key in self.page_key_list:
                    curJson = json.dumps(tab)
                    tab_file_name = str(fundId) + '_' + self.funds_dict[int(fundId)] + '_' + key + '.json'
                    file_name = self.path + os.sep + tab_file_name
                    with open(file_name, 'w') as f:
                        f.write(curJson)
                        if logger.isEnabledFor(logging.INFO):
                            self.myConsole.print(f'写入文件{file_name}', style='bold italic cyan')
                    bakup_file = cur_backup_path + os.sep + tab_file_name
                    shutil.copy2(file_name, bakup_file)
                else:
                    if logger.isEnabledFor(logging.DEBUG):
                        self.myConsole.print(f'KEY:{key} 不在本次工作范围，略过', style='dim bright_yellow')


    def push(self, filter: list):
        """
        将处理好的tab页信息推回给服务器
        注意文件所属路径为工作路径： self.path
        通过 set_path 方法指定当前工作路径
        
        @param filter: 用来指定需要上传的文件名， 注意是不包含路径的全名。 若不指定则会将目录下首层所有json报文都推送一次
        """

        url = 'https://'+ self.host +'/api/order2/pageV2/update'
        headers = {
            'Authorization': self.authorization,
            'Content-Type': 'application/json'
        }

        for root, dirs, files in os.walk(self.path, topdown=True):
            # 路径置为空, 从而让其只遍历根目录
            dirs[:] = [] 
            for file in files:
                # 在pageKeyList中的内容才是本次需要处理的对象
                shouldBeHandler = False
                if filter is None or len(filter) == 0:
                    for key in self.page_key_list:
                        if key in file:
                            shouldBeHandler = True
                            break
                else:
                    for filt in filter:
                        if file == filt:
                            shouldBeHandler = True
                            break
                abs_file_name = root + os.sep + file
                if not shouldBeHandler:
                    if logger.isEnabledFor(logging.DEBUG):
                        self.myConsole.print(f'{abs_file_name} 非目标文件，跳过', style='dim bright_yellow')
                    continue
                jsonContent = ''
                with open(abs_file_name, 'r', encoding='utf-8') as f:
                    jsonContent = f.read()
                data_b = jsonContent.encode('utf-8')
                f = Request(url=url, headers = headers, data=data_b)
                s = urlopen(f)
                self.myConsole.print(f'{abs_file_name} 上传结果 {s.read()}', style='bright_green')

    def fetchProcessRule(self, scenesList: list = []) -> json:
        """
        获取规则列表
        查询的产品范围为 self.funds, 通过方法 set_fund_list 指定

        返回查询到的 json 结果 
        如果查询失败，返回一个空的 json map
        """
        url = 'https://'+ self.host +'/api/order2/fundProcessRule/getPage'
        headers = {
            'Authorization': self.authorization,
            'Content-Type': 'application/json'
        }

        data_dict = {
            "pageNo": 1,
            "pageSize": 100,
            "productIdList": self.funds,
            "scenesList": scenesList
        }
        data_bytes = json.dumps(data_dict).encode("utf-8")
        f = Request(url=url, headers=headers, data=data_bytes)
        s = urlopen(f)
        json_str = s.read().decode('utf-8')  
        json_data = json.loads(json_str)
        if json_data['code'] != '0' :
            self.myConsole.print(f'查询到的规则失败，返回信息: {json_str}', style='red on white')
            return {}
        return json_data.get("data")
    
    def saveNewProcessRule(self, dictParam: dict):
        """
        新建一个流程规则
        """
        url = 'https://'+ self.host +'/api/order2/fundProcessRule/save'
        headers = {
            'Authorization': self.authorization,
            'Content-Type': 'application/json'
        }

        data_bytes = json.dumps(dictParam).encode("utf-8")
        f = Request(url=url, headers=headers, data=data_bytes)
        s = urlopen(f)
        json_str = s.read().decode('utf-8')  
        self.myConsole.print(f'创建流程规则，返回信息: {json_str}', style='red on white')
        


if __name__ == '__main__':
    handler = mbyq(token='Basic amd1c2VyOjEyMzQ1Ng==', host='aurora-test3-jg-pv.tclpv.com')
    handler.set_fund_list = [129,133,135,131,134,132]
    print(handler.fetchProcessRule(scenesList=['待预审提交']))

# if __name__ == '__main__':
    # page_key_list = ['applyInfo1', 'imageInfo04', 'OrderDetail', 'webDesignReview', 'webSignReview', 'imageInfo02', 'imageInfoSg4zlAndYg', 
    # 'arrayBuildImageInfo', 'arrayBuildImageInfo1', 'arrayBuildImageInfo2', 'courtyardBuildImageInfo', 'courtyardBuildImageInfo1', 'courtyardBuildImageInfo2',
    # 'sunBuildImageInfo', 'sunBuildImageInfo1', 'sunBuildImageInfo2']
    # fund_list = [129, 134]
    # handler = mbyq(token='Basic amd1c2VyOjEyMzQ1Ng==', path=r'D:\workplace\pythons\Bllools\20240423')
    # handler.get(fund_list=fund_list, page_key_list=page_key_list)

    # handler = mbyq(token='Basic amd1c2VyOjEyMzQ1Ng==', 
    #                path=r'D:\workplace\20240425', 
    #                host= None,
    #                page_key_list = ['webSignReview'])
    # handler.push(['129_光鑫宝-共富_FIELD_MAPPING.json'])


