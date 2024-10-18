from helper.config.config_type import type
import sys
import os
import logging

class config():
    def __init__(self, typeList = [type.FILE, type.ENV, type.SYS]):
        self.typeList = typeList
        self.config = {}

    def load(self):
        for curType in self.typeList:
            match curType:
                case type.FILE:
                    self.loadFileConfig()
                case type.SYS:
                    self.loadSystemConfig()
                case type.ENV:
                    self.loadEnvironmentConfig()
        return self

    def loadFileConfig(self):
        """
        最大可能性加载文件配置
        1、首先在当前执行文件所在目录找
        2、然后再运行环境所在目录找
        3、在根目录找
        """

        # 当前文件的绝对路径
        exe_path = sys.argv[0]
        # 当前文件所在目录
        current_file_parent = os.path.dirname(exe_path)
        current_work_place = os.getcwd()
        default_config_file_list = ['config.yml', 'config.yaml']
        loaded_config_file_list = []
        for cur_file in default_config_file_list:
            absPath = current_file_parent + os.sep + cur_file
            if os.path.exists(absPath):
                self.loadingTheFile(absPath, cur_file)
                loaded_config_file_list.append(cur_file)
                break
            
            absPath = current_work_place + os.sep + cur_file
            if os.path.exists(absPath):
                if self.loadingTheFile(absPath, cur_file):
                    loaded_config_file_list.append(cur_file)
                    break

        logging.debug(f'加载配置文件完成, 生效文件 {loaded_config_file_list}')

    def loadingTheFile(self, absPath, cur_file):
        suffix = cur_file.split('.')[-1].lower()
        match suffix:
            case 'yml' | 'yaml':
                self.load_yaml_config_file(absPath)
                return True
            case 'xml':
                pass
        return False

    def load_yaml_config_file(self, absPath: str) -> None:
        """
        加载yml文件, 读取配置信息，并填充到 config 对象中
        """
        logging.debug(f'当前加载配置文件 -> {absPath}')
        import yaml

        with open(absPath, 'r', encoding='utf-8') as file:  
            yaml_config = yaml.safe_load(file)
            self.config.update(yaml_config)
            logging.debug(f'加载配置文件{absPath}完成\r\n一共加载配置{len(yaml_config)}项')



    def loadSystemConfig(self):
        pass

    def loadEnvironmentConfig(self):
        pass

    def hasConfig(self, key) -> bool:
        return key in self.config
    
    def get(self, key):
        """
        尝试从配置池中获取配置
        若存在则返回配置 key 所对应的 value
        否则返回 None
        """
        if self.hasConfig(key):
            return self.config[key]
        else:
            return None
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    myConfig = config([type.FILE])
    myConfig.load()
    app_id = myConfig.get('eqb.pro.appId')
    print(app_id)
