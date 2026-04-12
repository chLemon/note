from py_scripts.models.note import Note
import pytest


@pytest.mark.parametrize(
    "line, expected",
    [
        ("- [笔记](./dir.md)", "./dir.md"),
        ("- [n](<./dir.md>)", "./dir.md"),
        ("+ [n](./dir.md)", "./dir.md"),
        ("+ [n](<./dir.md>)", "./dir.md"),
        ("+ [n](<./dir().md>)", "./dir().md"),
        ("+ [name-sub](<./name-sub.md>)", "./name-sub.md"),
        ("   -   [indent](./dir.md)", "./dir.md"),  # 带缩进
        ("not a note link", None),  # 补充：反面测试
    ],
)
def test_is_note_markdown_item(line, expected):
    """
    使用 parametrize 后，pytest 会为每组数据运行一次该函数
    """
    assert Note.is_note_markdown_item(line) == expected
