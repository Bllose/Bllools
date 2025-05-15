

SPECIFIC_PLATFORM = r'?targetPlatform=win32-x64'
PLATFORM_LIST = ['ms-toolsai.jupyter']

def url_builder(publisher, name, version, need) -> str:
    """
    组装下载地址
    """
    base_url = f'https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{publisher}/vsextensions/{name}/{version}/vspackage'
    if need:
        base_url += SPECIFIC_PLATFORM
    return base_url

def url_analysis(info:str) -> str:
    param = info.split()
    pair = param[1].split('.')
    publisher = pair[0]
    name = pair[1]
    return url_builder(publisher, name, param[3], needPlatform(param[1]))

def standardize(origin:str) ->str:
    if '\n' in origin:
        return origin.replace('\n', ' ')
    return origin

def needPlatform(target: str) ->bool:
    if target in PLATFORM_LIST:
        return True
    return False
    

if __name__ == '__main__':
    origin = '''Identifier tomoki1207.pdf Version 1.2.2'''
    print(url_analysis(standardize(origin)))