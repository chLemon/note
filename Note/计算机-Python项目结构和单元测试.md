# Python项目结构和单元测试

## 1. 项目结构

[build + hatchling 15分钟搞懂Python项目结构和打包](https://www.bilibili.com/video/BV12NgLzhEKx)

我们在安装依赖的时候，其实都是在 pypi 这个网站上下载东西，下载的是一个 whl 文件，是一个 zip 压缩包。安装的过程就是下载+解压缩。

以 flask 为例，会包含2个文件夹：

- `flask-3.1.1.disk-info`：记录 flask 用到的依赖
- `flask`：存放源码的代码目录，可能有多个

### 1.1. flat layout

结构比较简单的项目

```text
project_name
    |-- main.py
    |-- __init__.py
pyproject.toml
```

这样打包出来的 whl 文件，python 文件就会在一个目录下，不至于在根目录下。

### 1.2. src layout【推荐】

最最流行的代码结构

```text
src
  |-- project_name
            |-- __init__.py
            |-- main.py
tests
docs
scripts
```

只有 `src` 目录下的文件才会被打包，打包后的结构就是 `project_name/main.py`，并不会有 `src`。

## 2. Python单元测试

[如何使用pytest进行单元测试](https://www.bilibili.com/video/BV1KZWKz3Ek5/)

在 src 布局下，单元测试位于 tests 文件夹下，结构一一对应，pytest 会自动搜索名字以 `test_` 开头的文件和函数作为测试文件和测试函数。

在 VsCode 里，可以在命令里找 Python: Configure Tests 选择，可以在左边找到 tests

@pytest.fixture

@pytest.mark.parametrize
