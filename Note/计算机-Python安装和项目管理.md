# Python

## 1. Mac 安装 Python

不建议使用 `brew`，最好直接去官网安装。可以看下方 `uv` 的部分，通过 `uv` 来安装管理。

mac 现在自带的有2个版本，一个是早期的 2.7.18，还会保留。新版本会有一个 3.9。

## 2. 项目管理

### 2.1. Python 官方体系项目管理的发展历程

[从pip到uv：一口气梳理现代Python项目管理全流程！](https://www.bilibili.com/video/BV13WGHz8EEz)

早期的官方体系做的不太好，所以有各种各样的写法，后来出了一些规范，渐渐完善了起来。

#### 2.1.1. 虚拟环境 venv

- 版本冲突 问题：如果直接通过 pip 安装依赖，那么整台机器的该依赖版本都会改变，而不同的项目可能需要不同的版本，会产生依赖冲突

- 依赖地狱 问题：一个依赖可能依赖了若干其他依赖，在依赖变多的情况下，版本冲突就更麻烦了

所以有了虚拟环境：

```shell
# 创建虚拟环境
python3 -m venv .venv
# 激活虚拟环境
source .venv/bin/activate
```

这里的 `.venv` 是虚拟环境的名字，运行这个命令会在当前项目下创建 `.venv` 的文件夹，放置依赖的源码。
这个名字是可自定义的，但是由于约定俗成的原因，通常保持这个名字。

在激活虚拟环境后，再使用 pip 安装，就不是安装在全局了。

这里的原理是，venv 修改了 `sys.path` 的值，这是一个列表，里面包含了 python 在 import 时搜索的目录，在其中增加了当前项目的 `.venv` 目录。

#### 2.1.2. 环境复现

当你获得了一个其他人的项目，想复现项目环境的时候，早期会这么做：

```shell
# freeze 会列出所有的依赖名和版本，重定向到一个文件里
pip freeze > requirements.txt
# 批量安装
pip install -r requirements.txt
```

这样做的缺点是：

1. `pip freeze` 也会展示出所有的间接依赖
2. `pip uninstall` 时，并不会卸载间接依赖

#### 2.1.3. 官方指定统一的配置文件 `pyproject.toml`

```toml
[project]
name = "proj"
version = "0.1.0"
dependencies = [
    "Flask==3.1.1"
]
```

早期各个项目会有各自的配置文件，现在基本上都统一在了 `pyproject.toml` 里，可以在 `dependencies` 里直接写直接依赖进行管理。

在进行

```shell
pip install .
```

时，会把当前项目安装到当前目录里，在这个过程中，会

1. 构建当前项目，打包成一个标准的Python软件包
2. 安装当前软件包，同时也会安装所有依赖

不过这样做时，在当前虚拟环境的包目录 `.venv/lib/python3.13/site-packages` 里，也会把我们的项目代码放进去，我们的项目里就会有2份代码，如果有代码进行修改时，不会立刻生效。可以用

```shell
# -e 编辑模式
pip install -e .
```

进行安装，这样在虚拟环境的包目录里，我们的项目代码会变成一个链接，指向我们的源码，这时的修改就会立刻生效。

这时，我们通过一个配置文件管理了所有的直接依赖。不过当需要增加新依赖时，操作会比较复杂，需要先去网站找依赖的版本，手动加到 toml 里。

现在社区有第三方工具，封装了 venv 和 pip，不用自己去手动繁琐地操作这些，如 poetry、uv、PDM

### 2.2. conda

[15分钟彻底搞懂！Anaconda Miniconda conda-forge miniforge Mamba](https://www.bilibili.com/video/BV1Fm4ZzDEeY)

python 本身运行速度很慢，在一些科学领域，有用C语言等写的 numpy、pandas 等工具，可以用 python 进行调用，使得调用简单，性能又好，非常好用。

但是早期的 python 官方对于这些其他语言包的依赖管理做得很不好。所以有人把这些解决好冲突的依赖打了个包，叫 Anaconda Distribution，广受好评。后来该公司因为这个太火了，就改名叫 Anaconda 了。

但是里面东西太多了，非常大，所以他们又做了个 conda 命令程序，类似于 pip，可以安装、卸载依赖，变成了一个独立的开发平台，支持多语言、依赖管理、虚拟环境等。这个只有 conda 程序和必要依赖的叫 miniconda。

远程依赖是他们自己维护的，叫 ANACONDA.ORG。他们自己维护了一套，又由于想给社区开放这个功能，这样一套的依赖仓库就叫一个 channel，默认的是 defaults，但是这个后来商业收费了。现在开源免费社区最大的是 conda-forge。

miniconda 的 conda 命令默认从 defaults 拉取依赖，所以有人又写了个 miniforge 软件，默认从 conda-forge 去拉取依赖（conda 本身是开源的），又觉得 conda 性能有点差，用 C++ 重写了一下，叫 mamba。

现在一般说的下载个 conda，一般指的是下载 miniforge，使用 mamba 进行操作。

不过由于现在 conda 里很多库也不齐全了，pip 官方做的也不错，而且 conda / mamba 和 pip 并不能很好的兼容，评论区很多人已经不推荐使用了。

### 2.3. uv 的出现

传统 python 要用这些命令来管理依赖：

```shell
# 创建虚拟环境
python -m venv .venv
# 激活
source .venv/bin/activate
# 编辑配置文件
edit pyproject.toml
# 安装
pip install -e .
# 运行
python main.py
```

现在只需要1-2行命令可能就能完成了：

```shell
uv add flask
uv run main.py
```

如果是 clone 了别人的项目，只需要

```shell
uv sync
```

## 3. uv

[让uv管理Python的一切](https://www.bilibili.com/video/BV1Stwfe1E7s/)

rust 写的一个高性能 python 项目管理工具，支持 Python 安装、虚拟环境、依赖管理、工具安装、打包发布。

### 3.1. 安装 Python

```shell
# 查看 uv 可以安装的 python 版本
uv python list
# 安装特定版本（非必要，run 时没有会自动安装）
uv python install cpython-3.12
# 运行文件
uv run -p 3.12 main.py
# 打开交互式界面
uv run -p 3.12 python
```

### 3.2. 工程管理

```shell
# 创建 uv 工程
uv init -p 3.13
```

会创建：

- `hello.py`：示例代码
- `.python-version`：记录了python的版本信息，换版本可以直接修改
- `pyproject.toml`：配置文件

### 3.3. 安装依赖

```shell
# 安装依赖，同时 uv 会创建虚拟环境
uv add requests
# --dev 安装依赖，但是打包的时候不打包
uv add pytest --dev
# 删除依赖
uv remove pytest --dev
```

安装的依赖会自动加入到 `pyproject.toml` 的 `dependencies` 中。

可以点 vscode 右下角的 python 版本号切换 vscode 的 python 解释器，使用虚拟环境。

### 3.4. 运行文件

```shell
uv run main.py
```

### 3.5. 安装工具

```shell
# 安装工具，脱离当前工程，整个系统可用，每个工具都有自己的虚拟环境，无需担心库和库之间冲突
uv tool install ruff
# 查看已经安装的工具
uv tool list
```

### 3.6. 其他命令

```shell
# 查看工程的所有依赖关系
uv tree
```

### 3.7. 打包

在 toml 里新增一部分：

```toml
[project.scripts]
script-name = "script-file-name:method-name"
```

```shell
# 构建为 whl 文件
uv build

# 本地安装
uv tool install dist/test.whl
```

安装后，可以直接使用 脚本名称 使用命令

## 4. pip 相关

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
