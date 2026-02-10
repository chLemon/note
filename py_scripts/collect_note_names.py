from pathlib import Path
from collections import defaultdict
from pydantic import BaseModel, Field
import re


README_FILE_NAME = "README.md"
DOING_DIR_NAME = "&Doing"

SPLITTER = "------------------------------------------------------"


class TopCategoryInfo(BaseModel):
    notes: list[Path] = Field(description="没有子分类的笔记")
    sub_categories_to_notes: defaultdict[str, list[Path]] = Field(
        description="手动子分类的笔记"
    )
    sub_categories: list[str] = Field(description="子分类列表")


class BaseGroup(BaseModel):
    categories_to_notes: dict[str, TopCategoryInfo] = Field(description="分类和笔记")
    categories: list[str] = Field(description="分类列表")


class ReadmeContent(BaseModel):
    """README 的文件结构"""

    description: str | None = Field(default=None, description="描述")
    doing_group: BaseGroup | None = Field(default=None, description="Doing")
    note_group: BaseGroup | None = Field(default=None, description="列表")

    def parse(self, content: str):
        remain_idx = content.find(SPLITTER) + len(SPLITTER)
        self.description = content[:remain_idx] + "\n\n"
        content_list = content.split('\n')

        self.doing_group = BaseGroup(categories=[], categories_to_notes=defaultdict())
        self.note_group = BaseGroup(categories=[], categories_to_notes=defaultdict())

        i = remain_idx
        cur_group = self.doing_group
        cur_level = 1
        while i < len(content_list):
            line = content_list[i]
            if match := re.search("## 列表", line):
                # 该处理下一组
                cur_group = self.note_group
            elif match := re.search(r"^### (.*)", line):
                # 一级目录
                cur_top_category_info = cur_group.categories_to_notes[match.group(1)]
                cur_level = 1
            elif match := re.search(r"^#### (.*)", line):
                # 二级目录
                cur_sub_category_list = cur_top_category_info.sub_categories_to_notes[
                    match.group(1)
                ]
                cur_level = 2
            elif match := re.search(r"+ \[.*\]\((.*)\)", line):
                # 具体的笔记
                a_note = Path(match.group(1))
                if cur_level == 1:
                    cur_top_category_info.notes.append(a_note)
                else:
                    cur_sub_category_list.append(a_note)
            i += 1

    def update(self, doing_categories_to_files: defaultdict[str, list[Path]], note_categories_to_files[str, list[Path]]):
        pass

    def to_markdown(self):
        pass


def generate_content(title: str, categories_to_files: defaultdict[str, list]):
    if categories_to_files:
        return ""
    # 标题行
    res = "## " + title + "\n\n"
    # 类别列表行：
    categories = categories_to_files.keys()
    sorted(categories)
    res += "类别列表：" + "、".join(categories) + "\n\n"

    # 具体的笔记行
    ## 新的内容全部放在最前面

    ## 子标题
    res += ""

    ## 内容

    return res + items + "\n\n"


def parse_old_file(content: str):
    """解析之前的 README 内容
    主要目的是保留 人工编辑的子目录结构 及其顺序

    Args:
        content (str): 之前的README文件内容
    """
    readme_structure = defaultdict()


def valid_file(file_name: str):
    """
    无用文件，主要是 . 开头的 隐藏文件夹 和 Doing 文件夹
    """
    return file_name != DOING_DIR_NAME and not file_name.startswith(".")


def get_all_file_names_and_categories(dir: Path):
    """获取Path目录下，所有的文件名列表和分类列表

    Args:
        dir (Path): 目录
    Returns:
        {}: 分类 -> 文件列表
    """
    category_to_files = defaultdict(list)
    if not dir.exists():
        return category_to_files

    files = [file for file in dir.iterdir() if valid_file(file.name)]
    for file in files:
        file_stem = file.stem
        category = file_stem.split("-")[0] if "-" in file_stem else ""
        category_to_files[category].append(file)

    return category_to_files


def generate_markdown_item(file: Path, note_dir: Path):
    return f"+ [{file.stem}]({file.relative_to(note_dir)})"


def concat_dir_files(dir: Path):
    """
    生成 Path 下所有文件名的列表

    Returns:
        str, str: 拼接好的文件列表，和分类信息
    """
    if not dir.exists():
        return "", ""
    items = [file.stem for file in dir.iterdir() if valid_file(file.name)]
    # items 排序，让文件列表稳定
    items.sort()
    categories = {item.split("-")[0] for item in items if "-" in item}
    return "\n".join(f"+ {item}" for item in items), "、".join(categories)


def update_readme_file(git_path: Path):
    """
    更新当前笔记仓库下的 README.md 文件

    每个笔记仓库，主要是以下2个文件夹，需要整理到 README 中：
        - &Doing: 近期正在处理的一些东西
        - 笔记仓库同名文件夹 note_dir: 已完成的笔记，同时作为坚果云同步的笔记文件夹
    """

    git_name = git_path.name

    if not git_path.exists():
        print("*    当前机器不存在目录: " + git_name)
        return

    readme_path = git_path / README_FILE_NAME
    note_dir = git_path / git_name

    # 1. 读取老 README 文件内容
    with open(readme_path, "r", encoding="utf-8") as file:
        last_readme_content = file.read()
    readme_content = ReadmeContent()
    readme_content.parse(last_readme_content)

    # 2.1 Doing 目录下所有的内容
    doing_categories_to_files = get_all_file_names_and_categories(
        note_dir / DOING_DIR_NAME
    )

    # 2.2 笔记目录下所有的一级目录名（不包含 Doing）
    note_categories_to_files = get_all_file_names_and_categories(note_dir)

    # 3. 更新
    readme_content.update(doing_categories_to_files, note_categories_to_files)

    # 4. 生成新的 readme 文件内容
    new_content = readme_content.to_markdown()

    # 5. 写回文件
    with open(readme_path, "w", encoding="utf-8", newline="\n") as file:
        file.write(new_content)
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
