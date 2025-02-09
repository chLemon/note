# 校验图片是不是都在md里被引用了
import os
import re
from pathlib import Path

def is_note_dir(paths):
    """内部没有文件夹"""
    return all(not os.path.isdir(path) for path in paths)

def list_paths(path: str):
    """返回文件夹内全部的路径"""
    return [os.path.join(path, file) for file in os.listdir(path)]

def rcheck(note_path: str):
    """递归检查"""
    sub_paths = list_paths(note_path)
    if(is_note_dir(sub_paths)):
        # 当前目录已经是 笔记目录 了
        check(sub_paths)
    else:
        # 当前目录还是 大目录，递归处理
        map(rcheck, sub_paths)

def collect_pics(md_path):
    with open(md_path, 'r', encoding='utf-8') as file:
        md_content = file.read()
    pattern = r'''\!\[.*\]\((.+)\)'''
    matches = re.findall(pattern, md_content)
    return {Path.path(url).name for url in matches}

def check(paths):
    """判断当前笔记目录里，所有图片是不是都是在文档中被引用了"""
    md_files = [path for path in paths if path.endwith('.md')]
    pic_files = {Path.path(path).name for path in paths if not path.endwith('.md')}
    pics_in_mds = {}
    for md in md_files:
        pics_in_mds.update(collect_pics(md))
    retain = pic_files - pics_in_mds
    for i in retain:
        print(i)


# 定义
note_path = './Note/'
rcheck(note_path)