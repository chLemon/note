from pathlib import Path
import re


class Note:
    # 笔记名称，不含分类
    name: str
    # 笔记名称，含分类
    stem: str
    # 路径
    path: Path
    # 一级分类
    first_category: str
    # 二级分类
    second_category: str | None = None

    def __init__(self, name, stem, path, first_category, second_category) -> None:
        self.name = name
        self.stem = stem
        self.path = path
        self.first_category = first_category
        self.second_category = second_category

    _NOTE_LINK_PATTERN = re.compile(r"[-+]\s+\[.*?\]\(<?([^>)]+)>?\)")

    @classmethod
    def is_note_markdown_item(cls, markdown_line: str) -> str | None:
        """判断是笔记的列表项

        Args:
            markdown_line (str): markdown 的一行

        Returns:
            str: 解析出的笔记path
        """
        # 笔记列表项的格式可能有多种：
        # - [笔记名](目录)
        # - [笔记名](<目录>)
        # + [笔记名](目录)
        # + [笔记名](<目录>)
        if match := cls._NOTE_LINK_PATTERN.search(markdown_line):
            return match.group(1).strip()
        return None

    @classmethod
    def parse_from_path_str(cls, path_str: str, second_category: str | None):
        """从字符串 path 构造 Note，主要用于读取已有 readme.md 时

        Args:
            path_str (str): path 字符串
            second_category (str | None): 二级目录

        Returns:
            _type_: 解析好的 Note
        """
        """"""
        path = Path(path_str)
        note = cls.parse_from_path(path, None)
        if note:
            note.second_category = second_category
        return note

    @classmethod
    def parse_from_path(cls, path: Path, base_path: Path | None):
        """从 path 构造 Note

        Args:
            path (Path): 笔记文件的 path
            base_path (Path | None): 基础路径，一般是 readme.md 所在的目录，用来规范引用里的路径

        Returns:
            _type_: 解析好的 Note
        """
        file_stem = path.stem
        # 文件名都是 类别-笔记名
        match = re.search(r"(.*?)-(.*)", file_stem)
        if not match:
            # raise ValueError(f"{str(path)} 未分类")
            return None

        note = cls(
            name=match.group(2),
            stem=file_stem,
            path=(
                path.resolve().relative_to(base_path.resolve()) if base_path else path
            ),
            first_category=match.group(1),
            second_category=None,
        )
        return note

    @classmethod
    def update_second_category(cls, all_notes: list[Note], old_notes: list[Note]):
        """更新二级目录

        Args:
            all_notes (list[Note]): 全部笔记
            old_notes (list[Note]): 老的笔记，，只用于获取二级目录的信息
        """
        stem_to_second_category = {
            note.stem: note.second_category for note in old_notes
        }
        for note in all_notes:
            if note.stem in stem_to_second_category:
                note.second_category = stem_to_second_category[note.stem]

    def to_markdown_item(self):
        return f"- [{self.name}](<{self.path.as_posix()}>)"

    def __repr__(self):
        return f"Note(name={self.name}, path={self.path}, first_category={self.first_category}, second_category={self.second_category})"

    def __lt__(self, other):
        if not isinstance(other, Note):
            return NotImplemented
        # 按照文件名 stem 排序
        if self.stem is None or other.stem is None:
            return False
        return self.stem < other.stem
