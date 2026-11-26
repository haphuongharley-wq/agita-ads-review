"""Build index.html from the ad copy markdown in the Agita repo."""
import pathlib
import re

import markdown

SRC = pathlib.Path.home() / "agita-project/copy/ads-jan-2027/ad-copy.md"
md = SRC.read_text()

imgs = {"P1": "p1-for-etter", "P2": "p2-polaroid"}
for key, stem in imgs.items():
    gallery = "".join(
        f'<a href="images/{stem}-{fmt}.jpg" target="_blank"><img class="ad" src="images/{stem}-{fmt}.jpg" alt="{key} {fmt}"></a>'
        for fmt in ("feed", "story"))
    md = re.sub(rf"(## {key}:[^\n]*\n)", rf'\1\n<div class="gallery">{gallery}</div>\n\n', md)

body = markdown.markdown(md, extensions=["tables"])
sections = [("v1", "V1"), ("v2", "V2"), ("v3", "V3"), ("p1", "P1"), ("p2", "P2")]
for anchor, key in sections:
    body = body.replace(f"<h2>{key}:", f'<h2 id="{anchor}">{key}:', 1)
nav = "".join(f'<a href="#{a}">{k}</a>' for a, k in sections)

page = f"""<!DOCTYPE html><html lang="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AB5 annonser januar</title>
<style>
:root{{--bg:#F7F3EA;--ink:#2C3550;--muted:#5A5F6E;--accent:#C8664A;--card:#FFFFFF;color-scheme:light}}
*{{box-sizing:border-box}}
body{{margin:0;overflow-wrap:anywhere;background:var(--bg);color:var(--ink);font:17px/1.6 -apple-system,'Helvetica Neue',Arial,sans-serif}}
header{{background:var(--ink);color:#fff;padding:40px 16px 28px}}
.wrap{{max-width:780px;margin:0 auto}}
header h1{{font-family:Georgia,serif;font-size:34px;margin:0 0 8px}}
header p{{margin:0;color:#D5D9E4}}
nav{{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}}
nav a{{color:#fff;text-decoration:none;border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:6px 14px;font-size:14px}}
main{{padding:24px 16px 64px}}
h1,h2,h3{{font-family:Georgia,serif;line-height:1.25}}
main h1{{display:none}}
h2{{font-size:28px;margin-top:56px;padding-top:12px;border-top:3px solid var(--accent)}}
h3{{font-size:20px;margin-top:32px}}
blockquote{{margin:0 0 12px;padding:12px 18px;background:var(--card);border-left:4px solid var(--accent);border-radius:6px}}
.gallery{{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap}}
.gallery a{{flex:1 1 220px;max-width:360px}}
img.ad{{width:100%;display:block;border-radius:10px;box-shadow:0 6px 24px rgba(44,53,80,.18);margin:8px 0 16px}}
table{{border-collapse:collapse;width:100%;font-size:15px;display:block;overflow-x:auto}}
td,th{{border:1px solid #DDD5C4;padding:8px 10px;text-align:left;vertical-align:top}}
code{{background:#ECE5D6;padding:1px 5px;border-radius:4px;font-size:14px;word-break:break-all}}
hr{{display:none}}
</style></head><body>
<header><div class="wrap"><h1>Annonser, januar 2027</h1>
<p>AB5 Kunstskole. Tre videoannonser og to bildeannonser som sender folk til gratisvideoen, til godkjenning.</p>
<nav>{nav}</nav></div></header>
<main><div class="wrap">{body}</div></main></body></html>"""
pathlib.Path(__file__).with_name("index.html").write_text(page)
print("ok")
