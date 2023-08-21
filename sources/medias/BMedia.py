import moviepy.editor as mp


def extract_audio(videos_file_path : str):
    """
    从视频中提取音频
    """
    my_clip = mp.VideoFileClip(videos_file_path)
    my_clip.audio.write_audiofile(f'{videos_file_path}.mp3')


if __name__ == '__main__':
    videos_file_path = r'C:\Users\bllos\Videos\TubeGet\How to Learn a British Accent Fast (Modern RP).mp4'
    extract_audio(videos_file_path)
