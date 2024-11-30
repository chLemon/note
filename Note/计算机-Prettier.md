# Prettier

官方文档：<https://prettier.io/docs/>

一个好用的代码格式化工具

Prettier 本身是一个独立的程序，安装的 VsCode 插件目前使用的内核版本还不够高，在 markdown 时会触发一些 bug

可以在 VsCode 设置文件里设置一些东西，其本身也提供了一套完善复杂的设置文件的机制。如：

在项目根目录下新建 `.prettierrc`

默认使用 2 个空格，可以在通用设置里改为 4 个

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

## 1. 安装

```bash
# 本地安装 Prettier
npm install --save-dev --save-exact prettier

# 创建一个空的配置文件，让编辑器和其他工具知道我正在使用 Prettier
node --eval "fs.writeFileSync('.prettierrc','{}\n')"

# 接下来，创建一个 `.prettierignore` 文件，让 Prettier CLI 和编辑器知道哪些文件不需要格式化。以下是示例：
node --eval "fs.writeFileSync('.prettierignore','# Ignore artifacts:\nbuild\ncoverage\n')"
```

> TIP
>
> 如果 .gitignore 文件与 Prettier 运行的目录相同，Prettier 将遵循 .gitignore 文件中指定的规则。您也可以基于 .eslintignore 文件（如果有）来创建 .prettierignore 文件。
>
> 如果您的项目尚未准备好格式化 HTML 文件，请添加 \*.html 。

使用 Prettier 格式化所有文件：

```bash
npx prettier . --write
```

> INFO
>
> `npx` 是什么？ `npx` 是 `npm` 附带的，可以让你运行本地安装的工具。为了简洁起见，我们将在本文件的其余部分省略 `npx` 部分！

> WARNING
>
> 如果您忘记先安装 Prettier， `npx` 会临时下载最新版本。使用 Prettier 时，这可不是什么好主意，因为我们每次发布都会更改代码格式！在您的 `package.json` 中保存一个固定版本的 Prettier 非常重要。而且它的速度也更快。

`prettier --write .` 非常适合格式化所有内容，但对于大型项目来说，可能需要一些时间。您可以运行 `prettier --write app/` 来格式化某个目录，或者运行 `prettier --write app/components/Button.js` 来格式化某个文件。或者使用类似 `prettier --write "app/**/*.test.js"` 的 _glob_ 来格式化目录中的所有测试文件（请参阅 [fast-glob](https://github.com/mrmlnc/fast-glob#pattern-syntax) 了解支持的 glob 语法）。

如果您已设置 CI，请运行以下命令，以确保每个人都运行 Prettier。这可以避免合并冲突和其他协作问题！

```bash
npx prettier . --check
```

`--check` 与 `--write` 类似，但仅检查文件是否已格式化，而不是覆盖它们。`prettier --write` 和 `prettier --check` 是运行 Prettier 最常用的方法。

> NOTE
>
> 别忘了常规的本地安装！编辑器插件会选择您本地的 Prettier 版本，确保您在每个项目中都使用正确的版本。（您肯定不希望编辑器因为使用了比项目更新的 Prettier 版本而意外造成大量更改！）
>
> 并且能够从命令行运行 Prettier 仍然是一个很好的后备，并且是 CI 设置所需要的。