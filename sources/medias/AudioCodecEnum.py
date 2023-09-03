from enum import Enum


class AudioCE(Enum):
    """
    针对视频所使用的音频编码进行枚举

    Attributes:
        AAC
        DTS
    """
    AAC = 'AAC (Advanced Audio Coding)'
    DTS = 'DCA (DTS Coherent Acoustics)'