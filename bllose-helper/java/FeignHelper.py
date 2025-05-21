from bllper.fileHelper import FileProcessor

class JavaFileModifier(FileProcessor):
    def __init__(self, type:str = None):
        super().__init__(type)
    
    def process_file(self, file_path):
        # 这里我们只处理文本文件（以 .txt 结尾）
        if file_path.endswith('.java'):
            try:
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 对文件内容进行修改，这里简单地在文件末尾添加一行文本
                new_content = content + "\nThis line is added by the modifier."

                # 将修改后的内容写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                print(f"Modified file: {file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")    

if __name__ == '__main__':
    modifier = JavaFileModifier()
    modifier.traverse_folder(r'D:\workplace\tclhuaweiyun\2025-02\temp\xk-basic')