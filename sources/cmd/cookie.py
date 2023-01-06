import click
import logging
from click_loglevel import LogLevel
from example.sgvo.login_ccp_cs import func_cookie

@click.command()
@click.option("-l", "--log-level", type=LogLevel(), default=logging.WARN)
def getClick(log_level) -> str:
    logging.basicConfig(
        format='%(asctime)s %(levelname)s:%(message)s',
        datefmt='%y-%m-%d %I:%M:%S',
        level=log_level,
    )
    logging.log(log_level, "Log level set to %r", log_level)

    cookies = getCookie()
    cookieStr = "; ".join([str(x) + "=" + str(y) for x, y in cookies.items()])
    print(cookieStr)


@func_cookie()
def getCookie(cookie):
    return cookie

"""
!!
"""
if __name__=='__main__':
    getClick()
