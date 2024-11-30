# 校验图片是不是都在md里被引用了
import re
from pathlib import Path
from typing import Set


def collect_pics(md_file_path: Path) -> Set[Path]:
    """
    收集md文件中引用的图片

    return: 一个集合，包含所有被引用的图片文件名
    """
    with open(md_file_path, "r", encoding="utf-8") as file:
        md_content = file.read()
    pattern = r"""\!\[.*\]\((.+)\)"""
    matches = re.findall(pattern, md_content)
    return {md_file_path.parent / Path(url) for url in matches}


def get_all_non_md_files(folder: Path) -> Set[Path]:
    """
    获取指定文件夹下所有非md文件
    """
    if not folder.exists():
        return set()
    return {
        file_path
        for file_path in folder.iterdir()
        if not file_path.name.endswith(".md")
    }


def collect_no_used_pics(single_note_path: Path) -> Set[Path]:
    """
    判断当前笔记目录里，所有图片是不是都是在文档中被引用了
    """
    # 当前目录下的所有文档文件
    md_files = [
        file_path
        for file_path in single_note_path.iterdir()
        if file_path.name.endswith(".md")
    ]
    # 当前目录下的所有图片文件
    pic_files = get_all_non_md_files(single_note_path / "images")
    # 判断是否都被使用了
    pics_in_mds = set()
    for md in md_files:
        pics_in_mds.update(collect_pics(md))
    retains = pic_files - pics_in_mds

    return retains


def check_every_pic_is_used(note_path: Path):
    """
    检查每个图片是否都在笔记中被引用
    笔记大体结构：
    - Note
        - NoteDir
            - note.md
            - images
                - image1.png
                - image2.jpg
    """
    if not note_path.exists():
        print("*    当前机器不存在目录: " + note_path.stem)
        return

    sub_paths = [path for path in note_path.iterdir() if path.is_dir()]
    all_no_used_pics = set()
    for sub_path in sub_paths:
        all_no_used_pics.update(collect_no_used_pics(sub_path))

    if all_no_used_pics:
        print(f"{note_path.stem} 中有图片没有被使用\n" + "\n".join(str(pic) for pic in all_no_used_pics))
    else:
        print(f"{note_path.stem} 中所有图片都被使用了")

if __name__ == "__main__":
    check_every_pic_is_used(Path().cwd().parent / "Note")
