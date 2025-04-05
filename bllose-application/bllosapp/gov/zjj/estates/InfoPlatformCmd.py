import cmd2
import logging
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from bllospider.gov.zjj.estates.info_platform import fetch_main_table_data, \
                                                     fetch_seat_info_list, \
                                                     fetch_room_detail_info, \
                                                     export_excel, \
                                                     closeDriver
class InfoPlatformCmd(cmd2.Cmd):
    intro = '住建局信息平台数据爬取工具 \r\n \
输入命令 >>> fetch  获取序号为1的项目信息 \r\n \
输入命令 >>> fetch -s 5 获取序号为5的项目信息 \r\n \
输入命令 >>> fetch -s 10 -l 10 从序号10开始，一共获取10个项目信息 \r\n \
输入命令 >>> fetch -l -1 获取所有项目信息，慎用，因为数量庞大，爬取时间会很久 \r\n \
输入命令 >>> fetch -d 使用最大单页页幅20/页，默认单页10条'
    prompt = '>>> '

    fetch_parser=cmd2.Cmd2ArgumentParser()
    fetch_parser.add_argument('-l', '--limit', type=int, default=1, help='获取信息条数限制，默认为1，获取全部数据请设置为-1')
    fetch_parser.add_argument('-s', '--start', type=int, default=1, help='起始序号，默认为1')
    fetch_parser.add_argument('-d', '--double', action='store_true', help='使用最大单页页幅20/页，默认单页10条')
    fetch_parser.add_argument('-i', '--information', action='store_true', help='打印详细信息')
    @cmd2.with_argparser(fetch_parser)
    @cmd2.with_category('数据抓取')
    def do_fetch(self, args):
        """
        爬取信息平台数据
        """
        if args.information:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        limit = args.limit
        start = args.start
        mainTableList = fetch_main_table_data(
                                        startIndex = start, 
                                        page_limit= -1, 
                                        index_limit= limit,
                                        max_page= args.double
                                        )
        logging.info(f"主表信息获取完毕，信息总条数：{len(mainTableList)}")

        counter = fetch_seat_info_list(mainTableList)
        logging.info(f"套房信息获取完毕，信息总条数: {counter}")

        detail_counter = 0
        try:
            detail_counter += fetch_room_detail_info(mainTableList)
            logging.info(f"房间详情信息获取完毕")
        except Exception as e:
            logging.error(f"获取房间详情信息发生错误: {e}")
        finally:
            closeDriver()
            # 无论报了什么错，将已经处理好的信息进行保存
            # 保存excel文件    
        
        outputFileName, _ = export_excel(mainTableList)  
        
        # 渲染结果输出
        urlStyle = Style(color="#0000FF", underline=True)
        result = Text()
        result.append("项目数量: ", style="bold yellow")
        result.append(str(len(mainTableList)), style="italic green")
        result.append("\n")

        result.append("套房数量: ", style="bold yellow")
        result.append(str(counter), style="italic green")
        result.append("\n")

        result.append("房间信息: ", style="bold yellow")
        result.append(str(detail_counter), style="italic green")
        result.append("\n")

        result.append("输出文件: ", style="bold yellow")
        result.append(outputFileName, style=urlStyle)
        
        panel = Panel(result, title="爬取完成")
        console = Console()
        console.print(panel)

if __name__ == '__main__':
    InfoPlatformCmd().cmdloop()

