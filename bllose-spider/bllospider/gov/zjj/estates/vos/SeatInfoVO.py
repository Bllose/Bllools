from dataclasses import dataclass
import json

@dataclass
class SeatInfoVO:
    """
    套房信息VO
    """
    # 项目名称
    projectName: str = ""

    # 销售类型：预售/现售
    saleType: str = ""

    # 座号
    seatNum: str = ""

    # 层号
    floorNum: str = ""

    # 房间号
    roomNum: str = ""

    # 房间出售状态
    roomStatus: str = ""

    # 房间详情路径
    roomInfoPath: str = ""

    # 项目楼栋情况
    projectBuildingInfo: str = ""

    # 用途
    use: str = ""

    # 是否无障碍住房
    isAccessibility: str = ""

    # 拟售价格（按建筑面积计）
    price: str = ""

    # 拟售价格（按套内建筑面积计）
    price2: str = ""

    # 合同号
    contractNum: str = ""

    # 预售查丈建筑面积
    area: str = ""
    # 预售查丈套内建筑面积
    area2: str = ""
    # 预售查丈分摊面积
    area3: str = ""

    # 竣工查丈建筑面积
    area4: str = ""
    # 竣工查丈套内建筑面积
    area5: str = ""
    # 竣工查丈分摊面积
    area6: str = ""

    # def to_json(self):
    #     return json.dumps(self, ensure_ascii=False)

    # def __str__(self):
    #     return self.to_json()

    # def __repr__(self):
    #     return self.to_json()