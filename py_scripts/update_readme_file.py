from pathlib import Path
from collections import defaultdict
from typing import ClassVar
import re


class Note:
    # 笔记名称，不含分类
    name: str | None = None
    # 笔记名称，含分类
    stem: str | None = None
    # 路径
    path: Path | None = None
    # 一级分类
    first_category: str | None = None
    # 二级分类
    second_category: str | None = None

    @classmethod
    def parse_from_path_str(cls, path_str: str, second_category: str | None):
        path = Path(path_str)
        note = cls.parse_from_path(path, None)
        if note:
            note.second_category = second_category
        return note

    @classmethod
    def parse_from_path(cls, path: Path, base_path: Path | None):
        file_stem = path.stem
        match = re.search(r"(.*?)-(.*)", file_stem)
        if not match:
            # raise ValueError(f"{str(path)} 未分类")
            return None

        note = cls()
        note.name = match.group(2)
        note.stem = file_stem
        note.path = (
            path.resolve().relative_to(base_path.resolve()) if base_path else path
        )
        note.first_category = match.group(1)
        return note

    def __repr__(self):
        return f"Note(name={self.name}, path={self.path}, first_category={self.first_category}, second_category={self.second_category})"

    def __lt__(self, other):
        if not isinstance(other, Note):
            return NotImplemented
        # 按照文件名 stem 排序
        if self.stem is None or other.stem is None:
            return False
        return self.stem < other.stem


class ReadmeContent:
    """README 的文件结构"""

    DESCRIPTION_SPLITTER: ClassVar[str] = (
        "------------------------------------------------------"
    )
    NOTE_SPLITTER: ClassVar[str] = "## 列表"

    # 描述部分
    description: str
    # Doing
    doing_part: str
    # 列表
    note_part: str

    def read_from_md(self, content: str):
        description_end_idx = content.find(ReadmeContent.DESCRIPTION_SPLITTER) + len(
            ReadmeContent.DESCRIPTION_SPLITTER
        )
        note_start_idx = content.find(ReadmeContent.NOTE_SPLITTER)

        self.description = content[:description_end_idx].strip()
        self.doing_part = content[description_end_idx:note_start_idx].strip()
        self.note_part = content[note_start_idx:].strip()

    def parse_note_part(self) -> list[Note]:
        notes = []
        if not self.note_part:
            return notes

        note_item_list = self.note_part.split("\n")

        cur_second_category = None
        for note_item in note_item_list:
            if match := re.search(r"^#### (.*)", note_item):
                # 二级目录
                cur_second_category = match.group(1)
            elif match := re.search(r"\+ \[.*\]\(<(.*)>\)", note_item):
                # 具体的笔记
                notes.append(
                    Note.parse_from_path_str(match.group(1), cur_second_category)
                )
        return notes

    def update(
        self,
        doing_notes: list[Note],
        doing_categories: set[str],
        notes: list[Note],
        note_categories: set[str],
        old_notes: list[Note],
    ):
        # old_notes 只用于获取二级目录的信息
        stem_to_second_category = {
            note.stem: note.second_category for note in old_notes
        }
        for note in notes:
            if note.stem in stem_to_second_category:
                note.second_category = stem_to_second_category[note.stem]
        # doing_part 的拼接
        self.doing_part = "## Doing\n\n"
        self.doing_part += "类别列表：" + "、".join(sorted(doing_categories)) + "\n\n"
        for note in sorted(doing_notes):
            self.doing_part += f"+ [{note.name}]({note.path.as_posix()})\n"
        # note_part 的拼接
        self.note_part = "## 列表\n\n"
        self.note_part += "类别列表：" + "、".join(sorted(note_categories)) + "\n"
        ## 整理成 一级目录 -> 二级目录 -> note
        first_to_second_to_notes = defaultdict(lambda: defaultdict(list))
        for note in notes:
            first_to_second_to_notes[note.first_category][note.second_category].append(
                note
            )
        for first_category in sorted(first_to_second_to_notes.keys()):
            self.note_part += f"\n### {first_category}\n\n"
            second_to_notes = first_to_second_to_notes[first_category]
            actual_second_categories = sorted([k for k in second_to_notes.keys() if k])
            if actual_second_categories:
                self.note_part += (
                    "类别列表：" + "、".join(actual_second_categories) + "\n\n"
                )
            for second_category, notes_in_second in second_to_notes.items():
                if second_category:
                    self.note_part += f"\n#### {second_category}\n\n"
                for note in sorted(notes_in_second):
                    self.note_part += f"+ [{note.name}](<{note.path}>)\n"

    def to_markdown(self):
        return self.description + "\n\n" + self.doing_part + "\n\n" + self.note_part


README_FILE_NAME = "README.md"
DOING_DIR_NAME = "&Doing"


def get_all_notes(note_dir: Path, base_path: Path) -> tuple[list[Note], set[str]]:
    """获取Path目录下，所有的笔记列表和分类列表

    笔记只会直接位于 note_dir 下

    Args:
        note_dir (Path): 笔记目录
        base_path (Path): 基础路径，用于计算相对路径
    Returns:
        笔记列表，分类
    """
    notes = []
    categories = set()

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
            categories.add(note.first_category)
    return notes, categories


def update_readme_file(git_path: Path):
    """
    更新当前笔记仓库下的 README.md 文件

    每个笔记仓库，主要是以下2个文件夹，需要整理到 README 中：
        - &Doing: 近期正在处理的一些东西
        - 笔记仓库同名文件夹 note_dir: 已完成的笔记，同时作为坚果云同步的笔记文件夹

    每个笔记的名称格式为：分类-名称.md
    此处的分类为一级分类，在 README.md 里，可以人工添加二级分类，在更新时，已有的二级分类需要保留不变
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
    readme_content.read_from_md(last_readme_content)
    old_notes = readme_content.parse_note_part()

    # 2.1 Doing 目录下所有的内容
    doing_notes, doing_categories = get_all_notes(note_dir / DOING_DIR_NAME, git_path)

    # 2.2 笔记目录下所有的一级目录名（不包含 Doing）
    notes, note_categories = get_all_notes(note_dir, git_path)

    # 3. 更新
    readme_content.update(
        doing_notes, doing_categories, notes, note_categories, old_notes
    )

    # 4. 生成新的 readme 文件内容
    new_content = readme_content.to_markdown()

    # 5. 写回文件
    with open(readme_path, "w", encoding="utf-8", newline="\n") as file:
        file.write(new_content)
    print(git_name + " 的 README 已更新完毕")


if __name__ == "__main__":
    update_readme_file(Path.cwd().parent)
