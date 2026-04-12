lfrom pathlib import Path
from py_scripts.models.readme_content import ReadmeContent
from py_scripts.models.note import Note


README_FILE_NAME = "README.md"
DOING_DIR_NAME = "_Doing"


def get_all_notes(note_dir: Path, base_path: Path) -> list[Note]:
    """获取Path目录下，所有的笔记列表和分类列表

    笔记只会直接位于 note_dir 下

    Args:
        note_dir (Path): 笔记目录
        base_path (Path): 基础路径，用于计算相对路径
    Returns:
        笔记列表
    """
    notes = []

    # 获取文件夹下的所有内容
    for note_file in note_dir.iterdir():
        if note_file.name == DOING_DIR_NAME:
            continue
        if note_file.is_dir():
            # 如果是文件夹，在文件夹下，一定有一个同名文件
            note_file = note_file / (note_file.stem + ".md")
        note = Note.parse_from_path(note_file, base_path)
        # 临时兼容一下之前没有分类的笔记
        if note:
            notes.append(note)
    return notes


def update_readme_file(git_path: Path):
    """
    更新当前笔记仓库下的 README.md 文件

    每个笔记仓库，主要是以下2个文件夹，需要整理到 README 中：
        - _Doing: 近期正在处理的一些东西
        - 笔记仓库同名文件夹 note_dir: 已完成的笔记，同时作为坚果云同步的笔记文件夹

    每个笔记的名称格式为：分类-名称.md
    此处的分类为一级分类，在 README.md 里，可以人工添加二级分类，在更新时，已有的二级分类需要保留不变
    """
    git_name = git_path.name
    readme_path = git_path / README_FILE_NAME
    note_dir = git_path / git_name

    if not readme_path.exists():
        print("*    当前机器不存在目录: " + git_name)
        return

    # 1. 读取老 README 文件内容
    last_readme_content = ReadmeContent.read_from_md_path(readme_path)

    # 2. 读取文件
    # 2.1 Doing 目录下所有的内容
    doing_notes = get_all_notes(note_dir / DOING_DIR_NAME, git_path)

    # 2.2 笔记目录下所有的一级目录名（不包含 Doing）
    notes = get_all_notes(note_dir, git_path)

    # 2.3 更新二级目录
    old_notes = last_readme_content.parse_note_part()
    Note.update_second_category(doing_notes, old_notes)
    Note.update_second_category(notes, old_notes)

    # 3. 更新 readme_content 的 note_part
    last_readme_content.new_note_part(doing_notes, notes)

    # 4. 生成新的 readme 文件内容
    new_content = last_readme_content.to_markdown()

    # 5. 写回文件
    with open(readme_path, "w", encoding="utf-8", newline="\n") as file:
        file.write(new_content)
    print(git_name + " 的 README 已更新完毕")
