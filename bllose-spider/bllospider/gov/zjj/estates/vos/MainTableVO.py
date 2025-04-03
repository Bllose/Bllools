from dataclasses import dataclass, field
from bllospider.gov.zjj.estates.vos.SeatInfoVO import SeatInfoVO
from typing import List
import json

@dataclass
class MainTableVO:

    # 主表格数据 - 开始
    # 序号
    index: int = -1
    # 预售证号
    cert_num: str = ""
    cert_path: str = ""
    # 项目名称
    project_name: str = ""
    project_path: str = ""
    # 开发企业
    enterprice_name: str = ""
    # 所在区
    district: str = ""
    # 批准时间
    approval_time: str = ""
    # 主表格数据 - 结束

    # 当前项目套房信息 - 开始
    seat_info_list: List[SeatInfoVO] = field(default_factory=list)

    def add_seat_info(self, seat_info: SeatInfoVO):
        self.seat_info_list.append(seat_info)
    # 当前项目套房信息 - 结束

    @staticmethod
    def builder():
        return MainTableVOBuilder()

    @staticmethod
    def build_url(base_url: str, path: str) -> str:
        """构建完整URL
        Args:
            base_url: 基础URL
            path: URL路径
        Returns:
            完整的URL字符串
        """
        if not base_url:
            return path
        if not path:
            return base_url
        
        # 去除base_url末尾的斜杠和path开头的斜杠，然后用单个斜杠连接
        base_url = base_url.rstrip('/')
        path = path.lstrip('/')
        return f"{base_url}/{path}"

    def __str__(self):
        """重写 __str__ 方法，将对象转换为 JSON 字符串"""
        # 创建一个字典来存储所有属性
        data = self.__dict__.copy()
        # 将seat_info_list中的对象转换为字典
        data['seat_info_list'] = [vars(seat_info) for seat_info in self.seat_info_list]
        return json.dumps(data, ensure_ascii=False)

    def __repr__(self):
        """
        重写 __repr__ 方法，将对象转换为 JSON 字符串
        """
        return self.__str__()

class MainTableVOBuilder:
    def __init__(self):
        self.vo = MainTableVO()
    
    def with_index(self, index: int) -> 'MainTableVOBuilder':
        self.vo.index = index
        return self

    def with_cert(self, num: str, path: str = "", pre_url: str = "") -> 'MainTableVOBuilder':
        self.vo.cert_num = num
        self.vo.cert_path = MainTableVO.build_url(pre_url, path)
        return self

    def with_project(self, name: str, path: str = "", pre_url: str = "") -> 'MainTableVOBuilder':
        self.vo.project_name = name
        self.vo.project_path = MainTableVO.build_url(pre_url, path)
        return self

    def with_enterprise(self, name: str) -> 'MainTableVOBuilder':
        self.vo.enterprice_name = name
        return self

    def with_district(self, district: str) -> 'MainTableVOBuilder':
        self.vo.district = district
        return self

    def with_approval_time(self, time: str) -> 'MainTableVOBuilder':
        self.vo.approval_time = time
        return self

    def build(self) -> MainTableVO:
        return self.vo



