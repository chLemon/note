def check_every_note_is_classified():
    """检查所有的文件都进行了分类"""
    # 直接通过 README 判断即可
    with open('./README.md', 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file]
    splitter = '------------------------------------------------------'
    before_splitter = True
    not_classified = []
    for l in lines:
        if splitter in l:
            before_splitter = False
            continue
        if before_splitter:
            continue
        if not l.startswith('+'):
            continue
        # 有效的笔记
        if '-' not in l:
            not_classified.append(l)
    return not_classified


if __name__ == '__main__':
    not_classified = check_every_note_is_classified()
    if not_classified:
        print('\n'.join(not_classified))
    else:
        print("全部都已分类")