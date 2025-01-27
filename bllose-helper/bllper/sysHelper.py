import psutil
import winreg

def get_windows_proxy_settings():
    proxy_settings = {
        "proxy_enabled": False,
        "proxy_server": None,
        "proxy_bypass": None
    }

    try:
        # 打开用户级别的 Internet 设置注册表项
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")

        # 获取代理启用状态
        proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
        if proxy_enable:
            proxy_settings["proxy_enabled"] = True

            # 获取代理服务器地址
            proxy_server, _ = winreg.QueryValueEx(key, "ProxyServer")
            proxy_settings["proxy_server"] = proxy_server

            # 获取绕过代理的地址列表
            proxy_bypass, _ = winreg.QueryValueEx(key, "ProxyOverride")
            proxy_settings["proxy_bypass"] = proxy_bypass

        winreg.CloseKey(key)
    except (FileNotFoundError, OSError, ValueError):
        pass

    return proxy_settings


def git_proxy_settings():
    """
    获取当前系统代理设置，并返回适用于 Git 的代理设置字符串
    """
    proxy_settings = get_windows_proxy_settings()
    if proxy_settings["proxy_enabled"]:
        http_setting_string = f'git config --global http.proxy http://{proxy_settings["proxy_server"]}'
        https_setting_string = f'git config --global https.proxy http://{proxy_settings["proxy_server"]}'
        return http_setting_string, https_setting_string
    else:
        return None, None


def main():
    port = input("请输入要检查的端口号: ")
    port = int(port)
    found = False
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            found = True
            pid = conn.pid
            process = psutil.Process(pid)
            print(f"应用程序名称: {process.name()}")
            print(f"应用程序路径: {process.exe()}")
            print(f"进程 ID: {pid}")
            choice = input("是否杀死该进程? (y/n): ")
            if choice.lower() == 'y':
                try:
                    process.kill()
                    print("进程已成功杀死。")
                except psutil.NoSuchProcess:
                    print("进程已经不存在。")
                except psutil.AccessDenied:
                    print("没有权限杀死该进程。")
                except Exception as e:
                    print(f"杀死进程时出错: {e}")
    if not found:
        print(f"未找到占用端口 {port} 的应用程序。")


if __name__ == "__main__":
    # 调用函数获取代理设置
    proxy_info = get_windows_proxy_settings()
    print("代理是否启用:", proxy_info["proxy_enabled"])
    print("代理服务器地址:", proxy_info["proxy_server"])
    print("绕过代理的地址列表:", proxy_info["proxy_bypass"])
