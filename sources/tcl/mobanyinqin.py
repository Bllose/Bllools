import ijson
from urllib.request import Request, urlopen
import json
import os


class mbyq():
    def __init__(self, 
                 token: str,
                 host: str = None,
                 origin: bool = False,
                 path: str = '/workplace',
                 page_key_list = []):
        self.authorization = token
        self.origin = origin
        self.path = path
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        
        current_work_dir = os.path.dirname(__file__)
        configYml = 'mbyq_config.yml'
        absYml = current_work_dir + os.sep + configYml
        config = ''
        if os.path.isfile(absYml):
            with open(absYml, 'r', encoding='utf-8') as f:
                config = f.read()
                if config is not None and len(config) > 1:
                    import yaml
                    data = yaml.safe_load(config)
                    self.funds = data['tcl']['funds']
                    if host is not None and len(host) > 1:
                        self.host = host
                    else:
                        self.host = data['tcl']['hosts']['sit2']
                    if page_key_list is not None and len(page_key_list) > 1:
                        self.page_key_list = page_key_list
                    else:
                        self.page_key_list = data['tcl']['mbyq']['page_keys']


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
            f = Request('http://'+ self.host +'/api/order2/pageV2/getPages?fundId=' + str(fundId), headers=headers)
            s = urlopen(f)
            content = s.read()
            if self.origin:
                with open(str(fundId) + '_' + self.funds[fundId] +'_origin.json', 'w', encoding='UTF-8') as f:
                    f.write(str(content, 'UTF-8'))

            for pageKey in self.page_key_list:
                objects = ijson.items(content, 'data.item')
                for cur in objects:
                    if cur['pageKey'] == pageKey:
                        curJson = json.dumps(cur)
                        file_name = self.path + os.sep + str(fundId) + '_' + self.funds[fundId] + '_' + pageKey + '.json'
                        with open(file_name, 'w') as f:
                            f.write(curJson)
                            print(f'写入文件{file_name}')
                            break


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
                print(file, end="\t")
                
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
                    print(f'{abs_file_name} 非目标文件，跳过')
                    continue
                jsonContent = ''
                with open(abs_file_name, 'r', encoding='utf-8') as f:
                    jsonContent = f.read()
                data_b = jsonContent.encode('utf-8')
                f = Request(url=url, headers = headers, data=data_b)
                s = urlopen(f)
                print(f'{abs_file_name} 上传结果 {s.read()}', end="\r\n")



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


