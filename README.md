# Bao Qinghan

一个手绘涂鸦风格的个人网站，记录设计、代码与日常灵感。

[访问网站](https://boooooobbb.github.io/baoqinghan/)

## 页面

- `/`：个人介绍、精选作品、最近记录、近况与联系方式
- `/about/`：关于我
- `/projects/`：作品列表
- `/projects/personal-site/`：个人网站项目详情
- `/notes/`：记录列表
- `/notes/building-this-site/`：网站搭建记录
- `/404.html`：未找到页面

## 更新内容

网站是原生 HTML、CSS、JavaScript 静态页面，无运行时框架依赖。

1. 在 `src/pages/` 编辑页面正文，`{{root}}` 表示站点根路径，支持 GitHub Pages 子目录。
2. 在 `src/pages.json` 编辑标题、描述和导航归属，新增页面也在这里登记。
3. 公共样式与交互在 `assets/site.css` 和 `assets/site.js`；共享导航、页脚及元信息在 `scripts/build.py`。
4. 使用 Python 3 运行：

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000
```

打开 `http://localhost:8000/` 预览。提交生成文件到 `main` 后由现有 GitHub Pages 配置发布。根目录 HTML 和 `dist/` 均为生成结果，请勿单独编辑；构建脚本同步两份静态文件。`.openai/hosting.json` 的原有身份和设置保留。

发布基址配置在 `scripts/build.py` 的 `ORIGIN`；更换域名时也需更新 404 页的回首页路径。

新项目、文章请使用真实内容；目前仅发布个人网站项目和其搭建记录，未公开的社交账号不显示。

## 个人收藏与文章

电影和游戏在 `src/collections.json` 中维护，按数组顺序展示。封面存放在 `assets/covers/`，是使用内置 ImageGen 生成的手绘演绎；完整提示词见 `assets/covers/prompts.json`。展示封面、名称和一句话简评，不包含评分。

文章列表当前为空。旧建站记录保留原 URL，但不出现在列表中。

安装构建依赖后生成页面：

```sh
python3 -m pip install -r requirements.txt
python3 scripts/build.py
python3 scripts/check.py
```

新增文章：在 `content/articles/` 新建 `my-first-post.md`，文件名使用英文小写字母、数字和连字符。文件顶部是 JSON 元数据，空行后是 Markdown 正文，例如：

```markdown
{"title":"一篇新文章","date":"2026-11-01","summary":"文章摘要。"}

## 从这里开始

正文支持链接、列表、表格和代码块。标题由元数据生成，正文标题从二级开始。
```

重新构建后，文章会按日期倒序出现在 `/notes/`，详情路径是 `/notes/my-first-post/`，并自动加入 sitemap。元数据错误、重复路径或空正文会阻止构建。Markdown 是仓库作者维护的可信内容，不接受访客提交。移除已发布文章时需一并删除其根目录和 dist 中的生成页面。
