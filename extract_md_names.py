import os

# 定义
readme_path = './README.md'
readme_retain_anchor = '# 列表'
note_path = './Note/'
doing_name = '&Doing'
doing_path = note_path + doing_name



# 读取 README 文件内容
with open(readme_path, 'r', encoding='utf-8') as file:
    content = file.read()

def optimize_file_name(file_name:str):
    return file_name if not file_name.endswith('.md') else file_name[:-3]
def filter_file_name(file_name:str):
    return file_name == doing_name or file_name.startswith('.')
def concat_dir_files(dir_path):
    return '\n'.join('+ ' + optimize_file_name(file_name) for file_name in os.listdir(dir_path) if not filter_file_name(file_name)) + '\n\n'

# 保留 列表 前面的部分
keep = content[:content.find(readme_retain_anchor) + len(readme_retain_anchor)] + '\n\n'
# 获取Note下所有的一级目录名，拼接在 keep 后面
keep += concat_dir_files(note_path)

# 获取 Doing 下所有的一级目录名，拼接
keep += '# Doing\n\n'
keep += concat_dir_files(doing_path)

# 写回文件
with open(readme_path, 'w', encoding='utf-8') as file:
    file.write(keep)