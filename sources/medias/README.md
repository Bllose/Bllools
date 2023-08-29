# 依赖软件
[ImageMagick](http://www.imagemagick.org/script/download.php)   
[ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/)  

## 系统环境配置
IMAGEMAGICK_BINARY -> magick.exe  
FFMPEG_BINARY -> ffmpeg.exe  
Path 下增加ffmpeg的安装地址，比如 ffmpeg/bin   

# 使用案例

``` Python
from medias import BMedia as a
b = a.BlloseMedia(r'C:\workspace\English\2018年6月四级听力(第一套).mp3')
b.cut('1:28', '1:35')
b.continueCutting(4, 0)
b.continueCutting(-6, 0)
b.continueCutting(1, 0)
b.continueCutting(1, 0)
b.continueCutting(1, 0)
b.playAudioCutting()
b.doneCutting()
```
每次进行剪切会播放一下剪切内容， 上面示例多次调用```continueCutting```就是听了文件后做微调。  
最终完成后调用```doneCutting```输出截取文件。

