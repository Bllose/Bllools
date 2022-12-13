import datetime, click, logging
from logging import DEBUG,INFO,WARNING,ERROR
from typing import Tuple
from click_loglevel import LogLevel
from example.tbsd.PrivateInfoManager import analyLoginInfo


@click.command()
@click.option('-d', '--dir', default='.', help='保存文件路径，默认为当前路径')
@click.option("-l", "--log-level", type=LogLevel(), default=INFO, help='日志打印级别, 默认为info, 如果遇到问题, 尝试使用debug运行看看')
@click.option('-t', '--team', help='迭代周期，请通过 --level debug 执行文件，并按照提示填写 ID')
@click.option('-a', '--add', default='f', help='是否包含最近两周的总代码量, 即是否完成本周工作是只计算最新一周还是计算最近两周')
@click.option('-e', '--exceed', default='f', help='是否要跨越统计，即加上上个月末尾的数据一起统计。一般而言会有第一周跨越上个月的情况')
@click.option('-s', '--specific', type= float, default = -1.0, help='重新指认合格代码量')
def task_cmd(
        dir: str,
        log_level,
        team: str,
        add: str,
        exceed: str,
        specific: float
) -> None:
    # 预备逻辑 开始
    logging.basicConfig(
        format='%(asctime)s %(levelname)s:%(message)s',
        datefmt='%y-%m-%d %I:%M:%S',
        level=log_level,
    )
    logging.log(log_level, "Log level set to %r", log_level)

    dir, template_file = pre_checker(dir)
    username, password = analyLoginInfo('USERNAME_W3', 'PSW_W3')
    # 预备逻辑 结束

    isExceed = False if exceed == 'f' else True
    '''
    通过爬虫，将工作完成导出文件下载下来
    '''
    from example.tbsd import download_uadp
    cc = download_uadp.CodingCounter(username, password, team=team, saved_path= dir, exceed=isExceed)

    import time
    for team in cc.getTeamList():
        offeringPbi = cc.export_request(team)
        while (not cc.file_list(offeringPbi)):
            time.sleep(5)

    # 所有 uadp文件均保存在当前目录下， 后续由jar完成初步统计
    downloadedFilesList = cc.download()

    # for theFile in downloadedFilesList:
    #     click.echo("开始处理文件：{}".format(theFile))
    from example.tbsd.ParseSilentAchievement import ParseSilentAchievement, establishRecordFile
    import os, re
    employeeFileName = ''
    for root, dirs, files in os.walk(dir, topdown=False):
        for file in files:
            if re.search('[0-9]{12}\.xlsx', file):
                employeeFileName = root + os.sep + file

    if employeeFileName != '':
        psa = ParseSilentAchievement(downloadedFilesList, datetime.datetime.now(), employeeFileName)
        saList = psa.processing()

        er = establishRecordFile(saList=saList,
                                 saveDir= dir,
                                 initFile= dir + r'\init.xlsx',
                                 level=DEBUG)
        if add == 'f':
            er.establishBody(add=False, specific=specific)
        else:
            er.establishBody(add=True, specific=specific)
    else:
        click.echo('ERROR: 缺少员工文件! PS: 202202181423.xlsx 任务失败终止')

    '''
    将原始导出文件清理出当前目录，方便下次运行
    '''
    clean(dir=dir)

# 清理历史UADP文件
def clean(dir:str) -> None:
    import os
    old_file_path = dir + os.path.sep + 'oldFiles'
    if not os.path.exists(old_file_path) :
        os.mkdir(old_file_path)

    pattern = '(UADP.+xlsx)'
    import re
    for root, dirs, files in os.walk(dir):
        for curFile in files:
            if 'UADP' in curFile:
                searcher = re.search(pattern, curFile)
                oldFileName = os.path.join(old_file_path, searcher.group(1))
                if os.path.exists(os.path.join(dir, curFile)):
                    os.rename(os.path.join(dir, curFile), oldFileName)


def pre_checker(
        dir:str
) -> Tuple[str, str]:

    if dir == '.':
        import os
        dir = os.getcwd()
        click.echo('使用当前路径:{}'.format(dir))

    template_file = dir + os.path.sep + 'init.xlsx'

    return dir, template_file


# 返回创建的文档名称
def call_jar(
        dir:str,
        log:int
) -> str:
    import os
    os.chdir(dir)
    click.echo('当前执行目录:{}'.format(os.getcwd()))
    instructure = 'java -jar SilentAchievement-2.13.05.jar'
    if log == 0:
        instructure += ' > jar.log'
    jar = os.system(instructure)
    if jar == 0:
        import os, re, time
        pattern = time.strftime("%Y-%m", time.localtime()) + '月静默达成.xlsx'
        for root, dirs, files in os.walk('.'):
            for file in files:
                matcher = re.search(pattern, file)
                if matcher:
                    click.echo('识别并使用文件: {}'.format(pattern))
                    return os.path.abspath(root + os.path.sep + file)
            raise Exception('未能搜索到文件{}, 请检查jar文件是否可以正常运作'.format(pattern))


if __name__ == '__main__':
    # clean(r'D:\etc\Python\Python39_64\Lib\bllools\gj\cmds')
    task_cmd()

