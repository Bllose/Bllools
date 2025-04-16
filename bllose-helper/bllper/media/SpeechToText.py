import speech_recognition as sr
from pydub import AudioSegment
import traceback
import os

def mp3_to_wav(mp3_file_path, wav_file_path):
    """
    将 MP3 文件转换为 WAV 文件
    :param mp3_file_path: MP3 文件路径
    :param wav_file_path: 转换后的 WAV 文件路径
    """
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_file_path, format="wav")

def speech_to_text(wav_file_path, proxy_url=None):
    """
    将语音文件转换为文字
    :param wav_file_path: WAV 文件路径
    :param proxy_url: 代理服务器地址，格式如 "http://127.0.0.1:7918"
    :return: 识别出的文字内容
    """
    r = sr.Recognizer()
    with sr.AudioFile(wav_file_path) as source:
        audio = r.record(source)
    try:
        # 设置代理环境变量
        if proxy_url:
            os.environ['http_proxy'] = proxy_url
            os.environ['https_proxy'] = proxy_url
        text = r.recognize_google(audio, language='zh-CN')
        return text
    except sr.UnknownValueError:
        print("无法识别语音")
        traceback.print_exc()
    except sr.RequestError as e:
        print(f"请求错误; {e}")
        traceback.print_exc()
    finally:
        # 清除代理环境变量
        if proxy_url:
            os.environ.pop('http_proxy', None)
            os.environ.pop('https_proxy', None)
    return None

if __name__ == "__main__":
    mp3_file = r'D:\temp\output.mp3'  # 替换为实际的 MP3 文件路径
    wav_file = 'temp_audio.wav'
    proxy = "http://127.0.0.1:7897"  # 设置本地代理

    # 将 MP3 转换为 WAV
    # mp3_to_wav(mp3_file, wav_file)

    # 进行语音识别
    result = speech_to_text(wav_file, proxy)
    if result:
        print("识别结果:")
        print(result)