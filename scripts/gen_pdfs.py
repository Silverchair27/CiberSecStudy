#!/usr/bin/env python3
"""Gera um .pdf ao lado de cada aula (docs/**/NN-*.md) usando Chromium
headless (--print-to-pdf). Requer `pip install markdown` e um binário de
Chromium/Chrome disponível (ajuste CHROME abaixo se o caminho mudar,
ex.: `find /opt/pw-browsers -iname chrome -type f`).

Uso: python3 scripts/gen_pdfs.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path
import markdown

REPO = Path(__file__).resolve().parent.parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
TMP_HTML_DIR = Path(tempfile.mkdtemp(prefix="cibersecstudy-pdf-"))

CSS = """
@page { margin: 20mm 18mm; }
* { box-sizing: border-box; }
body {
  font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
  color: #1a1a1a;
  line-height: 1.55;
  font-size: 12.5px;
  max-width: 780px;
  margin: 0 auto;
}
h1 {
  font-size: 22px;
  border-bottom: 3px solid #2b6cb0;
  padding-bottom: 8px;
  margin-top: 0;
  color: #14304d;
}
h2 {
  font-size: 16px;
  color: #14304d;
  border-bottom: 1px solid #d0d7de;
  padding-bottom: 4px;
  margin-top: 26px;
}
h3 {
  font-size: 13.5px;
  color: #1f4e79;
  margin-top: 18px;
}
p { margin: 8px 0; }
code {
  background: #f2f4f6;
  border: 1px solid #dfe3e8;
  border-radius: 3px;
  padding: 1px 4px;
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: 11px;
}
pre {
  background: #f6f8fa;
  border: 1px solid #dfe3e8;
  border-radius: 5px;
  padding: 10px 12px;
  overflow-x: auto;
  page-break-inside: avoid;
}
pre code {
  background: none;
  border: none;
  padding: 0;
  font-size: 10.5px;
  line-height: 1.45;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 12px 0;
  font-size: 11px;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid #d0d7de;
  padding: 5px 8px;
  text-align: left;
  vertical-align: top;
}
th {
  background: #eef2f7;
  font-weight: 600;
}
blockquote {
  border-left: 3px solid #2b6cb0;
  margin: 10px 0;
  padding: 2px 14px;
  color: #3c3c3c;
  background: #f7f9fb;
}
a { color: #1a56a4; text-decoration: none; }
ul, ol { margin: 6px 0; padding-left: 22px; }
li { margin: 3px 0; }
hr { border: none; border-top: 1px solid #d0d7de; margin: 18px 0; }
.doc-footer {
  margin-top: 28px;
  padding-top: 8px;
  border-top: 1px solid #d0d7de;
  font-size: 9.5px;
  color: #6b7280;
}
"""

md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists"])

lesson_files = sorted(
    p for p in REPO.glob("docs/*/*.md")
    if p.name not in ("README.md", "ROADMAP.md")
    and p.name[0].isdigit()
)

print(f"Encontradas {len(lesson_files)} aulas.")

ok, fail = 0, []
for md_path in lesson_files:
    md.reset()
    text = md_path.read_text(encoding="utf-8")
    body_html = md.convert(text)
    title = md_path.stem
    html_doc = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>{title}</title>
<style>{CSS}</style>
</head><body>
{body_html}
<div class="doc-footer">CiberSecStudy — {md_path.relative_to(REPO)}</div>
</body></html>"""

    tmp_html = TMP_HTML_DIR / (md_path.stem + ".html")
    tmp_html.write_text(html_doc, encoding="utf-8")

    out_pdf = md_path.with_suffix(".pdf")
    cmd = [
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        f"--print-to-pdf={out_pdf}",
        "--print-to-pdf-no-header",
        "--no-pdf-header-footer",
        f"file://{tmp_html}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if out_pdf.exists() and out_pdf.stat().st_size > 500:
        ok += 1
        print(f"OK  {out_pdf.relative_to(REPO)}  ({out_pdf.stat().st_size} bytes)")
    else:
        fail.append(str(md_path))
        print(f"FAIL {md_path}")
        print(result.stderr[-2000:])

print(f"\nConcluído: {ok} ok, {len(fail)} falhas.")
if fail:
    print("Falharam:", fail)
    sys.exit(1)
