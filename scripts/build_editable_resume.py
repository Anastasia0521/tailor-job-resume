#!/usr/bin/env python3
import argparse
import base64
import html
import json
import mimetypes
from pathlib import Path

def esc(value):
    return html.escape(str(value or ""))

def photo_uri(path):
    if not path:
        return ""
    p = Path(path)
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"

def render(data, photo):
    contacts = "　｜　".join(esc(x) for x in data.get("contact", []))
    sections = []
    for section in data.get("sections", []):
        items = []
        for item in section.get("items", []):
            meta = f'<span class="meta">{esc(item.get("meta"))}</span>' if item.get("meta") else ""
            items.append(f'<article><h3>{esc(item.get("heading"))}{meta}</h3><p>{esc(item.get("body"))}</p></article>')
        sections.append(f'<section><h2>{esc(section.get("title"))}</h2>{"".join(items)}</section>')
    photo_html = f'<img id="photo" src="{photo}" alt="证件照">' if photo else ""
    return TEMPLATE.replace("{{NAME}}", esc(data.get("name"))).replace("{{TARGET}}", esc(data.get("target"))).replace("{{CONTACT}}", contacts).replace("{{SUMMARY}}", esc(data.get("summary"))).replace("{{SECTIONS}}", "".join(sections)).replace("{{PHOTO}}", photo_html)

TEMPLATE = r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{{NAME}}｜针对性简历</title><style>
*{box-sizing:border-box}body{margin:0;background:#e9e9e9;color:#111;font:10.7pt/1.5 "Times New Roman","Songti SC",SimSun,serif}.page{width:210mm;min-height:297mm;margin:12mm auto;padding:14mm;background:#fff;box-shadow:0 2px 12px #aaa;position:relative}.head{min-height:45mm;padding-right:40mm;position:relative}h1{font-size:23pt;margin:0 0 4mm}h2{font-size:15pt;font-weight:normal;border-bottom:1px solid;margin:4mm 0 2mm}h3{font-size:11pt;margin:2mm 0 1mm}.meta{float:right;font-weight:normal;font-style:italic}p{margin:0 0 2mm;text-align:justify}#photo{position:absolute;right:0;top:0;width:31mm;height:43mm;object-fit:cover;object-position:center 27%}.bar{position:fixed;right:16px;top:16px;z-index:9;display:flex;gap:6px;flex-wrap:wrap;max-width:480px;justify-content:flex-end}.bar button{border:0;border-radius:5px;padding:9px 12px;background:#222;color:#fff;cursor:pointer}.bar .save{background:#176b42}.tip{position:fixed;left:16px;top:16px;z-index:9;background:#fff8d9;padding:9px 12px;border-radius:5px}.panel{position:fixed;right:16px;top:68px;z-index:10;background:#fff;padding:14px;width:290px;box-shadow:0 3px 16px #999}.panel[hidden]{display:none}.control{display:grid;grid-template-columns:68px 1fr 48px;gap:7px;margin:8px 0}.control input{width:100%}.editing .page{outline:2px dashed #b89a37;outline-offset:-5px}@page{size:A4;margin:0}@media print{body{background:#fff}.bar,.tip,.panel{display:none!important}.page{margin:0;box-shadow:none;outline:none}}
</style></head><body class="editing"><div class="tip">点击简历文字即可修改，内容会自动暂存。</div><div class="bar"><button id="mode" onclick="toggleEdit()">切换为预览</button><button onclick="togglePanel()">调整照片</button><button class="save" onclick="downloadHtml()">保存并下载 HTML</button><button onclick="print()">打印 / 导出 PDF</button><button onclick="restore()">撤销全部修改</button></div><aside class="panel" id="panel" hidden contenteditable="false"><b>照片大小与位置</b><label class="control">宽度<input id="pw" type="range" min="22" max="45" value="31"><output>31mm</output></label><label class="control">高度<input id="ph" type="range" min="30" max="58" value="43"><output>43mm</output></label><label class="control">左右<input id="pr" type="range" min="-8" max="35" value="0"><output>0mm</output></label><label class="control">上下<input id="pt" type="range" min="-8" max="25" value="0"><output>0mm</output></label><label class="control">裁切<input id="pc" type="range" min="0" max="100" value="27"><output>27%</output></label></aside><main class="page" contenteditable="true"><header class="head"><h1>{{NAME}}</h1><p><b>应聘岗位：</b>{{TARGET}}</p><p>{{CONTACT}}</p>{{PHOTO}}</header><section><h2>个人概述</h2><p>{{SUMMARY}}</p></section>{{SECTIONS}}</main><script>
const key='tailor-job-resume-draft-v1',page=document.querySelector('.page'),original=page.innerHTML,photo=document.querySelector('#photo'),panel=document.querySelector('#panel');try{const x=localStorage.getItem(key);if(x)page.innerHTML=x}catch(e){}function save(){localStorage.setItem(key,page.innerHTML)}page.addEventListener('input',save);function toggleEdit(){const on=!document.body.classList.contains('editing');document.body.classList.toggle('editing',on);page.contentEditable=on?'true':'false';document.querySelector('#mode').textContent=on?'切换为预览':'继续编辑';if(!on)panel.hidden=true;save()}function restore(){if(confirm('确定恢复初始版本吗？')){page.innerHTML=original;localStorage.removeItem(key)}}function togglePanel(){if(!photo)return;panel.hidden=!panel.hidden}function apply(){if(!photo)return;photo.style.width=pw.value+'mm';photo.style.height=ph.value+'mm';photo.style.right=pr.value+'mm';photo.style.top=pt.value+'mm';photo.style.objectPosition='center '+pc.value+'%';[pw,ph,pr,pt].forEach(x=>x.nextElementSibling.textContent=x.value+'mm');pc.nextElementSibling.textContent=pc.value+'%';save()}['pw','ph','pr','pt','pc'].forEach(id=>document.getElementById(id).addEventListener('input',apply));function downloadHtml(){save();const blob=new Blob(['<!doctype html>\n'+document.documentElement.outerHTML],{type:'text/html;charset=utf-8'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=(document.querySelector('h1').textContent||'简历')+'_可编辑简历.html';a.click();URL.revokeObjectURL(a.href)}
</script></body></html>'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--photo")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    Path(args.output).write_text(render(data, photo_uri(args.photo)), encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()

