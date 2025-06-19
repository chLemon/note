from pathlib import Path


def check_note_read_me_is_classified(git_path: Path):
    """
    检查所有的文件都进行了分类

    读取 README 里 列表 中的文件名，如果文件名没有 - ，则说明没有进行分类
    """
    # 直接通过 README 判断即可
    read_me_path = git_path / "README.md"
    with open(read_me_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file]
    splitter = "# 列表"
    before_splitter = True
    not_classified = []
    for l in lines:
        if splitter in l:
            before_splitter = False
            continue
        if before_splitter:
            continue
        if not l.startswith("+"):
            continue
        # 有效的笔记
        if "-" not in l:
            not_classified.append(l)
    return not_classified


def check_every_note_is_classified(git_path: Path):
    not_classified = check_note_read_me_is_classified(git_path)
    if not_classified:
        print("以下文件没有被分类\n" + "\n".join(not_classified))
    else:
        print("全部都已分类")


if __name__ == "__main__":
    check_every_note_is_classified(Path().cwd().parent)
