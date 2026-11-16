"""Generate crawlable GitHub Pages HTML using the Python standard library."""
import json
import shutil
from html import escape as e
from pathlib import Path
from urllib.parse import urlparse
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
BASE = 'https://2716190547.github.io/ai-free-relay/'
REPO = 'https://github.com/2716190547/ai-free-relay'
sites = json.loads((ROOT / 'data/sites.json').read_text())
assert len({s['slug'] for s in sites}) == len(sites)
for s in sites:
    assert s['slug'].replace('-', '').isalnum()
    for field in ['url', 'source', 'referral_url']:
        if s[field]:
            assert urlparse(s[field]).scheme == 'https' and urlparse(s[field]).netloc
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
paths = []
def page(path, title, description, content, schema=None):
    depth = path.count('/')
    root = '../' * depth or './'
    canonical = BASE + ('' if path == 'index.html' else path.replace('index.html', ''))
    structured = {'@context':'https://schema.org','@type':'WebPage','name':title,'description':description,'url':canonical,'inLanguage':'zh-CN'}
    if schema:
        structured.update(schema)
    html = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} · 额度拾集</title><meta name="description" content="{e(description)}"><link rel="canonical" href="{canonical}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="website"><meta property="og:locale" content="zh_CN"><meta name="theme-color" content="#2457db"><link rel="icon" href="{root}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{root}style.css"><script type="application/ld+json">{json.dumps(structured,ensure_ascii=False).replace('<', chr(92)+'u003c')}</script></head><body><a class="skip" href="#main">跳到正文</a><header><a class="brand" href="{root}"><span class="mark">拾</span> 额度拾集</a><nav aria-label="主导航"><a href="{root}#directory">找免费额度</a><a href="{root}guide/">领取指南</a><a href="{root}about/">收录规则</a><a href="{REPO}">GitHub ↗</a></nav></header><main id="main">{content}</main><footer><strong>额度拾集</strong><span>把免费额度的条件，放在领取按钮前。</span><a href="{root}about/">来源与邀请披露</a><a href="{REPO}/issues">提交 / 纠错</a><p>独立信息目录，与所列平台无隶属关系。活动以各站最新公告为准。</p></footer></body></html>'''
    target=OUT/path; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(html)
    paths.append(canonical)
def cta(s):
    return f'<a class="button" href="{e(s["referral_url"] or s["url"],quote=True)}" rel="sponsored nofollow noopener">{ "通过邀请链接访问" if s["referral_url"] else "访问官网"} ↗</a>'
cards=''
for s in sites:
    cards+=f'''<article class="entry" data-search="{e(s['name']+' '+s['category']+' '+s['benefit'])}" data-category="{s['category']}"><div><span class="tag">{s['category']}</span><h3><a href="sites/{s['slug']}/">{s['name']}</a></h3><p>{s['note']}</p></div><div class="benefit"><small>福利类型</small><strong>{s['benefit']}</strong><span>额度与条件待核实</span></div><div class="actions"><a href="sites/{s['slug']}/">查看领取条件</a>{cta(s)}</div></article>'''
page('index.html','免费 AI 中转站导航与额度领取指南','聚合 AI 中转站免费额度线索，对照注册、签到与积分条件。提供独立详情、资料来源及邀请链接披露。',f'''<section class="hero"><div><span class="eyebrow">给 AI 编程多一点免费空间</span><h1>免费额度，<br>先看条件再领取。</h1><p>发现 AI 中转站的注册福利与签到活动。<br>不把积分当现金，也不把历史活动当承诺。</p><a class="button" href="#directory">浏览福利目录 ↓</a></div><aside class="ticket"><span>领取前核对</span><h2>每一份免费，<br>都有使用条件。</h2><ul><li>是否需要邀请或社群领取？</li><li>额度会过期吗？适用哪些模型？</li><li>签到是否有充值门槛？</li></ul><a href="guide/">阅读完整领取指南 ↗</a></aside></section><section class="notice"><strong>资料核对中</strong> 首批 6 个站点来自公开目录，尚未逐站实测领取。邀请入口如已配置会明确标识；未配置时直达官网。</section><section id="directory"><div class="section-head"><div><h2>免费额度目录</h2><p>先找适合的领取方式，再确认平台的最新规则。</p></div><span>资料整理：2026-11-16</span></div><div class="filters"><label>搜索站点 <input id="search" type="search" placeholder="名称、签到、积分…"></label><label>领取方式 <select id="category"><option value="">全部方式</option><option>注册福利</option><option>每日签到</option></select></label><output id="count" aria-live="polite">6 个站点</output></div><div id="entries">{cards}</div><p id="empty" hidden>没有匹配的站点，请换个关键词或选择全部方式。</p></section><section class="reading"><h2>把额度用明白</h2><a href="guide/">免费 AI 中转站怎么选？<span>领取步骤、计费单位与有效期</span></a><a href="about/">我们如何收录与推荐？<span>来源、核实标准与邀请收益披露</span></a></section><script src="app.js" defer></script>''',{'@type':'CollectionPage','mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':s['name'],'url':BASE+'sites/'+s['slug']+'/'} for i,s in enumerate(sites)]}})
for s in sites:
    page(f'sites/{s["slug"]}/index.html',f'{s["name"]} 免费额度与领取条件',f'了解 {s["name"]} 的{ s["benefit"]}活动线索、核实状态、官网入口及领取前需要确认的条件。',f'''<article class="prose"><a href="../../#directory">← 返回目录</a><span class="eyebrow">{s['category']}</span><h1>{s['name']}</h1><p class="lead">{s['note']}</p><div class="notice">核实状态：待人工核实。资料整理日期：{s['reviewed']}；不是活动确认日期或 API 实测日期。</div><h2>免费额度如何领取？</h2><p>先访问官网，核对当前活动公告，再按平台要求注册。本页暂不承诺可领取金额、模型可用性或到账时间。</p><dl><dt>福利线索</dt><dd>{s['benefit']}</dd><dt>具体额度 / 有效期</dt><dd>未核实，请以官网公告为准</dd><dt>邀请链接</dt><dd>{'已配置，站长可能获得奖励' if s['referral_url'] else '尚未配置，当前为无邀请码的官网入口'}</dd><dt>服务实测</dt><dd>未进行注册领取或 API 调用测试</dd></dl>{cta(s)}<h2>领取前确认这四项</h2><ul><li>注册赠送是否仍在进行，是否需要特定登录方式。</li><li>赠送单位是现金余额、站内额度还是积分。</li><li>是否需要进群、实名、邀请或充值。</li><li>哪些模型可以使用，额度何时过期。</li></ul><h2>来源与纠错</h2><p>活动线索来自 <a href="{s['source']}">AI Coding 福利站导航</a>，本文为独立整理，未复制原站邀请码。<a href="{s['url']}">平台官网</a>是确认最新规则的入口。</p><p>发现信息变化？<a href="{REPO}/issues/new">提交纠错</a>，请附公告链接及日期。</p><a href="../../guide/">继续阅读领取指南</a></article>''')
page('guide/index.html','免费 AI 中转站怎么选：领取与使用指南','解释免费 AI 中转站的注册赠送、签到额度、计费单位、活动有效期和客户端接入前的核对步骤。','''<article class="prose"><span class="eyebrow">领取指南</span><h1>先看规则，<br>再领免费额度。</h1><p class="lead">免费 AI 中转站通常是第三方 API 服务。免费活动的领取规则、计费倍率和可用模型，需要分别确认。</p><h2>注册奖励和每日签到有什么区别？</h2><p>注册奖励通常只在首次满足条件时发放；每日签到需要重复操作，且可能有充值或活跃度要求。比较时分别记录一次性奖励和后续领取条件，不把它们当作永久免费承诺。</p><h2>为什么不能只比较赠送金额？</h2><p>同样标为「100」的额度，可能是站内单位、积分或有分组限制的余额。先查看模型输入输出价格、倍率、有效期，再估算自己的任务能调用多少次。不同站点的面额不直接相加。</p><h2>第一次领取怎么操作？</h2><ol><li>阅读官网公告，确认活动仍有效。</li><li>确认邀请奖励条件；如需邀请码，在提交注册前检查。</li><li>领取后核对余额、有效期与可用分组。</li><li>从控制台复制准确的 API 地址与模型 ID。</li><li>用一条不含敏感信息的短请求验证，并观察实际扣费。</li></ol><h2>能直接用于 Claude Code、Codex 或 Cursor 吗？</h2><p>取决于平台支持的协议与客户端配置要求，不能仅凭模型名称判断。请核对平台文档提供的 Base URL、模型 ID 和兼容协议；本目录不猜测接入地址。</p><h2>第三方中转适合什么用途？</h2><p>适合先用非敏感示例做功能体验。中转服务会处理你发送的请求，上传私人资料或工作代码前，请确认服务的数据处理规则与自己的使用权限。</p><h2>本站的邀请链接如何标识？</h2><p>按钮会明确写明「通过邀请链接访问」。站长可能因此获得奖励；未配置邀请链接时仅提供官网入口。邀请奖励不作为排序依据。</p><a href="../#directory">返回目录，查看站点</a></article>''')
page('about/index.html','收录规则、资料来源与邀请披露','了解额度拾集的收录方法、核实状态、邀请收益披露和信息纠错流程。','''<article class="prose"><h1>推荐之前，<br>先把依据写清楚。</h1><h2>这个站做什么？</h2><p>额度拾集是免费的第三方 AI 中转站活动目录，帮助读者找到福利线索并核对领取条件。首批条目参考公开导航整理，当前均未完成领取实测。</p><h2>收录与排序</h2><p>记录站点官网、活动类型、来源、核实状态与整理日期。当前采用固定编辑顺序，不提供未经验证的最好、最快或最稳定排名。后续新增活动需提供可公开核对的公告来源。</p><h2>核实标准</h2><p>能打开首页不等于 API 可用，公告存在不等于已经成功领取。未来完成核实后，会分别注明公告核对时间、领取条件和实际测试范围；不会用构建时间冒充核实时间。</p><h2>邀请收益披露</h2><p>网站预留站长个人邀请链接。使用后站长可能获得额度或佣金，具体收益以对应平台规则为准。未配置邀请链接的站点直达官网；本站不沿用参考网站作者的邀请码。</p><h2>资料来源与纠错</h2><p>首批线索参考 <a href="https://panxunying.github.io/ai-coding-welfare/">AI Coding 福利站导航</a>，每个详情页均链接来源和官网。本文内容为独立撰写，不代表原站或服务商的背书。</p><p><a href="https://github.com/2716190547/ai-free-relay/issues">通过 GitHub Issues 投稿或纠错</a>，请附站点名称、官方公告、活动条件及日期。不要提交 API Key 或账户凭据。</p></article>''')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc></url>' for u in paths)+'</urlset>')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n')
(OUT/'.nojekyll').touch()
for name in ['style.css','app.js','favicon.svg']:
    shutil.copy(ROOT/name,OUT/name)
print(f'Built {len(paths)} pages')
