import os
from pydub import AudioSegment
import traceback

class AudioProcessor:
    def __init__(self, input_file):
        self.input_file = input_file
        self.audio = None

    def load_audio(self):
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"音频文件不存在: {self.input_file}")
        self.audio = AudioSegment.from_file(self.input_file)
        return self

    def get_audio_info(self):
        if not self.audio:
            raise ValueError("请先加载音频文件")
        return {
            "duration": len(self.audio),  # 音频时长（毫秒）
            "sample_rate": self.audio.frame_rate,  # 采样率
            "channels": self.audio.channels  # 声道数
        }

    def _time_to_ms(self, time_str):
        """将时间字符串转换为毫秒数
        支持格式：mm:ss 或 hh:mm:ss
        """
        parts = time_str.split(':')
        if len(parts) == 2:  # mm:ss
            minutes, seconds = map(int, parts)
            return (minutes * 60 + seconds) * 1000
        elif len(parts) == 3:  # hh:mm:ss
            hours, minutes, seconds = map(int, parts)
            return (hours * 3600 + minutes * 60 + seconds) * 1000
        else:
            raise ValueError("时间格式错误，请使用 mm:ss 或 hh:mm:ss 格式")

    def split_audio(self, start_time=None, segment_length=None):
        """从指定时间点开始切割音频
        :param start_time: 开始时间点，格式为 mm:ss 或 hh:mm:ss
        :param segment_length: 切割长度（毫秒），如果不指定则切到结尾
        """
        if not self.audio:
            raise ValueError("请先加载音频文件")
        
        start_ms = self._time_to_ms(start_time) if start_time else 0
        duration = len(self.audio)
        
        if start_ms >= duration:
            raise ValueError("开始时间超出音频长度")
            
        if segment_length is not None:
            end_ms = min(start_ms + segment_length, duration)
            return self.audio[start_ms:end_ms]
        return self.audio[start_ms:duration]

    def adjust_volume(self, dB):
        if not self.audio:
            raise ValueError("请先加载音频文件")
        self.audio = self.audio + dB
        return self

    def export(self, output_path, format="mp3"):
        if not self.audio:
            raise ValueError("请先加载音频文件")
        self.audio.export(output_path, format=format)

def process_audio_example():
    try:
        # 使用相对于当前文件的路径
        current_dir = r'D:\temp'
        input_file = os.path.join(current_dir, "input.aac")
        output_file = os.path.join(current_dir, "output.mp3")

        processor = AudioProcessor(input_file)
        processor.load_audio()
        
        # 获取音频信息
        audio_info = processor.get_audio_info()
        print(f"音频信息: {audio_info}")

        # 从8分50秒开始切割音频
        segments = processor.split_audio(start_time="8:50")
        processor.audio = segments
        
        # 调整音量
        processor.adjust_volume(6)
        
        # 导出音频
        processor.export(output_file)
        print(f"音频处理完成，已保存到: {output_file}")

    except FileNotFoundError as e:
        print(f"错误: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"处理音频时发生错误: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    process_audio_example()