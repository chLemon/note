from pathlib import Path

readme_path = './README.md'
# 读取文件内容
with open(readme_path, 'r', encoding='utf-8') as file:
    content = file.read()

# 保留 列表 前面的部分
anchor = '# 列表'
keep = content[:content.find(anchor) + len(anchor)] + '\n\n'

# 获取Note下所有的.md文件名，拼接在 keep 后面
md_files = list(Path('./Note').rglob("*.md"))
keep += '\n'.join('+ '+ file.name for file in md_files)

# 写回文件
with open(readme_path, 'w', encoding='utf-8') as file:
    file.write(keep)