import cmd
from tcl.mobanyinqin import mbyq
import datetime
import os

class Handler(cmd.Cmd):
    intro = '指定具体的产品范围和pageKey范围, 下载或上传对应的JSON配置!\n'
    prompt = 'handler> '

    def do_fetch_tabs(self, args):
        '获取指定的栏位内容'

        if not hasattr(self, 'origin'):
            self.origin = False
        self.init_client()

        if not hasattr(self, 'fund_list'):
            print('未指定产品, 默认使用5号产品 129:光鑫宝-共富')
            self.fund_list = [129]
        self.mbyqClient.get(fund_list=self.fund_list)


    def do_push(self, args):
        self.init_client()

        filter = args.split(',')
        self.mbyqClient.push(filter)

    def init_client(self):
        if not hasattr(self, 'mbyqClient'):
            if not hasattr(self, 'host'):
                self.input_host()
            if not hasattr(self, 'path'):
                self.input_path()
            if not hasattr(self, 'page_key_list'):
                self.input_page_keys()
            if not hasattr(self, 'token'):
                self.input_token()
            if not hasattr(self, 'origin'):
                self.origin = False
        
        self.mbyqClient = mbyq(host=self.host, 
                               token=self.token, 
                               path=self.path, 
                               origin=self.origin,
                               page_key_list=self.page_key_list)

    """
    一下部分是通过 input 拦截，
    提醒用户输入指定参数的逻辑
    """
    def input_token(self):
        msg = input('输入登录token: ')
        while len(msg) < 1:
            msg = input('输入登录token: ')
        self.token = msg
        print(f'token : {self.token}')

    def input_page_keys(self):
        msg = input('输入需要处理的pageKey, 以逗号分隔: ')
        while len(msg) < 1:
            msg = input('输入需要处理的pageKey, 以逗号分隔: ')
        self.page_key_list = [x.strip() for x in msg.split(',')]
        print(f'pageKeys : {self.page_key_list}')

    def input_path(self):
        msg = input('输入本地文件所在路径或直接回车用默认工作空间: ')
        if msg is None or len(msg) < 1:
            self.path = r'/workplace' + os.sep + str(datetime.date.today()).replace('-', '')
        else:
            self.path = msg
        print(f'工作目录: {self.path}')

    def input_host(self, args: str = None):
        if args is None or len(args) < 1:
            print('选择或者输入想要选择的服务器↓')
            hosts = [value for value in self.config['tcl']['host']]
            for x in range(len(hosts)):
                print(str(x) + '\t' + hosts[x], end='\r\n')

            msg = input('请选择如上选项或者直接输入host: ')
            if len(msg) == 1:
                index = int(msg)
                self.host = hosts[index]
            else:
                self.host = msg
        else:
            self.host = args
            
        print(f'使用host: {self.host}')


    """
    以下部分是直接提供给用户调用，
    配置具体参数的逻辑
    """
    def do_set_token(self, args):
        '''
        指定连接模板引擎的token
        请求报文头中的 Authorization:\tBasic amd1c2VyOjEyMzQ1Ng==
        '''
        self.token = args
    
    def do_set_fund(self, args):
        '''
        指定产品范围
        112: 光富宝,115: 光鑫宝,128: 光盈宝,129: 光鑫宝-共富,130: 光富宝-同裕,131: 光瑞宝,132: 整村汇流,133: 公共屋顶,134: 光悦宝,135: 光煜宝-全款建站,136: 光煜宝-融资建站
        直接输入数字，以逗号分隔
        handler> fund 129,134
        意思： 光鑫宝-共富 和 光悦宝
        '''
        self.fund_list = [int(x) for x in args.split(',')]
        
    def do_set_page(self, args):
        '''
        指定查询的pageKey, 以逗号分隔
        枚举如下：
        applyInfo1\timageInfo04\tOrderDetail
        webDesignReview\twebSignReview\timageInfo02
        imageInfoSg4zlAndYg\tarrayBuildImageInfo
        arrayBuildImageInfo1\tarrayBuildImageInfo2
        courtyardBuildImageInfo\tcourtyardBuildImageInfo1
        courtyardBuildImageInfo2\tsunBuildImageInfo
        sunBuildImageInfo1\tsunBuildImageInfo2
        '''
        self.page_key_list = [x for x in args.split(',')]

    def do_set_host(self, args):
        '''
        直接给参数可以直接指定host
        否则提供选项进行选择
        '''
        self.input_host(args)

    def do_exit(self, _):
        exit(0)

    
    """
    用来初始化关键参数的逻辑
    """
    def init_by_config_file(self):
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
                    print(f'通过文件 {configYml} 加载相关配置')
                    self.init(data)
                    self.config = data       
        return self

    def init(self, data: dict):
        if 'host' in data:
            self.host = data['host']
        if 'token' in data:
            self.token = data['token']
        if 'path' in data:
            self.path = data['path']
            if self.path is not None and len(self.path) > 1:
                self.path = self.path + os.sep + str(datetime.date.today()).replace('-', '')
        if 'page' in data:
            if data['page'] is None:
                print('未配置pageKey! 执行前必须补充')
            else:
                self.page_key_list = [x.strip() for x in data['page'].split(',')]
        
        if 'fund' in data:
            if data['fund'] is not None:
                fundStr = str(data['fund']).strip()
                if len(fundStr) > 1:
                    self.fund_list = [int(x.strip()) for x in fundStr.split(',')]
        if not hasattr(self, 'fund_list') or len(self.fund_list) < 1:
            self.fund_dict = {112: '光富宝',115: '光鑫宝',128: '光盈宝',129: '光鑫宝-共富',130: '光富宝-同裕',131: '光瑞宝',132: '整村汇流',133: '公共屋顶',134: '光悦宝',135: '光煜宝-全款建站',136: '光煜宝-融资建站'}
            self.fund_list = [key for key in self.fund_dict.keys()]

if __name__ == '__main__':
    Handler().init_by_config_file().cmdloop()
        