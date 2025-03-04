import http.client
import ssl
import json
from bllonfig.Config import bConfig

context = ssl._create_unverified_context()

@bConfig()
def get_token(config, mobile:str = '', password:str = '') -> str:
   """
   模拟登录，获取token
   """
   
   if 'mobanyinqin' in config:
      mobanyinqin = config['mobanyinqin']
      me = mobanyinqin['me']
      mobile = me['mobile']
      password = me['password']

   conn = http.client.HTTPSConnection("aurora-test6-jg-pv.tclpv.com", context=context)
   payload = json.dumps({
      "mobile": mobile,
      "password": password
   })
   headers = {
      'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
      'Content-Type': 'application/json',
      'Accept': '*/*',
      'Host': 'aurora-test6-jg-pv.tclpv.com',
      'Connection': 'keep-alive'
   }
   conn.request("POST", "/api/web/qh/login/", payload, headers)
   res = conn.getresponse()
   data = res.read()
   responseJson = json.loads(data.decode('utf-8'))
   return responseJson['data']['token']



def get_pages(token:str = '', fundId:str = '134') -> list:
   """
   通过产品编号获取对应模版引擎页面key与name
   """
   resultList = []

   conn = http.client.HTTPSConnection("aurora-test6-jg-pv.tclpv.com", context=context)
   payload = ''
   headers = {
      'Cookie': f'xkKey={token}',
      'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
      'Accept': '*/*',
      'Host': 'aurora-test6-jg-pv.tclpv.com',
      'Connection': 'keep-alive'
   }
   conn.request("GET", f"/api/order2/pageV2/getPages?fundId={fundId}", payload, headers)
   res = conn.getresponse()
   data = res.read()
   pageV2 = json.loads(data.decode("utf-8"))
   pageV2List = pageV2['data']
   for page in pageV2List:
      resultList.append({
         'pageName': page['pageName'],
         'pageKey': page['pageKey']
      })
   return resultList

if __name__ == '__main__':
   token = get_token()
   print(get_pages(token))