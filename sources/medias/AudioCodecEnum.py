from enum import Enum


class AudioCE(Enum):
    """
    针对视频所使用的音频编码进行枚举

    Attributes:
        AAC
        DTS
        AC3
    """
    AAC = 'AAC (Advanced Audio Coding)'
    DTS = 'DCA (DTS Coherent Acoustics)'
    AC3 = 'ATSC A/52A (AC-3)'

