import cmd2
import json
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from bllper.timeHelper import formatter
from bllper.JsonHelper import deep_clean_null
from bllper.tokenHelper import generate_token_with_expiry, load_private_key_from_file, load_public_key, PUBLIC_KEY, verify_token
from bllper.sysHelper import git_proxy_settings
from blloesign.cmds.commandSets.sys_command_sets import CustomInitCommandSet
from bllospider.tcl.SpringBootAdmin import get_http_address_by_env


class bllose_cmd(cmd2.Cmd):
    intro = "工具集"
    prompt = 'bllose> '

    def __init__(self, *args, command_sets=None, **kwargs):
        # 将command_sets加入到kwargs中以便传递给父类构造函数
        if command_sets is not None:
            kwargs['command_sets'] = command_sets

        super().__init__(*args, **kwargs)
        
        self.console = Console()
        self.aliases['time'] = 'format'

    
    server_info_parser = cmd2.Cmd2ArgumentParser()
    server_info_parser.add_argument('-e', '--env', type=str, default='test3', help='环境名称')
    server_info_parser.add_argument('params', nargs=1, help='服务名称')
    @cmd2.with_argparser(server_info_parser)
    @cmd2.with_category('TCL')
    def do_host(self, args):
        """
        获取TCL环境的服务器信息
        """
        target = args.params[0]
        if target is None or len(target) < 1:
            return
        env =args.env
        response = get_http_address_by_env(env)

        conclusion = Text()    
        for name, url in response.items():
            if target in name:
                conclusion.append(f'{name} -> {url}', style="bold green")
            else:
                conclusion.append(f'{name} -> {url}', style="#808080")
            conclusion.append('\n')
        
        panel = Panel(conclusion, title=f'{env}环境服务器信息', expand=False)
        self.console.print(panel)


    @cmd2.with_category('代理')
    def do_gitproxy(self, args):
        """
        设置git代理
        """
        http_setting_string, https_setting_string = git_proxy_settings()
        if http_setting_string and https_setting_string:
            self.console.print(f'[green]{http_setting_string}[/green]')
            self.console.print(f'[green]{https_setting_string}[/green]')
        else:
            self.console.print('[red]未启用代理服务器[/red]')

    @cmd2.with_category('代理')
    def do_unproxy(self, args):
        """
        取消git代理
        """
        self.console.print('git config --global --unset http.proxy')
        self.console.print('git config --global --unset https.proxy')
    

    json_parser = cmd2.Cmd2ArgumentParser()
    json_parser.add_argument('params', nargs=1, help='json字符串中null对象全部清除掉')
    @cmd2.with_argparser(json_parser)
    @cmd2.with_category('小工具')
    def do_json(self, args):
        target = args.params[0]
        if target is None or len(target) < 1:
            return
        targetJson = json.loads(target)
        self.console.print(f'[green]{deep_clean_null(targetJson)}[/green]')

    format_parser = cmd2.Cmd2ArgumentParser()
    format_parser.add_argument('params', nargs=1, help='将时间戳转化为格式化的时间字符串')
    @cmd2.with_argparser(format_parser)
    @cmd2.with_category('小工具')
    def do_format(self, args):
        """
        将时间戳
        """
        try:
            timestamp = int(args.params[0])
        except ValueError:
            self.console.print(f'[red]入参->{args.params[0]}<-无法解析为时间戳[/red]')
            return
        self.console.print(f'[green]{formatter(timestamp)}[/green]')

    token_parser = cmd2.Cmd2ArgumentParser()
    token_parser.add_argument('days', type=int, help='token有效期天数')
    token_parser.add_argument('--name', type=str, default='临时用户', help='用户名称')
    token_parser.add_argument('--phone', type=str, default='13800138000', help='电话号码')
    token_parser.add_argument('--id_card', type=str, default='110101199001011234', help='身份证号')
    @cmd2.with_argparser(token_parser)
    @cmd2.with_category('认证工具')
    def do_token(self, args):
        """
        生成一个临时token，可以指定有效期天数
        使用示例：
        token 15  # 生成一个15天有效期的默认用户token
        token 30 --name 张三 --phone 13912345678 --id_card 110101199001011234  # 生成一个30天有效期的指定用户token
        """
        try:
            # 加载私钥
            private_pem = load_private_key_from_file()
            if not private_pem:
                self.console.print("[red]错误: 无法加载私钥文件[/red]")
                return

            # 生成token
            token = generate_token_with_expiry(
                private_pem,
                company="BLLOSE",
                name=args.name,
                phone=args.phone,
                id_card=args.id_card,
                days=args.days
            )

            # 验证生成的token
            public_pem = load_public_key(PUBLIC_KEY)
            is_valid, result = verify_token(public_pem, token)
            
            if is_valid:
                self.console.print("\n[green]Token生成成功！[/green]")
                self.console.print(f"[blue]用户信息:[/blue]")
                self.console.print(f"  名称: {args.name}")
                self.console.print(f"  电话: {args.phone}")
                self.console.print(f"  身份证: {args.id_card}")
                self.console.print(f"  有效期: {args.days}天")
                self.console.print("\n[yellow]Token:[/yellow]")
                self.console.print(token)
            else:
                self.console.print("[red]错误: Token验证失败[/red]")

        except Exception as e:
            self.console.print(f"[red]错误: {str(e)}[/red]")


if __name__ == '__main__':    
    my_command = CustomInitCommandSet('bllose')
    bllose_cmd(command_sets=[my_command]).cmdloop()