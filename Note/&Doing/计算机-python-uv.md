# uv

[让uv管理Python的一切](https://www.bilibili.com/video/BV1Stwfe1E7s/)
[【小萌发现】Python项目管理｜你还在用conda？3分钟速成UV！](https://www.bilibili.com/video/BV12a49z5EMW)

## 安装

https://docs.astral.sh/uv/getting-started/installation

## 使用

```shell
# 新建项目
uv init -p 3.13.5 project_name

cd project_name

# 安装依赖
uv add pandas

# 删除依赖
uv remove pandas

# 运行
uv run main.py
```

## 同步现有项目

```shell
# 安装所有依赖的包
uv sync

# 仅安装生产环境（不安装开发环境）
uv sync --no-dev
```

## 安装包常用方式

```shell
# 不指定包版本
uv add openai pandas

# 指定包的版本
uv add 'requests==2.31.0'

# 通过git安装
uv add git+https://github.com/

# 安装 requirements.txt 的所有包
uv add -r requirements.txt

# 仅加入开发环境分组
uv add --dev openai pandas
```
