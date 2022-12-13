import os, logging


def find_files(dir: str, key_words: list):
    for root, dirs, files in os.walk(dir):
        for file in files:
            curFile = open(root + '/' + file, encoding='utf-8')
            lineNum = 0
            curLine = ' '
            while curLine != "":
                lineNum += 1
                try:
                    curLine = curFile.readline()
                except UnicodeDecodeError:
                    logging.warning("{} 文件的编码各式非 utf-8!".format(file))
                    break
                if len(curLine) < 10:
                    continue
                for key in key_words:
                    if key in curLine:
                        print("文件{} 第{}行 包含敏感词汇:{}".format(file, lineNum, curLine))
                        break
        for dir in dirs:
            find_files(dir, key_words)


def replace_files_kes(dir: str, key_words: list):
    for root, dirs, files in os.walk(dir):
        for file in files:
            curFile = open(root + '/' + file, encoding='utf-8', mode="r")
            lineNum = 0
            curLine = ' '
            recorder = []
            while curLine != "":
                lineNum += 1
                try:
                    curLine = curFile.readline()
                except UnicodeDecodeError:
                    logging.warning("{} 文件的编码各式非 utf-8!".format(file))
                    break
                if len(curLine) < 10:
                    continue
                for key in key_words:
                    if key in curLine:
                        curLine = curLine.replace(key, 'Example')
                recorder.append(curLine)
            curFile.close()
            curFile = open(root + '/' + file, encoding='utf-8', mode="w")
            curFile.write(''.join(recorder))

        for dir in dirs:
            find_files(dir, key_words)

if __name__ == '__main__':
    key_word = ['huawei', 'HuaWei', 'cWX', 'cbg', 'ccp', 'tbsd', 'asc', 'jalor', 'rtc', 'Example']
    find_files(r'D:\workplace\temp\bllose-algorithmic-main', key_word)
    # replace_files_kes(r'D:\workplace\temp\LearnStudy-main', key_word)