# 额度拾集

免费 AI 中转站活动目录。静态 HTML，无第三方运行时依赖，部署到 GitHub Pages。

网站：https://2716190547.github.io/ai-free-relay/

## 本地构建

```sh
python3 scripts/build.py
python3 scripts/check.py
```

输出位于 `dist/`。推送 main 自动构建并部署。

## 填写你的邀请链接

编辑 `data/sites.json` 对应站点的 `referral_url`，填入完整 HTTPS 邀请链接。留空时按钮直达官网，不含原参考站邀请码。填写后还应更新 `scripts/build.py` 中首页及收录规则页的「尚未配置」文案。

站点资料当前全部待核实。`reviewed` 是资料整理日期，不是领取测试日期。不要仅修改 `verified` 就宣称实测，应同时在详情模板中补充实际证据和核实范围。

## 内容规划

1. 已完成：可筛选目录、六个独立站点页、领取指南、收录规则、邀请披露。
2. 下一步：逐站确认活动公告、计费单位、有效期、适用模型及领取门槛，填写个人邀请链接。
3. 运营：每周核查活动；失效条目注明失效原因；发布有证据的对比文章，避免同质页面和无依据排名。

## 搜索与 AI 检索

正文直接输出 HTML；每页独立 title、description、canonical、Open Graph；首页 CollectionPage / ItemList 结构化数据；sitemap.xml；语义标题、内链及来源。

上线后在 Google Search Console、Bing Webmaster Tools 验证网站并提交 sitemap。GitHub 项目站的 robots.txt 不在域名根路径，不能作为该域名爬虫控制文件；当前页面未设置 noindex。将来绑定独立域名时统一修改 BASE 和站点链接，再提交新 sitemap。

不保证排名或 AI 引用。没有伪造评分、实测、在线状态、金额或更新日期。未添加不具备排名保证的 llms.txt。

参考资料：https://panxunying.github.io/ai-coding-welfare/ 。内容独立撰写，仅将其作为活动线索来源。
