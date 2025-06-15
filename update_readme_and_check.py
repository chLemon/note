import Note.py_script.collect_all_md_names as update_readme
import py_script.check_every_note_is_classified as classified_check
import py_script.check_every_pic_is_valid as pic_valid_check

from pathlib import Path

if __name__ == '__main__':
    note_git_path = Path.cwd()

    print("==========      开始更新 README 文件       ========== \n")
    update_readme.main(note_git_path)
    print("\n========== README 文件更新完成，开始分类校验 ==========\n")
    classified_check.main(note_git_path)
    print("\n==========  分类校验完成，开始图片有效性校验  ==========\n")
    pic_valid_check.main(note_git_path)
    print("\n==========      图片有效性校验完成          ==========\n")
