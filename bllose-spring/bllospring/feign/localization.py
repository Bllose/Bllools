from __future__ import annotations
from bllper.fileHelper import FileProcessor
from bllospider.tcl.SpringBootAdmin import get_http_address_by_env
import re
import base64
from attr import define, field
from rich.console import Console
from rich.syntax import Syntax



@define
class FeignClientVo:

    """
    FeignClient注解的参数
    通过组建参数对象，重构新的注解参数
    """


    # The service id with optional protocol prefix. 
    name:str = field(default=None)

    # The name of the service with optional protocol prefix.
    value:str = field(default=None)


    # This will be used as the bean name instead of name if present, but will not be used
	# as a service id.
    contextId:str = field(default=None)


    # an absolute URL or resolvable hostname (the protocol is optional).
    url:str = field(default=None)


    # path prefix to be used by all method-level mappings. Can be used with or
	# without <code>@RibbonClient</code>.
    path:str = field(default=None)


    # A custom configuration class for the feign client.
    # Class<?>[] configuration() default {};
    configuration:str = field(default=None)


    def __str__(self) -> str:

        """

        重写 __str__ 方法，返回对象的字符串表示形式，值为空则不展示

        """

        attributes = []

        if self.name is not None:
            attributes.append(f'name="{self.name}"')
        if self.value is not None:
            attributes.append(f'value="{self.value}"')
        if self.contextId is not None:
            attributes.append(f'contextId="{self.contextId}"')

        if self.url is not None:
            attributes.append(f'url="{self.url}"')
        if self.path is not None:
            attributes.append(f'path="{self.path}"')
        if self.configuration is not None:
            attributes.append(f'configuration={self.configuration}')

        return ", ".join(attributes)


    def buildByAnnotationParams(self, paramString: str) -> FeignClientVo:

        """
        解析注解参数
        @FeignClient("service1")
        @FeignClient(name = "service1")
        """

        # 先格式化参数配置，将回车、注释等相关内容剔除出去

        paramString = self.preFormatting(paramString)


        builder = FeignClientVo()

        if not ',' in paramString and not '=' in paramString:
            # 没有逗号也没有等号，说明只有一个参数，直接赋值给 value
            builder.value = paramString
            return builder


        paramPairs = paramString.split(',')

        for pair in paramPairs:
            kv = pair.split('=')
            key = kv[0].strip()
            value = kv[1].strip()
            

            if 'null' in value.lower():
                continue

            if value.startswith('"'):
                value = value[1:]

            if value.endswith('"'):
                value = value[:-1]

            if value.startswith('base64'):
                value = value.replace('base64', '')
                value = base64.b64decode(value).decode('utf-8')


            if key == 'name':
                builder.name = value

            elif key == 'value':
                builder.value = value

            elif key == 'contextId':
                builder.contextId = value

            elif key == 'url':
                builder.url = value

            elif key == 'path':
                builder.path = value

            elif key == 'configuration':
                builder.configuration = value

        return builder
    

    def preFormatting(paramString: str) -> str:

        """
        对参数进行预处理，去除换行符、回车符、空格、制表符
        """

        # 解决形如：configuration = {CommonClient.Configuration.class, CommonClient.MessageConfiguration.class} 的配置问题

        regex = r'[^,=]+=\s*({.+})'
        matches = re.findall(regex, paramString, re.DOTALL)

        if matches:
            for match in matches:
                if ',' in match:
                    # 将该段str转化为base64编码
                    encoded_str = 'base64' + base64.b64encode(match.encode('utf-8')).decode('utf-8')
                    paramString = paramString.replace(match, encoded_str)


        regex = r'/\*.+\*/'
        # 使用 re.sub() 函数替换匹配到的内容为空字符串
        paramString = re.sub(regex, '', paramString, flags=re.DOTALL)

        # 避免匹配到 http:// 直接匹配以 // 开头的行
        regex = r'(?<!:)//.+\n'

        # 使用 re.sub() 函数替换匹配到的内容为空字符串
        paramString = re.sub(regex, '', paramString, flags=re.DOTALL)

        # 先替换换行符
        paramString = paramString.replace('\n', '')

        # 再替换回车符
        paramString = paramString.replace('\r', '')
        
        return paramString
        


# 定义正则表达式模式，使用 re.DOTALL 让 . 匹配换行符
pattern = r'(@FeignClient\((.+?)\))'


class FeignLocalization(FileProcessor):

    def __init__(self, type:str = None, env:str = 'test3'):

        """
        @param type: 处理的文件类型
        @param env: 环境变量 test1 ~ test10
        """

        super().__init__(type)
        self.env = env
        self.hostMap = self.targetEnvHttpAddress()
        self.successList = []
        self.failedList = []
        self.notFeignClientList = []
        self.console = Console()
        self.checkList = []


    def init(self):

        self.successList = []
        self.failedList = []
        self.checkList = []
        self.notFeignClientList = []

    def refreshEnv(self, env:str):

        self.env = env
        self.hostMap = self.targetEnvHttpAddress()

    def getTheFeignAnnouncePart(self, content: str) -> str:
        # 将文本按行分割成列表
        lines = content.splitlines()

        # 查找 @FeignClient 所在的行号
        feign_client_index = next((i for i, line in enumerate(lines) if "@FeignClient" in line), None)

        if feign_client_index is not None:
            # 计算上下 5 行的范围
            start_index = max(0, feign_client_index - 5)
            end_index = min(len(lines), feign_client_index + 6)

            # 提取指定范围的代码行
            new_lines = lines[start_index:end_index]

            # 将提取的代码行组合成新的字符串
            new_string = '\n'.join(new_lines)
            return new_string

        return content

    def jls_extract_def(self, content, file_path):
        """
        组装用于检查的信息，并存入列表中
        将以 @FeignClient 作为基准，上下五行一起提取出来展示
        """
        syntax = Syntax(self.getTheFeignAnnouncePart(content), "java", theme="monokai")
        # self.console.print(syntax)
        self.checkList.append({file_path: syntax})
        return syntax


    def process_file(self, file_path):
        successFlag = False

        try:
            # 打开文件，使用 'r' 模式表示只读
            with open(file_path, 'r', encoding='utf-8') as file:
                # 读取文件的全部内容
                content = file.read()
                matches = re.findall(pattern, content, re.DOTALL)

                if matches:
                    feignClientVo = FeignClientVo.buildByAnnotationParams(FeignClientVo, paramString = matches[0][1])
                    hostKey = feignClientVo.value if feignClientVo.value else feignClientVo.name
                    if hostKey not in self.hostMap:
                        self.failedList.append({file_path: "未找到对应的host"})
                        return
                    feignClientVo.url = self.hostMap[hostKey]
                    print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
                    print(matches[0][1], '->',feignClientVo.__str__())
                    print("↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑")
                    content = content.replace(matches[0][1], feignClientVo.__str__())
                    successFlag = True
                else:
                    self.notFeignClientList.append({file_path: "未找到FeignClient注解"})


            if successFlag:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                    syntax = self.jls_extract_def(content, file_path)
                self.successList.append(file_path)
        except FileNotFoundError:
            print("文件未找到，请检查文件路径。")


    def targetEnvHttpAddress(self):
        return get_http_address_by_env(self.env)


    def printSuccessesResult(self, total:bool = True):

        if len(self.successList) == 0:
            print("没有成功的文件")
            return

        if not total:
            print("成功的文件列表:")
            for item in self.successList:
                print(item)

        else:
            print(f"成功的文件数量: {len(self.successList)}")


    def printFailedResult(self, total:bool = False):

        if len(self.failedList) == 0:
            print("没有未适配的文件")
            return
        

        if not total:
            print("未适配的文件列表:")
            for item in self.failedList:
                print(item)

        else:
            print(f"未适配的文件数量: {len(self.failedList)}")
        print(f'非FeignClient注解的文件数量: {len(self.notFeignClientList)}')


    def checkTheResult(self):

        if len(self.checkList) == 0:
            print("没有需要检查的文件")
            return

        print("需要检查的文件列表:")
        index = 0
        for item in self.checkList:
            index += 1
            for key, value in item.items():
                self.console.print(f'文件: {key}')
                self.console.print(value)
            

            commend = input(f'一共有文件{len(self.checkList)}个,当前准备检查第{index}个,回车继续,q退出')
            if commend == 'q':
                return
        



if __name__ == "__main__":
    fp = FeignLocalization("java", 'test6')
    fp.traverse_folder(r'D:\workplace\tclhuaweiyun\2025-02\temp\xk-order2')
    fp.printSuccessesResult()
    fp.printFailedResult()
    fp.checkTheResult()