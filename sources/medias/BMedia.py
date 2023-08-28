from moviepy.editor import *
from pymediainfo import MediaInfo
from pydub import AudioSegment
import subprocess
import logging
import os

MOVIE = ['mp4', 'avi']
AUDIO = ['mp3']

class BlloseMedia():

    def __init__(self, absPath):
        if absPath is None or len(absPath) < 1:
            logging.error(f'输入的文件路径{absPath}非法! 无法执行')
            return
        self.abspath = absPath

        PATH = os.sep
        if os.sep not in absPath:
            if '/' in absPath:
                PATH = '/'
            elif '\\' in absPath:
                PATH = '\\'

        self.file_type = self.abspath.split('.')[-1]
        self.file_name = self.abspath.split('.')[-2].split(PATH)[-1]
        self.cur_root = self.abspath[0: self.abspath.rfind(PATH)]

        if self.file_type in MOVIE:
            self.clip = VideoFileClip(self.abspath)

        if self.file_type in AUDIO:
            if self.file_type == 'mp3':
                self.mp3 = AudioSegment.from_mp3(self.abspath)

    def extract_audio(self, newPath: str):
        """
        从视频中提取音频
        """
        if newPath is not None and len(newPath) > 0:
            logging.debug("Do some check")
        else:
            newPath = self.abspath + '.mp3'
        self.clip.audio.write_audiofile(newPath)

    def conversion_to_mp4(self):
        if self.abspath.endswith(".mkv"):
            subprocess.call(['ffmpeg', '-i', self.abspath, '-codec', 'copy', self.abspath + '.mp4'])

    def cut(self, start, end, newPath):
        if ':' in start:
            holder = start.split(':')
            if len(holder) == 2:
                start = holder[0] * 60 + holder[1]

        if ':' in end:
            holder = end.split(':')
            if len(holder) == 2:
                end = holder[0] * 60 + holder[1]

        root = self.cur_root + os.sep + self.file_name
        if not os.path.exists(root):
            os.makedirs(root)

        import uuid
        newFileName = root + os.sep + self.file_name + str(uuid.uuid1()).replace('-', '') + '.' + self.file_type
        self.mp3[start * 1000: end * 1000].export(newFileName, format=self.file_type)
        logging.info(f'{newFileName} has been done!')

if __name__ == '__main__':
    t = r'D:\CET\202303CET4\Listening.mp3'
    # video = VideoFileClip(t).subclip(0,5.5)
    # video.audio.write_audiofile(f'{t}.mp3')
    # media_info = MediaInfo.parse(t)
    # print(media_info.to_json())
    b = BlloseMedia(t)
    b.cut('1:40', '1:43', r'D:\CET\202303CET4\Listening')

