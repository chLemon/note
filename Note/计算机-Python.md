# Python

## Mac 安装 Python

不建议使用 `brew`，最好直接去官网安装

mac 现在自带的有2个版本，一个是早期的 2.7.18，还会保留。新版本会有一个 3.9。

## pip 相关

现在 `pip` 命令可以指定相关版本，例如 `pip3.13`。

注意 pip 安装的包，不同版本不互通。即 `pip3.9` 安装的包并不会在 `pip3.13` 中，用 `python 3.13`执行时，会报错。

```bash
# 可以输出当前所有的包
pip3 freeze

# 输出到某个文件里
pip3 freeze > requirements.txt

# 安装某个文件里的包，注意要删掉里面很长的那种行，不然会报错
pip3.13 install -r requirements.txt

# 更新某个包
pip3.13 install --upgrade 包名

# 更新全部，现在没有直接的命令，可以借助 requirements.txt
pip3.13 install --upgrade -r requirements.txt
```
