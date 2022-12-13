import os
import platform
import logging


class Searcher():
    """
    努力找到指定文件
    """
    def __init__(self, name:str):
        self.name = name

    def getDriverPath(self) -> str:
        pathList = ['D:\\etc\\drivers\\'+self.name]
        pathList.append(os.path.join(os.getcwd(), self.name))
        if platform.system().lower() == 'windows':
            pathList.append(os.path.join(os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'], self.name))
        for path in pathList:
            if os.path.exists(path):
                return path
        logging.error('找不到文件%s->%s',self.name, pathList)
        return None
