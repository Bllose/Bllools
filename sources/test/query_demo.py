import cmd

class Query(cmd.Cmd):
    intro = '查询样例\n'
    prompt = 'query> '

    def do_query_by_id(self, arg):
        '通过id查询'
        self.query_by_id(arg)

    def query_by_id(self, id):
        print(f'查询id为{id}的用户信息')

    def do_exit(self, _):
        '退出'
        exit(0)

if __name__ == '__main__':
    Query().cmdloop()