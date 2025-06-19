from py_scripts import collect_note_names, check_every_note_is_classified, check_every_pic_is_used
from pathlib import Path

if __name__ == '__main__':
    note_git_path = Path.cwd()

    print("==========      开始更新 README 文件       ========== \n")
    collect_note_names(note_git_path)
    print("\n========== README 文件更新完成，开始分类校验 ==========\n")
    check_every_note_is_classified(note_git_path)
    print("\n==========  分类校验完成，开始图片有效性校验  ==========\n")
    check_every_pic_is_used(note_git_path)
    print("\n==========      图片有效性校验完成          ==========\n")
