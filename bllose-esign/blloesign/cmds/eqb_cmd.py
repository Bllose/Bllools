import cmd2
from datetime import datetime
from blloesign.cmds.commandSets.sys_command_sets import CustomInitCommandSet
from blloesign.cmds.commandSets.eqb_command_sets import AutoLoadCommandSet
from blloesign.cmds.commandSets.eqb_task_sets import AutoLoadTaskSet
from bllonfig.Config import bConfig
from blloesign.cmds.commandSets.EqbObservable import Observable

class eqb_cmd(cmd2.Cmd, Observable):
    intro = "e签宝相关功能"
    prompt = 'e签宝> '

    @bConfig()
    def __init__(self, *args, config=None, command_sets=None, **kwargs):
        if 'token' not in config:
            raise ValueError("未配置token,无法使用e签宝功能")
        if not self._validate_token(config['token']):
            print("Token is invalid")
            return

        # 将command_sets加入到kwargs中以便传递给父类构造函数
        if command_sets is not None:
            kwargs['command_sets'] = command_sets
        cmd2.Cmd.__init__(self, *args, **kwargs)
        Observable.__init__(self)

        # 定义别名
        self.aliases['flowid'] = 'flowId'
        self.aliases['fileid'] = 'fileId'

        self.eqb_task_set = AutoLoadTaskSet(self)
        self.eqb_command_set = AutoLoadCommandSet(self)
        self.register_observer(self.eqb_task_set)
        self.register_observer(self.eqb_command_set)

        self.register_command_set(self.eqb_task_set)
        self.register_command_set(self.eqb_command_set)
        

    def _update_env(self, new_env):
        self.env = new_env
        self.notify_observers(new_env)

    def _validate_token(self, token):
        if not token:
            return False
        from bllper.tokenHelper import verify_token, PUBLIC_KEY, load_public_key
        is_valid, result = verify_token(load_public_key(PUBLIC_KEY), token)
        if not is_valid:
            raise ValueError("Token is invalid")

        # 获取token中的日期字符串
        expire_date_str = result.split(',')[4]
        
        # 尝试多种常见的日期格式
        date_formats = [
            "%Y-%m-%d",    # 2025-01-24
            "%Y%m%d",      # 20250124
            "%Y/%m/%d",    # 2025/01/24
            "%d/%m/%Y",    # 24/01/2025
            "%m/%d/%Y",    # 01/24/2025
            "%Y.%m.%d"     # 2025.01.24
        ]
        
        expire_date = None
        for date_format in date_formats:
            try:
                expire_date = datetime.strptime(expire_date_str, date_format)
                break
            except ValueError:
                continue
        
        if expire_date is None:
            raise ValueError(f"无法解析日期格式: {expire_date_str}")
            
        if expire_date.date() < datetime.now().date():
            print("Token is out of date!")
            raise ValueError("Token is out of date!")
            
        return is_valid

if __name__ == '__main__':
    # import logging
    # logging.basicConfig(level=logging.DEBUG)
    my_command = CustomInitCommandSet('e签宝')
    eqb_cmd(command_sets=[my_command]).cmdloop()