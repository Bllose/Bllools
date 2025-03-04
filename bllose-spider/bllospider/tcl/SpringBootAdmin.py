import http.client
import ssl
import json

context = ssl._create_unverified_context()

def get_jsessionid(env:str = 'test1'):
    conn = http.client.HTTPSConnection("aurora-admin.tclpv.cn", context=context)
    payload = ''
    headers = {
        'authority': 'aurora-admin.tclpv.cn',
        'method': 'POST',
        'path': f'/{env}/login',
        'scheme': 'https',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'aurora-admin.tclpv.cn',
        'Connection': 'keep-alive',
        'Referer': f'https://aurora-admin.tclpv.cn/{env}/login?username=admin&password=admin123&remember-me=on'
    }
    conn.request("POST", f"/{env}/login?username=admin&password=admin123&remember-me=on", payload, headers)
    res = conn.getresponse()
    for key, value in res.getheaders():
        if key == 'Set-Cookie':
            jsessionid = value.split(';')[0].split('=')[1]
            return jsessionid
        
    return ''

def get_server_info(env:str = 'test1', jsessioinid:str = ''):
    conn = http.client.HTTPSConnection("aurora-admin.tclpv.cn", context=context)
    payload = ''
    headers = {
        'authority': 'aurora-admin.tclpv.cn',
        'method': 'GET',
        'path': f'/{env}/applications',
        'scheme': 'https',
        'accept': 'application/json',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'x-requested-with': 'XMLHttpRequest',
        'Cookie': f'JSESSIONID={jsessioinid}',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Host': 'aurora-admin.tclpv.cn',
        'Connection': 'keep-alive'
    }
    conn.request("GET", f"/{env}/applications", payload, headers)
    res = conn.getresponse()
    data = res.read()
    response = data.decode("utf-8")
    return response

def get_http_address_by_env(env:str = 'test1') -> dict:
    """
    通过指定的环境，获取当前已经注册的服务地址
    :param env: 环境名称
    :return: 返回服务地址的字典，key为服务名称，value为服务地址
    """
    serverList = get_server_info(env,  get_jsessionid(env))
    serverListJson = json.loads(serverList)
    resultMap = {}
    for server in serverListJson:
        resultMap[server['instances'][0]['registration']['name']] = server['instances'][0]['registration']['serviceUrl']
    return resultMap


if __name__ == '__main__':
    print(get_http_address_by_env('test1'))