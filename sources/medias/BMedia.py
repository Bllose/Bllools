from moviepy.editor import *
from pymediainfo import MediaInfo
from pydub import AudioSegment
import subprocess
import logging
import os
import json

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

        """
        持续性编辑参数
        """
        self.cutting = None
        self.left = 0
        self.right = 0
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", "-show_format", self.abspath]
        result = subprocess.check_output(cmd)
        metadata = json.loads(result.decode('utf-8'))

        for stream in metadata.get('streams'):
            if stream.get('codec_type') == 'video':
                self.video_code = stream.get('codec_name')
                self.video_code_full_name = stream.get('codec_long_name')
            elif stream.get('codec_type') == 'audio':
                self.audio_code = stream.get('codec_name')
                self.audio_code_full_name = stream.get('codec_long_name')
        logging.debug(f'{self.file_name} has been loaded, {self.video_code}, {self.audio_code}')
        # print(json.dumps(metadata, sort_keys=True, indent= 4, separators=(',', ':')))

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
            # subprocess.call(['ffmpeg', '-i', self.abspath, '-codec', 'copy', self.abspath + '.mp4'])'
            '''
            -i 文件路径
            -c:v 视频流
            -c:a 音频流
            '''
            subprocess.call(['ffmpeg', '-i', self.abspath, '-c:v', 'copy', '-c:a', 'aac', self.abspath + '.mp4'])
        else:
            logging.warning(f'暂时无法将{self.file_type}转为mp4; {self.file_name}')

    def cut(self, start, end, newPath = None):
        intStart = 0
        intEnd = 0
        if ':' in start:
            holder = start.split(':')
            if len(holder) == 2:
                intStart = int(holder[0]) * 60 + int(holder[1])
        else:
            intStart = int(start)

        if ':' in end:
            holder = end.split(':')
            if len(holder) == 2:
                intEnd = int(holder[0]) * 60 + int(holder[1])
        else:
            intEnd = int(end)

        root = self.cur_root + os.sep + self.file_name
        if not os.path.exists(root):
            os.makedirs(root)

        import uuid
        if newPath:
            newFileName = newPath + os.sep + self.file_name + str(uuid.uuid1()).replace('-', '') + '.' + self.file_type
        else:
            newFileName = root + os.sep + self.file_name + str(uuid.uuid1()).replace('-', '') + '.' + self.file_type
        self.left = intStart
        self.right = intEnd
        self.mp3[intStart * 1000: intEnd * 1000].export(newFileName, format=self.file_type)
        logging.info(f'{newFileName} has been done!')
        self.cutting = newFileName
        self.playAudioCutting()

    def playAudioCutting(self):
        from playsound import playsound
        if not self.cutting:
            raise BMediaError(102, '缺少正在处理的媒体，无法播放')
        playsound(self.cutting)

    def continueCutting(self, loffset: int, roffset: int):
        if not self.cutting:
            raise BMediaError(101, '缺少正在处理的媒体，无法继续剪辑!')

        self.mp3[(self.left + loffset) * 1000: (self.right + roffset) * 1000]\
            .export(self.cutting, format=self.file_type)

        self.left = self.left + loffset
        self.right = self.right + roffset
        self.playAudioCutting()

    def doneCutting(self):
        if os.sep in self.cutting:
            target = self.cutting.split(os.sep)
        elif '/' in self.cutting:
            target = self.cutting.split('/')
        elif '\\' in self.cutting:
            target = self.cutting.split('\\')

        target[-1] = self.file_name + '_' + str(self.left) + '~' + str(self.right) + '.' + self.file_type
        self.mp3[self.left * 1000: self.right * 1000].export(os.sep.join(target), format=self.file_type)


class BMediaError(Exception):
    def __init__(self, status, message):
        super().__init__(message, status)
        self.status = status
        self.message = message


def convert_all_of(path: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            cur = root + os.sep + file
            if not os.path.isfile(cur):
                continue
            b = BlloseMedia(cur)
            b.conversion_to_mp4()
    logging.info(f'转化MP4任务完成: {path}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    target = r'D:\DowntonAbbey'
    # convert_all_of(target)
    b = BlloseMedia(r'D:\DowntonAbbey\Downton.Abbey.S01E01.Chi_Eng.BD-HDTV.AC3.1024X576.x264-YYeTs.mkv')
    # b.conversion_to_mp4()


