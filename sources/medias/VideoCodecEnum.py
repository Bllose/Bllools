from enum import Enum


class VideoCE(Enum):
    """
    针对媒体文件所使用的视频编码进行枚举

    Attributes:
        h264: H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10; AVC: Advanced Video Coding
    """

    h264 = 'MPEG-4 part 10'