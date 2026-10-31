# @perrylink/dsh-checkers-suite

> **包名：** 请安装 `@perrylink/dsh-checkers`（当前 shim）。`@perrylink/dsh-checkers-suite` 是已弃用别名，现已指向这里。

**53 个 PerryLink 合规核查器**的一条命令安装包。

```sh
# npm (once the new-package 2FA approval is available)
dsh plugin --profile web add @perrylink/dsh-checkers-suite

# available now: the GitHub git channel
dsh plugin --profile web add github:PerryLink/dsh-checkers
```

它会安装全部合规插件，并通过一个 bundle 层插入 53 行 Cordis 配置。每个合规插件
仍保留自己的 npm 名、规则包、README 和版本；本包只是套件入口。

**范围：** 中国领域文档核对（外贸、报关、招投标、HSE、医疗、法律、公文、制造）。
每个合规插件 只提示差异，不作法律/医疗/海关定性。确切清单与版本见 `checkers.json`。

**卸载：** `dsh plugin --profile web remove @perrylink/dsh-checkers-suite` 移除套件行；
单独安装的合规插件 仍需分别移除。

Apache-2.0。合规插件版本变化后运行 `node build.mjs` 重新生成。
