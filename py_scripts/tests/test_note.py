from py_scripts.models.note import Note


def test_note_parser():
    cases = [
        ("- [笔记](./dir.md)", "./dir.md"),
        ("- [n](<./dir.md>)", "./dir.md"),
        ("+ [n](./dir.md)", "./dir.md"),
        ("+ [n](<./dir.md>)", "./dir.md"),
        ("  -   [indent](./dir.md)", "./dir.md"),  # 带缩进
    ]
    for line, expected in cases:
        assert Note.is_note_markdown_item(line) == expected
