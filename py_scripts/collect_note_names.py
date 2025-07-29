from pathlib import Path


readme_file_name = "README.md"
doing_dir_name = "&Doing"


def valid_file(file_name: str):
    """
    无用文件，主要是 . 开头的隐藏文件夹 和 Doing
    """
    return file_name != doing_dir_name and not file_name.startswith(".")


def concat_dir_files(dir: Path):
    """
    生成 Path 下所有文件名的列表

    Returns:
        str, str: 拼接好的文件列表，和分类信息
    """
    if not dir.exists():
        return "", ""
    # 特殊逻辑兼容，Journal 现在没有整理，把所有文件都收集起来
    if dir.name == "Journal":
        items = [file.stem for file in dir.rglob("*.md")]
    else:
        items = [file.stem for file in dir.iterdir() if valid_file(file.name)]
    # items 排序，让文件列表稳定
    items.sort()
    categories = {item.split("-")[0] for item in items if "-" in item}
    return "\n".join(f"+ {item}" for item in items), "、".join(categories)


def update_readme_file(git_path: Path):
    """
    更新当前笔记仓库下的 README.md 文件

    每个笔记仓库，主要是以下2个文件夹，需要整理到 README 中：
    &Doing: 近期正在处理的一些东西
    笔记仓库同名文件夹 note_dir: 已完成的笔记，同时作为坚果云同步的笔记文件夹
    """

    git_name = git_path.name

    if not git_path.exists():
        print("*    当前机器不存在目录: " + git_name)
        return

    readme_path = git_path / readme_file_name
    note_dir = git_path / git_name

    # 读取 README 文件内容，保留分隔符前的部分
    with open(readme_path, "r", encoding="utf-8") as file:
        content = file.read()
    splitter = "------------------------------------------------------"
    content = content[: content.find(splitter) + len(splitter)] + "\n\n"

    # 1. Doing 目录下所有的内容
    doing_items, doing_categories = concat_dir_files(note_dir / doing_dir_name)
    # 2. 笔记目录下所有的一级目录名（不包含 Doing）
    note_items, note_categories = concat_dir_files(note_dir)

    def concat_content(title: str, categories: str, items: str):
        if items == "":
            return ""
        res = "## " + title + "\n\n"
        if categories != "":
            res += "类别列表：" + categories + "\n\n"
        return res + items + "\n\n"

    content += concat_content("Doing", doing_categories, doing_items)
    content += concat_content("列表", note_categories, note_items)

    # 写回文件
    with open(readme_path, "w", encoding="utf-8", newline="\n") as file:
        file.write(content)
    print(git_name + " 的 README 已更新完毕")


def collect_note_names(note_git_path: Path):
    """
    这三个 git 文件夹通常都在一起，我决定将这个 py 文件放在 Note 中，一次性更新所有的笔记仓库的README
    """
    parent_path = note_git_path.parent
    update_readme_file(parent_path / "Journal")
    update_readme_file(note_git_path)
    update_readme_file(parent_path / "Secret_note")


if __name__ == "__main__":
    collect_note_names(Path.cwd().parent)
