import ijson
from urllib.request import Request, urlopen
from urllib.error import URLError
from requests.exceptions import SSLError  
import json
import os
import logging
from rich.console import Console
from rich import inspect

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
        if funds is not None and len(funds)>1:
            self.funds = funds
        else:
            self.funds = {112: '光富宝',115: '光鑫宝',128: '光盈宝',129: '光鑫宝-共富',130: '光富宝-同裕',131: '光瑞宝',132: '整村汇流',133: '公共屋顶',134: '光悦宝',135: '光煜宝-全款建站',136: '光煜宝-融资建站'}

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

    def get(self,
            fund_list = []):
        
        if len(self.page_key_list) == 0:
            print('需要指定pageKey!')
            return 
        elif len(fund_list) == 0:
            fund_list = [key for key in self.funds]

        headers = {
            'Authorization': self.authorization
        }


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
            if self.origin:
                with open(str(fundId) + '_' + self.funds[fundId] +'_origin.json', 'w', encoding='UTF-8') as f:
                    f.write(str(content, 'UTF-8'))

            objects = ijson.items(content, 'data.item')
            tab_list = [x for x in objects]
            # key_list = [x['pageKey'] for x in tab_list]

            for tab in tab_list:
                key = tab['pageKey']
                if key in self.page_key_list:
                    curJson = json.dumps(tab)
                    file_name = self.path + os.sep + str(fundId) + '_' + self.funds[fundId] + '_' + key + '.json'
                    with open(file_name, 'w') as f:
                        f.write(curJson)
                        if logger.isEnabledFor(logging.INFO):
                            self.myConsole.print(f'写入文件{file_name}', style='bold italic cyan')
                else:
                    if logger.isEnabledFor(logging.DEBUG):
                        self.myConsole.print(f'KEY:{key} 不在本次工作范围，略过', style='dim bright_yellow')


    def push(self, filter: list):

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


