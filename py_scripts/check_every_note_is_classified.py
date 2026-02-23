from pathlib import Path
from typing import List
import re


def check_note_read_me_is_classified(git_path: Path) -> List[str]:
    """
    检查所有的笔记都进行了分类
    """
    # 直接通过 README 判断即可
    note_path = git_path / git_path.name
    non_classified = []
    for note in note_path.iterdir():
        if note.name != "&Doing" and not re.match(r"(.*?)-(.*)", note.stem):
            non_classified.append(note.stem)
    return non_classified


def check_every_note_is_classified(git_path: Path):
    if not git_path.exists():
        print("*    当前机器不存在目录: " + git_path.stem)
        return

    not_classified = check_note_read_me_is_classified(git_path)
    if not_classified:
        print(f"{git_path.stem} 中以下文件没有被分类\n" + "\n".join(not_classified))
    else:
        print(f"{git_path.stem} 全部都已分类")


if __name__ == "__main__":
    check_every_note_is_classified(Path().cwd().parent)
