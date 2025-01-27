import urllib.request
import winreg

def get_windows_proxy_settings():
    proxy_settings = {
        "proxy_enabled": False,
        "proxy_server": None,
        "proxy_bypass": None
    }
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
        proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
        if proxy_enable:
            proxy_settings["proxy_enabled"] = True
            proxy_server, _ = winreg.QueryValueEx(key, "ProxyServer")
            proxy_settings["proxy_server"] = proxy_server
            proxy_bypass, _ = winreg.QueryValueEx(key, "ProxyOverride")
            proxy_settings["proxy_bypass"] = proxy_bypass
        winreg.CloseKey(key)
    except (FileNotFoundError, OSError, ValueError):
        pass
    return proxy_settings

proxy_info = get_windows_proxy_settings()
if proxy_info["proxy_enabled"]:
    proxy_handler = urllib.request.ProxyHandler({
        'http': f'http://{proxy_info["proxy_server"]}',
        'https': f'http://{proxy_info["proxy_server"]}'
    })
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)
    print(f'已设置代理服务器: {proxy_info["proxy_server"]}')

url = 'https://www.okx.com/api/v5/account/balance'

# 构建请求对象
req = urllib.request.Request(url)

# 添加请求头，这里可以根据实际需求添加更多的请求头信息
req.add_header('OK-ACCESS-KEY', '2ea9f72a-41a3-48ce-80bb-a4390cc6c9bd')
req.add_header('OK-ACCESS-PASSPHRASE', 'Rcedwcx1!')
# req.add_header('User-Agent', 'Apifox/1.0.0 (https://apifox.com)')
req.add_header('OK-ACCESS-TIMESTAMP', '2025-01-27T06:33:07.189Z')
req.add_header('OK-ACCESS-SIGN', 'XQzoLHtQ/yqRHbp7PAEKFxvua/201PaueyDRDTsONgs=')
# req.add_header('Accept', '*/*')
# req.add_header('Host', 'www.okx.com')
# req.add_header('Connection', 'keep-alive')
# req.add_header('Cookie', 'locale=en-US; __cf_bm=qCPi2n5OVrkUqYH4aIlUIc1w8bqbOBhu7UwT9AvlSQw-1737958626-1.0.1.1-oTL91CcCoamNZrYA9uPPAXYEHJVHSVjOtSo73aG7Pl2TvftaV_TWZe_z0wbp7xSeS0A_DiaUXi2FxjSCEXzkzA')

try:
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))
except urllib.error.URLError as e:
    print(f"请求出错: {e}")