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
