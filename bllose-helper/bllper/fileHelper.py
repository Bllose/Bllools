import os
import shutil

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


if __name__ == "__main__":
    copy_files_to_flat_dir("E:\\歌", "D:\\temp\\歌曲")