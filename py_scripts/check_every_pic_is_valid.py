# 校验图片是不是都在md里被引用了
import os
import re
from pathlib import Path

def is_note_dir(paths):
    """
    内部没有文件夹
    """
    return all(not os.path.isdir(path) for path in paths)

def collect_pics(md_file_path):
    """
    收集md文件中引用的图片

    return: 一个集合，包含所有被引用的图片文件名
    """
    with open(md_file_path, 'r', encoding='utf-8') as file:
        md_content = file.read()
    pattern = r'''\!\[.*\]\((.+)\)'''
    matches = re.findall(pattern, md_content)
    return {Path.path(url).name for url in matches}

def get_all_non_md_files(folder):
    """
    获取指定文件夹下所有非md文件
    """
    non_md_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if not file.lower().endswith('.md'):
                non_md_files.append(file)
    return non_md_files

def check(paths):
    """
    判断当前笔记目录里，所有图片是不是都是在文档中被引用了
    """
    # 当前目录下的所有文档文件
    md_files = [path for path in paths if path.endwith('.md')]
    # 当前目录下的所有图片文件
    pic_files = {Path.path(path).name for path in paths if not path.endwith('.md')}
    # 判断是否都被使用了
    pics_in_mds = {}
    for md in md_files:
        pics_in_mds.update(collect_pics(md))
    retains = pic_files - pics_in_mds
    for retain in retains:
        print(retain + "没有被使用")

def rcheck(note_path: str):
    """
    递归检查每个子目录
    """
    if is_note_dir(note_path):
        # 当前目录是 笔记目录
        check(note_path)
        return
    # 当前目录不是 笔记目录
    # 获取当前目录下的所有文件
    note_path = Path(note_path)
    if not note_path.is_dir():
        print(f"{note_path} 不是一个目录")
        return

    sub_paths = [os.path.join(note_path, file) for file in os.listdir(note_path)]
    if(is_note_dir(sub_paths)):
        # 当前目录已经是 笔记目录 了
        check(sub_paths)
    else:
        # 当前目录还是 大目录，递归处理
        map(rcheck, sub_paths)

def check_every_pic_is_valid(note_path: Path):
    """
    检查每个图片是否都在笔记中被引用
    笔记大体结构：
    - Note
        - note.md
        - images
            - image1.png
            - image2.jpg
    """
    rcheck(note_path)

if __name__ == '__main__':
    check_every_pic_is_valid(Path().cwd().parent / 'Note')