<div align="center">

# Neatly

**让 AI 做的 HTML 页面，看起来像设计师做的。**

给 Claude Code、Codex、Cursor 等 AI 编程工具用的 skill。<br>
报告、幻灯片、数据看板、落地页、文档，一套克制的视觉系统全部搞定。

[在线演示](https://neatly.kehaoran.ai) · [案例](#五个版式一套风格) · [安装](#安装) · [English](README.md)

[![MIT license](https://img.shields.io/badge/license-MIT-171717)](LICENSE)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-2e4bff)](#安装)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-2e4bff)](#安装)
[![No build step](https://img.shields.io/badge/build%20step-none-525252)](#不用-ai-也能用)

</div>

![同一份三季度报告：左边是 AI 默认做出来的页面，右边是 Neatly 做的](docs/compare.png)

```bash
npx skills add kehaoran-ai/neatly
```

装好以后，像平时一样让 AI 做页面就行。没有别的配置。

## AI 做的页面，一眼就能认出来

让任何一个模型做 HTML 报告，拿到的都是同一张脸：紫到蓝的渐变、带火箭 emoji 的发光大标题、一排三张卡片、全大写的小标签，再配一句「解锁无缝增长」。这不是模型审美差，而是它手里没有一套设计系统，只能退回到它见过的所有落地页的平均值。

Neatly 给它一套系统：

- **一套风格。** 中性灰、一种无衬线字体、方格纸上的线稿图、只有一个主题色，改一行就能换。
- **五个起步版式。** AI 只管写内容，不用自己发明结构。
- **写作规矩。** 标题写成带数字的结论句。不写口号，不写套话，用户没说过的事不编。
- **检查脚本。** 常见的 AI 痕迹，在页面交给你之前就被拦下。

## 五个版式，一套风格

下面每个案例都是一个单文件 HTML，点图就能打开线上页面。

| | |
|---|---|
| [![报告](site/img/report.png)](https://neatly.kehaoran.ai/examples/report.html)<br>**[报告](https://neatly.kehaoran.ai/examples/report.html)**：复盘、分析、备忘、调研总结 | [![幻灯片](site/img/deck.png)](https://neatly.kehaoran.ai/examples/deck.html)<br>**[幻灯片](https://neatly.kehaoran.ai/examples/deck.html)**：16:9，方向键翻页，可直接打印成 PDF |
| [![数据看板](site/img/dashboard.png)](https://neatly.kehaoran.ai/examples/dashboard.html)<br>**[数据看板](https://neatly.kehaoran.ai/examples/dashboard.html)**：关键指标配走势小线、图表、表格、动态 | [![落地页](site/img/landing.png)](https://neatly.kehaoran.ai/examples/landing.html)<br>**[落地页](https://neatly.kehaoran.ai/examples/landing.html)**：首屏、卖点、价格、常见问题、收尾按钮 |
| [![文档](site/img/docs.png)](https://neatly.kehaoran.ai/examples/docs.html)<br>**[文档](https://neatly.kehaoran.ai/examples/docs.html)**：教程和 API 页，分步说明，代码一键复制 | **换个颜色看看。** 在[演示站](https://neatly.kehaoran.ai)上切换主题色，所有案例实时跟着变，还能看到每个案例背后的起步文件。 |

五个版式在电脑、平板、手机上都能正常显示，打印也整齐。

## 一个页面是怎么做出来的

1. **你用大白话提要求。** 「把 9 月的销售做成一份 HTML 报告：营收 18,400 美元，环比涨 12%。」版式由 skill 自己选。
2. **AI 只写正文。** `make.py` 把设计系统原样复制进页面，AI 写大约 80 行内容，不用写 800 行 CSS。
3. **检查脚本过一遍。** 有错就改，改完才交给你。
4. **页面打开。** 一个文件，离线能看，手机能看，打印也整齐。

```text
$ python3 scripts/make.py report body.html september.html --title "September sales"
wrote september.html
ok  september.html  (0 errors, 0 warnings)
```

我们找了两个从没见过 Neatly 的全新 AI 来测，只给它们这个 skill。一份报告、一份幻灯片，都是一次就通过检查，各用了 6 到 8 步。

## 安装

**Claude Code**

```
/plugin marketplace add kehaoran-ai/neatly
/plugin install neatly@neatly
```

**任何支持 skill 的工具**（Claude Code、Codex、Cursor 等）

```bash
npx skills add kehaoran-ai/neatly
```

**手动安装**

```bash
git clone https://github.com/kehaoran-ai/neatly
cp -r neatly/skills/neatly ~/.claude/skills/
```

## 可以这样用

```
把这些会议记录做成 6 页幻灯片，周一开会用。
```

```
用这个 CSV 做一个数据看板，看注册、激活和收入。
```

```
写一页 CLI 安装文档，命令要能一键复制。
```

```
把这个页面改好看一点。（附上现有的 HTML 文件）
```

## 换成你的颜色

所有颜色都跟着一个变量走。在页面 `<body>` 开头加一行：

```html
<style>:root { --nt-accent: #e4572e; }</style>
```

也可以直接跟 AI 说「用我们的品牌色 #e4572e」。想先看效果，在任意 Neatly 页面的地址后面加 `?accent=e4572e`。

中文和日文页面不用额外设置：整行文字交给系统的中日文字体排，中文标题里夹的英文单词和汉字粗细一致。

## 检查脚本

```bash
python3 skills/neatly/scripts/check.py page.html
```

| 直接判不通过 | 给出提醒 |
|---|---|
| 衬线或斜体标题，Inter 和 Geist 字体 | 绕开主题色变量、写死的色值 |
| 渐变、发光、模糊和毛玻璃 | 过重的阴影 |
| 区块左边的彩色竖条 | 卡片或强调色用得太多 |
| 一排正好三张卡片 | 破折号超过两个 |
| 全大写文字、emoji、深色模式样式 | 「seamless」「unlock」这类套话 |
| 没替换的占位符，缺少 viewport | |

不是用 Neatly 做的页面也能拿来跑，一下就能看出它为什么像 AI 做的。

## 不用 AI 也能用

`skills/neatly/neatly.css` 可以单独使用：从 `skills/neatly/layouts/` 复制一个文件，替换掉里面的 `TODO`，用浏览器打开。`neatly.js` 是可选的，负责画图表、翻幻灯片、代码复制按钮和目录高亮。所有类名见 [`reference/components.md`](skills/neatly/reference/components.md)。

## 常见问题

**支持哪些 AI 工具？** 能加载 skill 的都行：Claude Code 可以按插件或 skill 安装，Codex、Cursor 等通过 `npx skills` 安装。如果你的工具不支持 skill，把仓库克隆下来，让它按 `skills/neatly/SKILL.md` 做。

**页面需要联网吗？** 只有 Montserrat 字体要联网，离线时自动换成系统字体，没有其他外部请求。

**为什么不用 Tailwind 或组件库？** 产出必须是一个文件：能发邮件、能双击打开、能直接扔进聊天窗口。不需要构建，不加载外部脚本，什么都不用装。

**能换字体吗？** 和主题色一样，改 `--nt-sans` 变量。请保持无衬线，检查脚本故意拦衬线标题。

**有深色模式吗？** 没有。把一种模式做好，就是这个项目的态度。

## 目录

```
skills/neatly/
  SKILL.md              AI 怎么用 Neatly
  neatly.css            视觉系统，内联进每个页面
  neatly.js             图表、幻灯片、复制按钮、目录高亮（可选）
  layouts/              五个起步文件
  reference/            组件手册
  scripts/make.py       用版式加正文生成页面
  scripts/check.py      检查脚本
examples/               五个做好的页面
site/                   演示站
```

改了 CSS 或 JS 之后，运行 `python3 scripts/build.py`，重新内联进所有版式和案例。

## 参与贡献

欢迎提 issue 和 PR，尤其是检查脚本还没拦住的 AI 痕迹，以及某个版式不够用的场景。请附上截图。

## 许可

MIT，作者 [柯浩然](https://github.com/kehaoran-ai)。如果 Neatly 帮你躲过了一次紫色渐变，点个 star，能让更多人找到它。
