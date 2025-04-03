from enum import IntEnum
from sre_parse import IN

class TableColumns(IntEnum):
    """表格列索引定义"""
    INDEX = 0             # 序号
    CERT_NUM = 1          # 预售证号
    PROJECT_NAME = 2      # 项目名称
    ENTERPRICE_NAME = 3   # 开发企业
    DISTRICT = 4          # 所在区
    APPROVAL_TIME = 5     # 批准时间