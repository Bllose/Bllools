import cmd2
from tcl.mobanyinqin import mbyq
import datetime
import os
import sys
import logging

logger = logging.getLogger(__name__)

class Handler(cmd2.Cmd):
    intro = '指定具体的产品范围和pageKey范围, 下载或上传对应的JSON配置!\n'
    prompt = 'handler> '

    FORMAT = '%(asctime)s %(levelname)-10s %(name)-30s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    load_parser = cmd2.Cmd2ArgumentParser()
    load_parser.add_argument('-l', '--loglevel', type=int, default=40, help='设置日志等级DEBUG:10; INFO:20; WARNING:30; ERROR:40(DEFUALT)')
    load_parser.add_argument('-p', '--pageKey', type=str, help='指定具体的pageKey下载')
    load_parser.add_argument('-f', '--fundId', type=str, help='指定具体的产品ID下载，比如光鑫宝-共富 就填 129')
    load_parser.add_argument('-e', '--env', type=str, default='', help='环境可选dev, sit, uat, pro')
    
    @cmd2.with_argparser(load_parser)
    def do_fetch_tabs(self, args):
        '获取指定的栏位内容'

        if not hasattr(self, 'origin'):
            self.origin = False
        if args.pageKey is not None and len(args.pageKey) > 0:
            self.page_key_list = args.pageKey.split(',')
            if hasattr(self, 'mbyqClient'):
                self.mbyqClient.set_page_key_list(self.page_key_list)
        if args.fundId is not None and len(args.fundId) > 0:
            self.fund_list = args.fundId.split(',')
            if hasattr(self, 'mbyqClient'):
                self.mbyqClient.set_fund_list(self.fund_list)
        self.init_client()
        
        if args.env is not None and len(args.env) > 1:
            logger.debug(f'加载自定义环境: {args.env}')
            self.do_select_host(args.env)
        self.mbyqClient.get(fund_list=self.fund_list)

    def do_select_host(self, args):
        '''
        通过环境选择host
        '''
        theHost = self.config['tcl']['host'][args]
        self.mbyqClient.set_host(host=theHost)

    def do_push(self, args):
        self.init_client()

        filter = args.split(',')
        self.mbyqClient.push(filter)

    def init_client(self):
        """
        如果不存在客户端，则初始化一个
        """
        if not hasattr(self, 'mbyqClient'):
            if not hasattr(self, 'host'):
                self.do_set_host()
            if not hasattr(self, 'path'):
                self.input_path()
            if not hasattr(self, 'page_key_list'):
                self.input_page_keys()
            if not hasattr(self, 'token'):
                self.do_set_token()
            if not hasattr(self, 'origin'):
                self.origin = False
            if not hasattr(self, 'fund_list'):
                logger.warning('未指定产品, 默认使用5号产品 129:光鑫宝-共富')
                self.fund_list = [129]
            self.mbyqClient = mbyq(host=self.host, 
                                token=self.token, 
                                path=self.path, 
                                origin=self.origin,
                                page_key_list=self.page_key_list,
                                funds=self.fund_list)
            self.mbyqClient.set_log_level(self.loglevel)
            
    def refresh_client(self):
        """
        强制刷新客户端
        """
        self.mbyqClient = mbyq(host=self.host, 
                                token=self.token, 
                                path=self.path, 
                                origin=self.origin,
                                page_key_list=self.page_key_list)

    """
    一下部分是通过 input 拦截，
    提醒用户输入指定参数的逻辑
    """
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
            envs = [key for key in self.config['tcl']['host'].keys()]
            hosts = [value for value in self.config['tcl']['host'].values()]
            tokens = [value for value in self.config['tcl']['token'].values()]

            print('选择或者输入想要选择的服务器↓')
            for x in range(len(envs)):
                print(str(x) + '\t' + envs[x], end='\r\n')

            msg = input('请选择如上选项或者直接输入host: ')
            if len(msg) == 1:
                index = int(msg)
                self.host = hosts[index]
                self.token = tokens[index]
            elif msg in envs:
                self.host = self.config['tcl']['host'][msg]
                self.token = self.config['tcl']['token'][msg]
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
        if args is None or len(args) < 1:
            return
        self.token = args
        if hasattr(self, 'mbyqClient'):
            self.mbyqClient.set_token(self.token)
    
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

    def do_set_host(self, args:str = None):
        '''
        直接给参数可以直接指定host
        否则提供选项进行选择
        '''
        self.input_host(args)

    def do_reset_path(self, args):
        '''
        自定义工作路径
        '''
        if args is None or len(args) < 1:
            logger.warning(f'未输入路径，路径保持不变')
            return
        if not os.path.exists(args):
            logger.warning(f'路径{args}非法！请核对后重新设置')
            return
        self.path = args
        logger.info(f'当前工作路径为: {self.path}')
    
    def do_change_log(self, args:int = 20):
        '''
        重新定义日志级别 10:debug; 20:info; 30:warning; 40:error
        '''
        self.init_client()
        try:
            theLevel = int(args.args)
        except Exception as e:
            logger.error(f'日志等级需要配置 10~60 的数字! 当前配置值{args.args}非法')
            return
        self.mbyqClient.set_log_level(theLevel)
        self.loglevel = theLevel


    def do_exit(self, _):
        '''
        退出当前工作空间
        '''
        exit(0)

    
    init_parser = cmd2.Cmd2ArgumentParser()
    init_parser.add_argument('-l', '--loglevel', type=int, default=20, help='设置日志等级DEBUG:10; INFO:20; WARNING:30; ERROR:40(DEFUALT)')
    
    @cmd2.with_argparser(init_parser)
    def do_init(self, args):
        """
        用来初始化关键参数的逻辑
        """
        logger.setLevel(level=int(args.loglevel))
        self.loglevel = int(args.loglevel)
        logger.setLevel(level=self.loglevel)

        # 当前文件的绝对路径
        exe_path = sys.argv[0]
        # 当前文件所在目录
        current_work_dir = os.path.dirname(exe_path)
        logger.debug(f'获取当前文件所在目录: {current_work_dir}')

        configYml = 'mbyq_config.yml'
        absYmlPath = current_work_dir + os.sep + configYml
        relativePath = './' + configYml
        if os.path.isfile(absYmlPath):
            self.load_config_file(configYml, absYmlPath)
        elif os.path.isfile(absYmlPath):
            self.load_config_file(configYml, relativePath)
        else:
            logger.error(f'获取不到配置文件，请输入配置文件绝对路径。当前解析文件失败↓\r\n绝对路径:{absYmlPath} \r\n 相对路径:{relativePath}')  
            absYmlPath = input('请重新输入配置文件绝对路径: ')
            self.load_config_file(configYml, absYmlPath)

    def load_config_file(self, configYml, absYmlPath):
        try:
            with open(absYmlPath, 'r', encoding='utf-8') as f:
                config = f.read()
                logger.debug(f'开始加载配置文件: {absYmlPath}')
                if config is not None and len(config) > 1:
                    import yaml
                    data = yaml.safe_load(config)
                    logger.info(f'通过文件 {configYml} 加载相关配置')
                    self.init(data)
                    self.config = data
        except Exception as e:
            try:
                with open(configYml, 'r', encoding='utf-8') as f:
                    config = f.read()
                    logger.debug(f'开始加载配置文件: {configYml}')
                    if config is not None and len(config) > 1:
                        import yaml
                        data = yaml.safe_load(config)
                        print(f'通过文件 {configYml} 加载相关配置')
                        self.init(data)
                        self.config = data
            except Exception as e1:
                print(f'加载配置文件失败: {configYml}')


    def init(self, data: dict):
        if 'host' in data:
            self.host = data['tcl']['host']['uat']
        if 'token' in data:
            self.token = data['token']
        if 'path' in data:
            self.path = data['path']
            if self.path is not None and len(self.path) > 1:
                self.path = self.path + os.sep + str(datetime.date.today()).replace('-', '')
        if 'tcl' in data:
            self.page_key_list = data['tcl']['mbyq']['page_keys']
        
        if 'fund' in data:
            if data['fund'] is not None:
                fundStr = str(data['fund']).strip()
                if len(fundStr) > 1:
                    self.fund_list = [int(x.strip()) for x in fundStr.split(',')]
        if not hasattr(self, 'fund_list') or len(self.fund_list) < 1:
            self.fund_dict = {112: '光富宝',115: '光鑫宝',128: '光盈宝',129: '光鑫宝-共富',130: '光富宝-同裕',131: '光瑞宝',132: '整村汇流',133: '公共屋顶',134: '光悦宝',135: '光煜宝-全款建站',136: '光煜宝-融资建站'}
            self.fund_list = [key for key in self.fund_dict.keys()]



if __name__ == '__main__':
    Handler().cmdloop()
        