> https://web.qianguyihao.com/#%E5%89%8D%E8%A8%80
>
> https://www.bilibili.com/video/BV1BT4y1W7Aw/

# 配置

## 设置

左下角打开设置，比较方便。

![img](打开设置.png)

+ 用户设置：全局生效
+ 工作区设置：只对当前项目生效，优先级更高。保存在`.vscode/settings.json`中，可以提交到git，共享给团队其他成员。
+ 右上角icon可以打开json文件形式的设置

![](两种设置方式.png)

## 配置

### 面包屑导航

用户设置 -> 工作台 -> 导航路径  => 打开

![](面包屑导航.png)

### 显示代码行号

`Editor: Line Numbers` => on

### 右侧显示代码缩略图

`Editor: Minimap` => on

### 高亮光标当前所在行

1. `Editor.renderLineHighlight` => `all / line`
2. 设置里增加以下内容，意思是
   1. 修改光标所在行的背景色
   2. 修改光标所在行的边框色

```json
"workbench.colorCustomizations": {
    "editor.lineHighlightBackground": "#00000090",
    "editor.lineHighlightBorder": "#ffffff30"
}
```

### 文件自动保存

`Files : Auto Save` => off

在配置了保存自动格式化的情况下，会导致写代码的时候一直被自动格式化，很难受。

### 保存代码后是否立刻格式化

`Editor.formatOnSave` => off

### 热退出，关闭时记住未保存的文件

`Files: Hot Exit` => `onExit`

### 粘贴内容是否自动格式化

`Editor: Format On Paste` => `on`

### 字体大小

`Editor: Font Size`

### 空格和制表符

#### 是否根据文件内容自动检测用空格还是制表符

`Editor: Detect Indentation` => `off`

#### 使用Tab时插入空格

`Editor: Insert Spaces` => `on`

#### 制表符等于多少空格

`Editor: Tab Size` => 4

这个设置在 Prettier 插件里也可以设置

#### 保存时自动去掉行末空格

`Files: Trim Trailing Whitespace` => `on`

#### 直观显示空格和制表符

`Editor: Render Whitespace` => all

### 删除文件是否弹出确认框

`Explorer: Confirm Delete` => `on`

### 在新窗口打开文件/文件夹

`Window: Open Files In New Window` => `on`

`Window: Open Folders In New Window` => `on`

### 重新打开VSCode时， 是否展示之前的窗口

`Window: Restore Windows` => `all`

### 文件展示在文件夹之前

Explorer >> Sort Order : filesFirst

### 工作区的 Explorer 文件夹顺序

打开保存的 code-workspace 文件，调整里面的 folders 里的顺序即可

# 插件

## 插件市场

https://marketplace.visualstudio.com/vscode

- Featured：由 VS Code团队精心推荐的插件。
- Trending：近期热门插件。
- Most Popular：按总安装量排序的插件。
- Recently Added：最新发布的插件。

## 推荐插件

### 页面展示

| 插件名                   | 推荐 | 作用                                                                         |
| ------------------------ | ---- | ---------------------------------------------------------------------------- |
| Bracket Pair Colorizer 2 | √    | 彩虹括号                                                                     |
| highlight-icemode        | √    | 相同代码高亮，和 `Editor: selection highlight`一样，用插件时可以关闭默认设置 |
| vscode-icons             |      | 根据文件后缀显示不同图标                                                     |
| indent-rainbow           |      | 突出显示代码缩进                                                             |
| Better Comments          |      | 注释色彩，醒目、带分类                                                       |

### 代码管理

| 插件名          | 推荐 | 作用             |
| --------------- | ---- | ---------------- |
| GitLens         | √    | git相关          |
| Local History   | √    | 维护本地历史记录 |
| Project Manager |      | 管理常用项目     |
| Waka Time       |      | 统计写代码的时间 |

### 代码格式化

| 插件名             | 推荐 | 作用                                                                                           |
| ------------------ | ---- | ---------------------------------------------------------------------------------------------- |
| Code Spell Checker |      | 单词拼写检查                                                                                   |
| TODO Highlight     |      | 在命令面板中，Todohighlist可以显示所有的TODO（必须是大写的）                                   |
| Prettier           |      | 代码格式化<br />在项目跟目录下新建 `.prettierrc`<br />默认使用2个空格，可以在通用设置里改为4个 |
| ESLint             |      | 代码格式校验                                                                                   |

Prettier设置文件参考

```json
{
    "printWidth": 150,
    "tabWidth": 4,
    "semi": true,
    "singleQuote": true,
    "trailingComma": "es5",
    "tslintIntegration": true,
    "insertSpaceBeforeFunctionParenthesis": false
}
```

### 前端相关

| 插件名                                        | 推荐 | 作用                                             |
| --------------------------------------------- | ---- | ------------------------------------------------ |
| Live Server                                   | √    | 浏览器中实时预览                                 |
| open in browser                               |      | HTML文件中，右键菜单增加 Open In Default Browser |
| Auto Close Tag                                | √    | 自动闭合配对标签                                 |
| Auto Rename Tag                               | √    | 同时修改匹配的标签                               |
| HTML CSS Support                              | √    | 快速补全HTML和CSS                                |
| Vetur                                         |      | Vue集成插件                                      |
| ES7 React/Redux/GraphQL/React-Native snippets |      | React/Redux/react-router 的语法智能提示          |
| JavaScript(ES6) code snippets                 |      | ES6 语法智能提示，支持快速输入                   |
| javascript console utils                      | √    | Cmd + Shift + L 可以快速出现 `console.log()`     |
| JS-CSS-HTML Formatter                         |      | 保存文件自动格式化 HTML CSS JS 代码              |
| Image Preview                                 |      | 鼠标移动到url时，预览图片，并显示尺寸            |
| CSS Peek                                      |      | 快速查看某个元素上的CSS样式                      |
| Vue CSS Peek                                  |      | 增加了对Vue文件的支持                            |
| Color Info                                    |      | 预览CSS中颜色的信息                              |

### Markdown

| 插件名                          | 推荐 | 作用                        |
| ------------------------------- | ---- | --------------------------- |
| Markdown Preview Github Styling |      | 以 GitHub 风格预览 Markdown |
| Markdown All in One             |      | 一些便利的快捷键            |
| Markdown Shortcuts              |      | 一些便利的快捷键            |

### 其他

| 插件名                          | 推荐 | 作用                        |
| ------------------------------- | ---- | --------------------------- |
| Polacode-2020                   |      | 生成代码截图，做PPT时用     |

# 快捷键

### 1. 工作区快捷键

| Mac 快捷键           | Win 快捷键               | 作用                                          | 备注                 |
| :------------------- | :----------------------- | :-------------------------------------------- | :------------------- |
| **Cmd + Shift + P**  | **Ctrl + Shift + P**，F1 | 显示命令面板                                  |                      |
| **Cmd + B**          | **Ctrl + B**             | 显示/隐藏侧边栏                               | 很实用               |
| `Cmd + \`            | `Ctrl + \`               | **拆分为多个编辑器**                          | 【重要】抄代码利器   |
| **Cmd + 1、2**       | **Ctrl + 1、2**          | 聚焦到第 1、第 2 个编辑器                     | 同上重要             |
| **Cmd + +、Cmd + -** | **ctrl + +、ctrl + -**   | 将工作区放大/缩小（包括代码字体、左侧导航栏） | 在投影仪场景经常用到 |
| Cmd + J              | Ctrl + J                 | 显示/隐藏控制台                               |                      |
| **Cmd + Shift + N**  | **Ctrl + Shift + N**     | 重新开一个软件的窗口                          | 很常用               |
| Cmd + Shift + W      | Ctrl + Shift + W         | 关闭软件的当前窗口                            |                      |
| Cmd + N              | Ctrl + N                 | 新建文件                                      |                      |
| Cmd + W              | Ctrl + W                 | 关闭当前文件                                  |                      |

## 前端相关

快捷输入后，按`Tab`或者`Enter`。

| 快捷输入         | 功能                                               |
| ---------------- | -------------------------------------------------- |
| !                | 生成html骨架                                       |
| h1 / h2... / p … | h1等标签                                           |
| .class_name      | 创建一个带有class属性，且值为`class_name`的div标签 |
| `div.class_name` | 同上                                               |
| #id_value        | 创建一个带有id属性，且值为`id_value`的div标签      |
| `div#id_value`   | 同上                                               |



