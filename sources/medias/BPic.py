import os
from PIL import Image


def compress_image(file, outfile='', mb=10, step=10, quality=80):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，MB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """

    o_size = get_size(file)
    im = Image.open(file)
    if o_size <= mb:
        return im, o_size
    outfile = get_outfile(file, outfile)
    while o_size > mb:
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile, get_size(outfile)


def get_outfile(infileName, outfile):
    if outfile != '':
        return outfile

    processor = infileName.split(r'.')
    processor[-2] += '_new'
    return '.'.join(processor)


def get_size(theFileName):
    return os.path.getsize(theFileName)/1024/1024


def deep_walk(theRoot):
    """
    递归查找目录下图片，如果图片大于临界值则进行压缩
    :param theRoot: 根目录
    :return: None
    """
    for root, dirs, files in os.walk(theRoot):
        for file in files:
            path = root + os.sep + file
            if os.path.isdir(path):
                deep_walk(path)
                continue
            compress_image(path)


if __name__ == '__main__':
    # file = r'C:\Users\bllos\Pictures\菲菲李胜\白背\微信图片_20231012044334.jpg'
    # outFile = compress_image(file)
    deep_walk(r'C:\Users\bllos\Pictures\菲菲李胜')