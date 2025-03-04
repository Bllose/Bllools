import os
import shutil
import logging

def copy_files_to_flat_dir(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
        
    file_counts = {}
    
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_file = os.path.join(root, file)
            filename, ext = os.path.splitext(file)
            
            if file in file_counts:
                file_counts[file] += 1
                new_filename = f"{filename}_{file_counts[file]}{ext}"
            else:
                file_counts[file] = 0
                new_filename = file
                
            dst_file = os.path.join(dst_dir, new_filename)
            shutil.copy2(src_file, dst_file)


class FileProcessor:
    def __init__(self, type:str = None):
        """
        @param type: 处理的文件类型
        """
        self.type = type
        if self.type is not None and len(self.type) > 0:
            self.specified = True
        else:
            self.specified = False

    def process_file(self, file_path):
        logging.debug('子类实现该方法，实现自定义的文件处理')
        pass

    def traverse_folder(self, folder_path):
        """
        深度遍历文件夹，并对每个文件调用 process_file 方法
        :param folder_path: 要遍历的文件夹路径
        """
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if self.specified:
                    if file.split('.')[-1] != self.type:
                        continue
                file_path = os.path.join(root, file)
                self.process_file(file_path)


class FileReader:
    def each_row_handler(self, curRow:str):
        logging.debug('子类实现该方法，实现自定义的行处理逻辑')
        pass

    def read_file(self, file_path):
        """
        读取文件，对每一行调用 each_row_handler 方法
        :param file_path: 要读取的文件路径
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                self.each_row_handler(line)


if __name__ == "__main__":
    fp = FileProcessor("java")
    fp.traverse_folder(r'D:\workplace\tclhuaweiyun\2025-02\temp\xk-basic')