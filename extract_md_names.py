from pathlib import Path


def update_readme_file(git_path: Path):
    """更新 README.md 文件"""
    readme_path = git_path / 'README.md'
    doing_dir_name = '&Doing'

    def valid_file(file_name: str):
        """无用文件，主要是 . 开头的隐藏文件夹 和 Doing"""
        return file_name != doing_dir_name and not file_name.startswith('.')

    # 当前目录应该只有一个文件夹，作为用坚果云同步的笔记文件夹
    note_dir = next(file for file in git_path.iterdir()
                    if file.is_dir() and valid_file(file.name))

    # 读取 README 文件内容，保留分隔符前的部分
    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()
    splitter = '------------------------------------------------------'
    content = content[:content.find(splitter) + len(splitter)] + '\n\n'

    # 生成内容
    def concat_dir_files(dir: Path):
        """生成 Path 下所有文件名的列表

        Returns:
            str, str: 拼接好的文件列表，和分类信息
        """
        if not dir.exists():
            return '', ''
        # TODO 特殊逻辑兼容
        if dir.name == 'Journal':
            items = (file.stem for file in dir.rglob('*.md'))
        else:
            items = (file.stem for file in dir.iterdir()
                     if valid_file(file.name))
        categories = (item.split('-')[0] for item in items if '-' in items)
        return '\n'.join(f'+ {item}' for item in items), '、'.join(categories)

    # 1. Doing 目录下所有的内容
    doing_items, doing_categories = concat_dir_files(note_dir / doing_dir_name)
    # 2. 笔记目录下所有的一级目录名（不包含 Doing）
    note_items, note_categories = concat_dir_files(note_dir)

    def concat_content(title: str, categories: str, items: str):
        if items == '':
            return ''
        if categories != '':
            categories += '\n\n'
        return '# ' + title + '\n\n' + categories + items + '\n\n'

    content += concat_content('Doing', doing_categories, doing_items)
    content += concat_content('列表', note_categories, note_items)

    # 写回文件
    with open(readme_path, 'w', encoding='utf-8', newline='\n') as file:
        file.write(content)


if __name__ == '__main__':
    # 这三个 git 文件夹通常都在一起，我决定将这个 py 文件放在 Note 中，一次性更新所有的笔记仓库的README
    parent_dir = Path() / '..'

    update_readme_file(parent_dir / 'Journal')
    update_readme_file(parent_dir / 'Note')
    update_readme_file(parent_dir / 'Secret_note')
