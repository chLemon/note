from pathlib import Path
from typing import List
import re


def check_note_is_correct(note_dir: Path) -> List[str]:
    """
    检查所有的笔记：
    1. 都进行了分类
    2. 文件夹类的笔记，都有一个同名的 md
    """
    non_valid = []

    for note in note_dir.iterdir():
        # 跳过 Doing 文件夹 和 隐藏文件、文件夹
        if (note.name == "&Doing" or note.name.startswith(".")):
            continue
        if not re.match(r".+-.+", note.stem):
            non_valid.append(note.stem)
            continue
        if note.is_dir():
            if not (note / f"{note.stem}.md").exists():
                non_valid.append(note.stem)
    return non_valid


def check_every_note_is_valid(git_path: Path):
    if not git_path.exists():
        print("*    当前机器不存在目录: " + git_path.stem)
        return

    not_classified = check_note_is_correct(git_path / git_path.name)
    if not_classified:
        print(f"{git_path.stem} 中以下文件不正确\n" + "\n".join(not_classified))
    else:
        print(f"{git_path.stem} 全部都已分类")


if __name__ == "__main__":
    check_every_note_is_valid(Path().cwd().parent)
