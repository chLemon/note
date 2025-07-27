# Markdown 支持

- [Markdown 支持](#markdown-支持)
- [1. VS Code Markdown 支持](#1-vs-code-markdown-支持)
    - [1.1. 官方原生支持](#11-官方原生支持)
        - [1.1.1. 目录](#111-目录)
        - [1.1.2. 快速跳转](#112-快速跳转)
        - [1.1.3. 智能选择](#113-智能选择)
        - [1.1.4. 引用链接](#114-引用链接)
            - [1.1.4.1. 路径补全](#1141-路径补全)
            - [1.1.4.2. 文件复制进工作区](#1142-文件复制进工作区)
                - [1.1.4.2.1. 复制路径设置](#11421-复制路径设置)
            - [1.1.4.3. 链接校验](#1143-链接校验)
            - [1.1.4.4. 找到标题/链接的所有引用](#1144-找到标题链接的所有引用)
            - [1.1.4.5. 修改标题和链接](#1145-修改标题和链接)
            - [1.1.4.6. 文件移动或者重命名的时候，自动更新链接](#1146-文件移动或者重命名的时候自动更新链接)
        - [1.1.5. 预览](#115-预览)
            - [1.1.5.1. 动态预览 和 预览锁定](#1151-动态预览-和-预览锁定)
            - [1.1.5.2. Markdown: Toggle Preview Locking](#1152-markdown-toggle-preview-locking)
            - [1.1.5.3. 预览和编辑的交互](#1153-预览和编辑的交互)
            - [1.1.5.4. 数学公式预览，默认开启](#1154-数学公式预览默认开启)
            - [1.1.5.5. 预览安全](#1155-预览安全)
        - [1.1.6. 保留尾部空格](#116-保留尾部空格)
        - [1.1.7. 拓展推荐](#117-拓展推荐)
        - [1.1.8. Doc Writer Profile template](#118-doc-writer-profile-template)
    - [1.2. 插件汇总](#12-插件汇总)

# 1. VS Code Markdown 支持

> [官方文档](https://code.visualstudio.com/docs/languages/markdown)

VS Code 现在已经原生支持 Markdown Preview，并且提供了一些便利的设置和快捷键。安装一些插件效果更好。

## 1.1. 官方原生支持

### 1.1.1. 目录

- 左侧 `文件--大纲` 可以当做目录

### 1.1.2. 快速跳转

- `Command + Shift + O` 快速跳到当前文件的各级标题

- `Command + T` 搜索当前工作区所有 Markdown 文件的各级标题

### 1.1.3. 智能选择

可以用这 2 个快捷键进行智能选择

Expand: `⌃⇧⌘→` `control + shift + command + RightArrow`
Shrink: `⌃⇧⌘←` `control + shift + command + LeftArrow`

### 1.1.4. 引用链接

#### 1.1.4.1. 路径补全

- 路径补全：会自动对图片或文件链接的路径进行补全提示，`/`开头的会相对于当前工作区的根目录，`./`或者没有前缀的会相对于当前文件。
- 可以通过`^Space`来手动触发提示。
- 路径补全也可以链接到当前文件的标题，或者其他 Markdown 文件的标题。默认情况下，`#` 开头的路径，会认为是当前文件的标题。
- `##` 会查询当前工作区内其他文件的标题。

#### 1.1.4.2. 文件复制进工作区

- 可以在按住 shift 的时候，直接将资源管理器里的图片或文件拖进 markdown 文件，会快捷插入链接
- 也可以直接复制粘贴进来。
- 拖进来 或者 粘贴进来的时候，如果这个图片不在工作区内，会复制一份到当前工作区。

##### 1.1.4.2.1. 复制路径设置

`markdown.copyFiles.destination` 设置控制什么时候创建新的文件。这个设置是匹配 图片源目录 到 当前 markdown 文档的文件通配符。这个路径里还可以用一些变量，详见该设置处的说明

例如，你希望将工作区的 `/docs` 下的每个 Markdown 文件，都将新的媒体文件放到当前文件特定的 `images` 目录下，你可以写

```json
"markdown.copyFiles.destination": {
  "/docs/**/*": "images/${documentBaseName}/"
}
```

现在，当一个新文件被粘贴进 `/docs/api/readme.md`，图片文件就会创建在 `/docs/api/images/readme/image.png`

你甚至可以使用简单的正则表达式，以类似于片段的方式转换变量。

```json
"markdown.copyFiles.destination": {
  "/docs/**/*": "images/${documentBaseName/(.).*/$1/}/"
}
```

现在，当一个新文件被粘贴进 `/docs/api/readme.md`，图片文件就会创建在 `/docs/api/images/r/image.png`

#### 1.1.4.3. 链接校验

会校验链接是否有效

默认关闭，为了开启，设置 `"markdown.validate.enabled": true`

还有一些设置可以用来自定义链接校验：

- `markdown.validate.fileLinks.enabled` - 开启/关闭 本地文件链接 的校验 `[link](/path/to/file.md)`
- `markdown.validate.fragmentLinks.enabled` - 开启/关闭 当前文件标题链接 的校验 `[link](#_some-header)`
- `markdown.validate.fileLinks.markdownFragmentLinks` - 开启/关闭 其他文件标题链接 的校验 `[link](other-file.md#some-header)`
- `markdown.validate.referenceLinks.enabled` - 开启/关闭 链接 的校验 `[link][ref]`
- `markdown.validate.ignoredLinks -` 跳过校验的 链接 globs 的列表，当链接到一些本地没有，但是远程有的文件时，非常有用

#### 1.1.4.4. 找到标题/链接的所有引用

- 找到所有引用 - `⇧⌥F12` `shift + option + F12`

该功能支持：

- 标题：`# My Header` 展示所有引用到 `#my-header` 的链接
- 外部链接：`[text](http://example.com)`。展示所有链接到 `http://example.com` 的链接
- 内部链接：`[text](./path/to/file.md)`。展示所有链接到 `./path/to/file.md` 的链接
- 链接中的片段：`[text](./path/to/file.md#my-header)`。展示所有链接到 `./path/to/file.md` 里 `#my-header` 的链接

#### 1.1.4.5. 修改标题和链接

- `F2` 修改的时候可以修改掉所有引用，可用范围同上的 4 个

#### 1.1.4.6. 文件移动或者重命名的时候，自动更新链接

设置 `markdown.updateLinksOnFileMove.enabled`：

可以设置为：

- never (the default) — 不要试着自动更新连接
- prompt — 在更新连接前让用户确认
- always — 不需要确认，自动更新连接

自动连接更新会监测 Markdown 文件、图片、或目录 的改名。可以在 `markdown.updateLinksOnFileMove.include` 中为其他文件开启这个。

### 1.1.5. 预览

- `shift + command  + V` 可以直接在编辑器预览
- `command + K + V` 则可以在侧边预览

#### 1.1.5.1. 动态预览 和 预览锁定

默认开启

#### 1.1.5.2. Markdown: Toggle Preview Locking

编辑和预览同步滚动

默认开启

可以通过这两个设置禁用同步滚动：`markdown.preview.scrollPreviewWithEditor` 和 `markdown.preview.scrollEditorWithPreview`

#### 1.1.5.3. 预览和编辑的交互

编辑器里选择到的部分，会在预览里有一个灰色的高亮

双击预览，也会自动打开编辑器，并且滚动到点击处最近的行

#### 1.1.5.4. 数学公式预览，默认开启

`"markdown.math.enabled"`

#### 1.1.5.5. 预览安全

为了安全，内容展示在 Markdown Preview 里，会禁用脚本执行，并且只允许 https 的资源被加载

可以通过命令（`F1`）：`Markdown: Change preview security settings` 修改

- `Strict`: 默认设置，仅加载受信的内容，并且禁用脚本执行，禁止 http 的图片
    推荐保持在这个设置。除非你有一个充分的理由修改它，并且你信任你工作区里所有的 Markdown 文件
- `Allow insecure content`: 禁用脚本，但是允许内容里加载 http
- `Disable`: 在预览窗口里，禁用附加的安全措施。允许脚本执行，且允许 http 的内容加载

### 1.1.6. 保留尾部空格

要创建硬换行符，Markdown 要求在行尾有两个或更多空格。根据用户或工作区设置的不同，VS Code 可能会被配置为删除尾部空白。为了只在 Markdown 文件中保留拖尾空白，可以在 settings.json 中添加这些行：

```json
{
    "[markdown]": {
        "files.trimTrailingWhitespace": false
    }
}
```

### 1.1.7. 拓展推荐

| 插件                                   | 功能                                                   |
| -------------------------------------- | ------------------------------------------------------ |
| bierner.markdown-preview-github-styles | 改变 VS Code 内建 markdown 预览，匹配 Github 的风格    |
| bierner.markdown-emoji                 | 添加 emoji 语法                                        |
| goessner.mdmath                        | 数学公式的支持                                         |
| hbrok.markdown-preview-bitbucket       | 支持 bitbucket 风格，支持 `[TOC]` 目录                 |
| DavidAnson.vscode-markdownlint         | 检查 Markdown 语法，让 md 内容更通用（在不同解析器中） |
| ms-vscode.Theme-MarkdownKit            | 主题                                                   |
| pdconsec.vscode-print                  | 打印渲染                                               |
| mdickin.markdown-shortcuts             | markdown 快捷键                                        |

### 1.1.8. Doc Writer Profile template

> <https://code.visualstudio.com/docs/configure/profiles#_profile-templates>

官方提供了 文档协作 的 Profile 模板，包含下面的插件：

- streetsidesoftware.code-spell-checker: 源码的拼写检查
- bierner.markdown-checkbox: 为 VS Code 内建的 Markdown 预览提供 checkbox 支持
- bierner.markdown-emoji: 为 Markdown 预览和 notebook 的 Markdown 单元格添加 emoji 语法的支持
- bierner.markdown-footnotes: 为 Markdown 预览添加 `^footnote` 的语法支持
- bierner.markdown-preview-github-styles: 在 Markdown 预览使用 Github 风格
- bierner.markdown-mermaid: Mermaid 图表
- bierner.markdown-yaml-preamble: 将 YAML 前端内容渲染为表格
- DavidAnson.vscode-markdownlint: VS Code 的 Markdown 提示和格式检查
- itemName=ms-vscode.wordcount: 在状态栏查看 Markdown 文档的单词字数
- johnpapa.read-time: 计算阅读你的 Markdown 需要多久

这个 profile 还提供了如下的设置

```json
    "workbench.colorTheme": "Default Light Modern",
    "editor.minimap.enabled": false,
    "breadcrumbs.enabled": false,
    "editor.glyphMargin": false,
    "explorer.decorations.badges": false,
    "explorer.decorations.colors": false,
    "editor.fontLigatures": true,
    "files.autoSave": "afterDelay",
    "git.enableSmartCommit": true,
    "window.commandCenter": true,
    "editor.renderWhitespace": "none",
    "workbench.editor.untitled.hint": "hidden",
    "markdown.validate.enabled": true,
    "markdown.updateLinksOnFileMove.enabled": "prompt",
    "workbench.startupEditor": "none"
```

## 1.2. 插件汇总

| 插件                                   | 功能                                                                | 在插件包中 |
| -------------------------------------- | ------------------------------------------------------------------- | ---------- |
| bierner.markdown-checkbox              | 为 VS Code 内建的 Markdown 预览提供 checkbox 支持                   | ✅         |
| bierner.markdown-emoji                 | 为 Markdown 预览和 notebook 的 Markdown 单元格添加 emoji 语法的支持 | ✅         |
| bierner.markdown-footnotes             | 为 Markdown 预览添加 `^footnote` 的语法支持                         | ✅         |
| bierner.markdown-preview-github-styles | 改变 VS Code 内建 markdown 预览，匹配 Github 的风格                 | ✅         |
| bierner.markdown-mermaid               | Mermaid 图表                                                        | ✅         |
| bierner.markdown-yaml-preamble         | 将 YAML 前端内容渲染为表格                                          | ✅         |
| DavidAnson.vscode-markdownlint         | 检查 Markdown 语法，让 md 内容更通用（在不同解析器中）              |            |
| goessner.mdmath                        | 数学公式的支持                                                      |            |
| hbrok.markdown-preview-bitbucket       | 支持 bitbucket 风格，支持 `[TOC]` 目录                              |            |
| itemName=ms-vscode.wordcount           | 在状态栏查看 Markdown 文档的单词字数                                |            |
| johnpapa.read-time                     | 计算阅读你的 Markdown 需要多久                                      |            |
| ms-vscode.Theme-MarkdownKit            | 主题                                                                |            |
| mdickin.markdown-shortcuts             | markdown 快捷键                                                     |            |
| pdconsec.vscode-print                  | 打印渲染                                                            |            |
| streetsidesoftware.code-spell-checker  | 源码的拼写检查                                                      |            |
| Yu Zhang.Markdown All in One           | 快捷键、表格、预览等                                                |            |
| Markdown Preview Enhanced              |                                                                     |            |
| Mermaid Editor                         | mermaid 预览、导出 svg 文件                                         |            |

- bierner.github-markdown-preview
    这是一个插件包，包括了：
  - Markdown Preview GitHub Styling: 使得预览匹配 Github 风格的 CSS
  - Markdown Emoji: 添加 `:emoji:` 支持
  - Markdown Checkboxes: 添加 `[ ]` 任务列表支持
  - Markdown yaml Preamble: `添加` yaml 渲染支持。确保设置了 `"markdown.previewFrontMatter": "show"`
  - Markdown Footnotes: 添加 `[^1]` 脚注支持
  - Markdown Mermaid: 添加 Mermaid 支持
