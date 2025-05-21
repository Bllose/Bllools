import os
import zipfile
import argparse
from pathlib import Path
from tqdm import tqdm
import shutil

def get_folder_size(folder_path):
    """获取文件夹总大小（字节）"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # 跳过符号链接
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def compress_folder(folder_path, output_zip_path, chunk_size=1024*1024*10):
    """
    压缩指定文件夹到ZIP文件，并拆分为多个子文件
    
    参数:
    - folder_path: 待压缩的文件夹路径
    - output_zip_path: 输出ZIP文件的基础路径（不带扩展名）
    - chunk_size: 每个子文件的大小（字节），默认10MB
    """
    folder_path = os.path.abspath(folder_path)
    base_zip_path = os.path.abspath(output_zip_path)
    
    # 创建临时ZIP文件
    temp_zip_path = f"{base_zip_path}.zip"
    
    # 获取文件夹大小用于进度显示
    total_size = get_folder_size(folder_path)
    processed_size = 0
    
    # 创建ZIP文件
    with zipfile.ZipFile(temp_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        print(f"正在压缩文件夹: {folder_path}")
        for root, dirs, files in os.walk(folder_path):
            for file in tqdm(files, desc="添加文件"):
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(folder_path))
                zipf.write(file_path, arcname)
                processed_size += os.path.getsize(file_path)
    
    # 获取ZIP文件大小
    zip_size = os.path.getsize(temp_zip_path)
    print(f"压缩完成，总大小: {zip_size / (1024*1024):.2f} MB")
    
    # 计算需要拆分的块数
    num_parts = (zip_size + chunk_size - 1) // chunk_size
    print(f"准备拆分为 {num_parts} 个子文件，每个子文件大小: {chunk_size / (1024*1024):.2f} MB")
    
    # 创建输出目录
    output_dir = os.path.dirname(base_zip_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # 拆分ZIP文件
    part_paths = []
    with open(temp_zip_path, 'rb') as f:
        for i in range(num_parts):
            part_path = f"{base_zip_path}.part{i+1:03d}"
            part_paths.append(part_path)
            
            with open(part_path, 'wb') as part_f:
                # 最后一块可能不足chunk_size
                remaining = zip_size - (i * chunk_size)
                part_size = min(chunk_size, remaining)
                
                # 使用进度条显示拆分进度
                with tqdm(total=part_size, desc=f"创建子文件 {i+1}/{num_parts}") as pbar:
                    while part_size > 0:
                        read_size = min(4096, part_size)
                        data = f.read(read_size)
                        if not data:
                            break
                        part_f.write(data)
                        part_size -= read_size
                        pbar.update(read_size)
    
    # 删除临时ZIP文件
    os.remove(temp_zip_path)
    
    print(f"拆分完成！创建了 {num_parts} 个子文件。")
    return part_paths

def merge_and_extract(part_files, output_dir=None):
    """
    合并多个子文件并解压回原始文件夹
    
    参数:
    - part_files: 子文件路径列表（按顺序）
    - output_dir: 解压目标目录，默认为子文件所在目录下的extracted文件夹
    """
    if not part_files:
        raise ValueError("子文件列表不能为空")
    
    # 确定基础ZIP路径
    base_zip_path = os.path.commonprefix(part_files).rstrip('.')
    temp_zip_path = f"{base_zip_path}.zip"
    
    # 合并子文件
    print(f"正在合并 {len(part_files)} 个子文件...")
    with open(temp_zip_path, 'wb') as out_f:
        for i, part_file in enumerate(part_files):
            if not os.path.exists(part_file):
                raise FileNotFoundError(f"子文件不存在: {part_file}")
            
            part_size = os.path.getsize(part_file)
            with open(part_file, 'rb') as part_f:
                with tqdm(total=part_size, desc=f"合并子文件 {i+1}/{len(part_files)}") as pbar:
                    while True:
                        data = part_f.read(4096)
                        if not data:
                            break
                        out_f.write(data)
                        pbar.update(len(data))
    
    # 确定解压目录
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(base_zip_path), "extracted")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 解压ZIP文件
    print(f"正在解压到: {output_dir}")
    with zipfile.ZipFile(temp_zip_path, 'r') as zipf:
        # 获取ZIP文件中的所有文件和文件夹
        members = zipf.infolist()
        total_files = len(members)
        
        # 计算总大小用于进度显示
        total_size = sum(info.file_size for info in members)
        processed_size = 0
        
        for i, info in enumerate(tqdm(members, desc="解压文件")):
            zipf.extract(info, output_dir)
            processed_size += info.file_size
    
    # 删除临时ZIP文件
    os.remove(temp_zip_path)
    
    print(f"解压完成！文件已提取到: {output_dir}")
    return output_dir

def main():
    parser = argparse.ArgumentParser(description="文件夹压缩拆分与合并解压工具")
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # 创建压缩命令
    compress_parser = subparsers.add_parser('compress', help='压缩文件夹并拆分为多个子文件')
    compress_parser.add_argument('source_folder', help='要压缩的源文件夹路径')
    compress_parser.add_argument('output_base', help='输出子文件的基础路径（不带扩展名）')
    compress_parser.add_argument('-s', '--chunk-size', type=int, default=10*1024*1024, 
                               help='每个子文件的大小（字节），默认5MB')
    
    # 创建解压命令
    extract_parser = subparsers.add_parser('extract', help='合并子文件并解压')
    extract_parser.add_argument('part_files', nargs='+', help='要合并的子文件路径列表')
    extract_parser.add_argument('-o', '--output-dir', help='解压目标目录，默认为extracted')
    
    args = parser.parse_args()
    
    if args.command == 'compress':
        compress_folder(args.source_folder, args.output_base, args.chunk_size)
    elif args.command == 'extract':
        merge_and_extract(args.part_files, args.output_dir)

if __name__ == "__main__":
    main()