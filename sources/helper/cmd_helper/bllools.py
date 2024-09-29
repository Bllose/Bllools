import cmd2
import logging
from helper import json_helper
from rich import print_json

class bllools(cmd2.Cmd):
    intro = 'bllose 的工具集'
    prompt = 'handler> '
    FORMAT = '%(asctime)s %(levelname)-10s %(name)-30s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    load_parser = cmd2.Cmd2ArgumentParser()
    load_parser.add_argument('-f', '--function', default= 'null', type=str, help='指定需要处理的内容')
    load_parser.add_argument('-j', '--jsonStr', default= '{}', type=str, help='指定需要处理的内容')

    @cmd2.with_argparser(load_parser)
    def do_json(self, args):
        if 'null' in args.function or 'None' in args.function:
            json_str = args.jsonStr
            result = json_helper.remove_all_None_value(json_str)
            print(f'raw: {result}')
            print_json(result)

if __name__ == '__main__':
    bllools().cmdloop()
