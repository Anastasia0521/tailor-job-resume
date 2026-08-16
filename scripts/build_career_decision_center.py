#!/usr/bin/env python3
import argparse
import html
import json
import re
from pathlib import Path


def esc(value):
    return html.escape(str(value or ""))


def slug(value, fallback):
    text = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff_-]+", "-", str(value or "")).strip("-")
    return text or fallback


def render_table(table):
    columns = table.get("columns", [])
    rows = table.get("rows", [])
    head = "".join(f"<th>{esc(column)}</th>" for column in columns)
    body = []
    for row in rows:
        values = row if isinstance(row, list) else [row.get(column, "") for column in columns]
        body.append("<tr>" + "".join(f"<td>{esc(value)}</td>" for value in values) + "</tr>")
    caption = f"<caption>{esc(table.get('title'))}</caption>" if table.get("title") else ""
    return f'<div class="table-wrap"><table>{caption}<thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def render_section(section, index):
    section_id = slug(section.get("id") or section.get("title"), f"section-{index}")
    cards = "".join(
        f'<article class="metric {esc(card.get("tone", ""))}"><b>{esc(card.get("title"))}</b>'
        f'<strong>{esc(card.get("value"))}</strong><span>{esc(card.get("note"))}</span></article>'
        for card in section.get("cards", [])
    )
    paragraphs = "".join(f"<p>{esc(text)}</p>" for text in section.get("paragraphs", []))
    bullets = section.get("bullets", [])
    list_html = "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in bullets) + "</ul>" if bullets else ""
    tables = "".join(render_table(table) for table in section.get("tables", []))
    subsections = []
    for sub in section.get("subsections", []):
        sub_paragraphs = "".join(f"<p>{esc(text)}</p>" for text in sub.get("paragraphs", []))
        sub_bullets = sub.get("bullets", [])
        sub_list = "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in sub_bullets) + "</ul>" if sub_bullets else ""
        sub_tables = "".join(render_table(table) for table in sub.get("tables", []))
        subsections.append(f'<div class="subsection"><h3>{esc(sub.get("title"))}</h3>{sub_paragraphs}{sub_list}{sub_tables}</div>')
    content = f'<div class="metrics">{cards}</div>{paragraphs}{list_html}{tables}{"".join(subsections)}'
    return section_id, f'''<section id="{section_id}" class="report-section">
      <button class="section-toggle" type="button" onclick="toggleSection(this)" aria-expanded="true"><span>{esc(section.get("title"))}</span><i>收起</i></button>
      <div class="section-content">{content}</div>
    </section>'''


def render(data):
    sections = []
    nav = []
    for index, section in enumerate(data.get("sections", []), 1):
        section_id, section_html = render_section(section, index)
        sections.append(section_html)
        nav.append(f'<a href="#{section_id}">{esc(section.get("title"))}</a>')
    embedded = data.get("embedded_data", {})
    embedded.setdefault("profile", {key: data.get(key) for key in ("name", "title", "generated_at")})
    embedded_json = json.dumps(embedded, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    result = TEMPLATE
    replacements = {
        "{{NAME}}": esc(data.get("name")),
        "{{TITLE}}": esc(data.get("title") or "求职决策中心"),
        "{{SUBTITLE}}": esc(data.get("subtitle")),
        "{{GENERATED_AT}}": esc(data.get("generated_at")),
        "{{NAV}}": "".join(nav),
        "{{SECTIONS}}": "".join(sections),
        "{{EMBEDDED_DATA}}": embedded_json,
    }
    for key, value in replacements.items():
        result = result.replace(key, value)
    return result


TEMPLATE = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{NAME}}｜{{TITLE}}</title>
<style>
:root{--ink:#17202a;--muted:#667085;--paper:#fff;--line:#d9dee7;--brand:#174f88;--brand-soft:#edf4fb;--bg:#f4f6f8}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.72 system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}.toolbar{position:sticky;top:0;z-index:20;display:flex;gap:8px;flex-wrap:wrap;padding:10px 18px;background:#17202af2;box-shadow:0 2px 10px #0002}.toolbar button{border:1px solid #ffffff45;border-radius:6px;background:#263747;color:#fff;padding:8px 12px;cursor:pointer}.toolbar button.primary{background:#19714a}.shell{display:grid;grid-template-columns:250px minmax(0,920px);gap:24px;max-width:1220px;margin:24px auto;padding:0 20px}.sidebar{position:sticky;top:76px;align-self:start;background:#fff;border:1px solid var(--line);border-radius:10px;padding:18px}.sidebar h1{font-size:19px;margin:0 0 3px}.sidebar .sub{color:var(--muted);font-size:13px;margin-bottom:15px}.sidebar input{width:100%;padding:9px;border:1px solid var(--line);border-radius:6px;margin-bottom:12px}.sidebar nav{display:grid;gap:3px}.sidebar a{color:#354052;text-decoration:none;padding:7px 8px;border-radius:5px}.sidebar a:hover{background:var(--brand-soft);color:var(--brand)}main{min-width:0}.cover,.report-section{background:var(--paper);border:1px solid var(--line);border-radius:10px;margin-bottom:18px;box-shadow:0 2px 8px #1520300c}.cover{padding:34px}.cover h2{font-size:30px;line-height:1.2;margin:0 0 10px}.cover p{color:var(--muted);margin:0}.section-toggle{width:100%;display:flex;align-items:center;justify-content:space-between;border:0;background:transparent;padding:18px 24px;font:700 20px/1.3 inherit;color:var(--ink);cursor:pointer;text-align:left;border-bottom:1px solid var(--line)}.section-toggle i{font-size:12px;color:var(--muted);font-style:normal}.section-content{padding:22px 24px}.section-content p{margin:0 0 13px;text-align:justify}.section-content ul{padding-left:22px}.subsection{border-top:1px dashed var(--line);padding-top:14px;margin-top:18px}.subsection h3{margin:0 0 8px;color:var(--brand)}.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:12px;margin-bottom:16px}.metric{border:1px solid var(--line);border-radius:8px;padding:13px;background:#fafbfc}.metric b,.metric span{display:block;color:var(--muted);font-size:12px}.metric strong{display:block;font-size:22px;margin:3px 0}.metric.good{border-color:#a8d6bf;background:#f1faf5}.metric.warn{border-color:#efd59d;background:#fff9ed}.table-wrap{overflow:auto;margin:12px 0 18px}table{width:100%;border-collapse:collapse;font-size:13px}caption{text-align:left;font-weight:700;padding:0 0 7px}th,td{border:1px solid var(--line);padding:8px;vertical-align:top;text-align:left}th{background:#f3f6f9}.editing main{outline:2px dashed #c29b3b;outline-offset:5px}.search-hidden{display:none!important}.collapsed .section-content{display:none}.collapsed .section-toggle{border-bottom:0}@media(max-width:800px){.shell{grid-template-columns:1fr}.sidebar{position:static}.sidebar nav{grid-template-columns:repeat(2,minmax(0,1fr))}}@page{size:A4;margin:14mm}@media print{body{background:#fff;font-size:10.5pt}.toolbar,.sidebar{display:none!important}.shell{display:block;max-width:none;margin:0;padding:0}.cover,.report-section{border:0;box-shadow:none;border-radius:0;break-inside:auto}.cover{padding:0 0 8mm}.report-section{margin:0}.section-toggle{padding:5mm 0 2mm}.section-toggle i{display:none}.section-content{display:block!important;padding:2mm 0 5mm}.table-wrap{overflow:visible}a{color:inherit;text-decoration:none}}
</style></head>
<body><div class="toolbar"><button id="editButton" onclick="toggleEdit()">开始编辑</button><button onclick="expandAll()">全部展开</button><button onclick="collapseAll()">全部收起</button><button class="primary" onclick="downloadHtml()">保存并下载HTML</button><button onclick="window.print()">打印或导出PDF</button><button onclick="restore()">撤销全部修改</button></div>
<div class="shell"><aside class="sidebar"><h1>{{NAME}}</h1><div class="sub">{{TITLE}}<br>{{GENERATED_AT}}</div><input id="search" placeholder="搜索能力、论文或岗位" oninput="searchReport(this.value)"><nav>{{NAV}}</nav></aside>
<main data-decision-schema="1" contenteditable="false"><header class="cover"><h2>{{TITLE}}</h2><p>{{SUBTITLE}}</p></header>{{SECTIONS}}</main></div>
<script id="career-data" type="application/json">{{EMBEDDED_DATA}}</script>
<script>
const main=document.querySelector('main'),key='career-decision-v1:'+(document.title+'|'+location.pathname),original=main.innerHTML;try{const draft=localStorage.getItem(key);if(draft)main.innerHTML=draft}catch(e){}let editing=false;function save(){try{localStorage.setItem(key,main.innerHTML)}catch(e){}}main.addEventListener('input',save);function toggleEdit(){editing=!editing;document.body.classList.toggle('editing',editing);main.contentEditable=editing?'true':'false';editButton.textContent=editing?'结束编辑':'开始编辑';save()}function toggleSection(btn){const section=btn.closest('.report-section'),collapsed=section.classList.toggle('collapsed');btn.setAttribute('aria-expanded',String(!collapsed));btn.querySelector('i').textContent=collapsed?'展开':'收起'}function expandAll(){document.querySelectorAll('.report-section').forEach(x=>x.classList.remove('collapsed'))}function collapseAll(){document.querySelectorAll('.report-section').forEach(x=>x.classList.add('collapsed'))}function searchReport(query){const q=query.trim().toLowerCase();document.querySelectorAll('.report-section').forEach(section=>{const hit=!q||section.textContent.toLowerCase().includes(q);section.classList.toggle('search-hidden',!hit);if(hit&&q)section.classList.remove('collapsed')})}function restore(){if(confirm('确定恢复首次生成的内容吗？')){main.innerHTML=original;localStorage.removeItem(key)}}function downloadHtml(){save();const blob=new Blob(['<!doctype html>\n'+document.documentElement.outerHTML],{type:'text/html;charset=utf-8'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=document.title.replace(/[\\/:*?"<>|]/g,'_')+'.html';a.click();URL.revokeObjectURL(a.href)}
</script></body></html>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not data.get("name") or not data.get("sections") or not isinstance(data.get("embedded_data"), dict):
        raise SystemExit("input must contain name, non-empty sections and embedded_data object")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(data), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()

