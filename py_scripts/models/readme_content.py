from __future__ import annotations
from typing import ClassVar
from collections import defaultdict
import re
from py_scripts.models.note import Note
from pathlib import Path


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

    @classmethod
    def read_from_md_path(cls, readme_path: Path) -> ReadmeContent:
        """从 md 构建"""
        with open(readme_path, "r", encoding="utf-8") as file:
            content = file.read()

        description_end_idx = content.find(ReadmeContent.DESCRIPTION_SPLITTER) + len(
            ReadmeContent.DESCRIPTION_SPLITTER
        )
        note_start_idx = content.find(ReadmeContent.NOTE_SPLITTER)

        instance = ReadmeContent()
        instance.description = content[:description_end_idx].strip()
        instance.doing_part = content[description_end_idx:note_start_idx].strip()
        instance.note_part = content[note_start_idx:].strip()
        return instance

    def parse_note_part(self) -> list[Note]:
        """解析 note 部分"""
        notes = []
        if not self.note_part:
            return notes

        note_item_list = self.note_part.split("\n")

        cur_second_category = None
        for note_item in note_item_list:
            if match := re.search(r"^#### (.*)", note_item):
                # 二级目录
                cur_second_category = match.group(1)
            elif note_path := Note.is_note_markdown_item(note_item):
                # 具体的笔记
                notes.append(Note.parse_from_path_str(note_path, cur_second_category))
        return notes

    # 定义排序规则：None 排在最前，其他按字符串升序
    ITEM_SORT_KEY = lambda self, x: (0, "") if x is None else (1, str(x))

    def new_doing_part(self, doing_notes: list[Note]):
        """更新 doing_part

        Args:
            doing_notes (list[Note]): doing 笔记
        """

        self.doing_part = rf"""## Doing

类别列表：{"、".join( sorted(
            {note.first_category for note in doing_notes if note.first_category},
            key=self.ITEM_SORT_KEY,
        ))}

{"\n".join([note.to_markdown_item() for note in sorted(doing_notes)])}"""

    def new_note_part(self, notes: list[Note]):
        """更新 note_part

        Args:
            doing_notes (list[Note]): doing 笔记
            notes (list[Note]): 普通笔记
        """
        ## 整理成 一级目录 -> 二级目录 -> note
        first_to_second_to_notes = defaultdict(lambda: defaultdict(list))
        for note in notes:
            first_to_second_to_notes[note.first_category][note.second_category].append(
                note
            )

        self.note_part = rf"""## 列表

类别列表：{"、".join(sorted(sorted(
            {note.first_category for note in notes if note.first_category}, key=self.ITEM_SORT_KEY
        )))}
"""
        for first_category in sorted(
            first_to_second_to_notes.keys(), key=self.ITEM_SORT_KEY
        ):
            self.note_part += rf"""
### {first_category}

"""
            second_to_notes = first_to_second_to_notes[first_category]
            second_categories = sorted(
                {k for k in second_to_notes.keys() if k}, key=self.ITEM_SORT_KEY
            )
            if second_categories:
                self.note_part += "类别列表：" + "、".join(second_categories) + "\n\n"
            for second_category in sorted(
                second_to_notes.keys(), key=self.ITEM_SORT_KEY
            ):
                notes_in_second = second_to_notes[second_category]
                if second_category:
                    self.note_part += f"\n#### {second_category}\n\n"
                for note in sorted(notes_in_second):
                    self.note_part += f"- [{note.name}](<{note.path}>)\n"

    def to_markdown(self):
        return self.description + "\n\n" + self.doing_part + "\n\n" + self.note_part
