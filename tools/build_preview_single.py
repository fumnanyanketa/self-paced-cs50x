#!/usr/bin/env python3
"""Build a SINGLE self-contained preview HTML for the paginated-lesson prototype.

Bundles all pages of one lesson into one file that works offline by double-click:
the pager switches pages with JavaScript instead of navigating between files, and
there are no external asset references (no sync scripts). Google Fonts is the only
remote link; it degrades to system fonts offline.

Usage:
    python3 build_preview_single.py <input.md> <output.html> [course.json] [word_target]
"""
import html
import re
import sys

import markdown
from pygments.formatters import HtmlFormatter

import build_lesson as bl
from build_lesson_paged import (PAGER_CSS, WORD_TARGET, page_label, plan_pages,
                                split_sections)

EXTRA_CSS = r"""
.pv-page{display:none}
.pv-page.on{display:block}
#hero-compact{display:none}
body.compact #hero-full{display:none}
body.compact #hero-compact{display:block}
.toc-block{display:none}.toc-block.on{display:block}
.pager .seg a{cursor:pointer}
.pbtn{cursor:pointer}
.pv-banner{background:#fff4d6;border:1px solid #ecd9a3;color:#6b5514;border-radius:12px;padding:12px 16px;margin:0 0 22px;font-size:14px;font-weight:600}
"""


def render_page(page_md):
    md = markdown.Markdown(
        extensions=["fenced_code", "tables", "toc", "sane_lists", "attr_list", "codehilite"],
        extension_configs={"codehilite": {"guess_lang": False, "css_class": "codehilite"},
                           "toc": {"toc_depth": "2-3"}},
    )
    body = md.convert(page_md)
    toc = md.toc
    body = re.sub(r'<h2 id="[^"]*"(>\s*(?:\U0001F6E0️?\s*)?Capstone)',
                  r'<h2 id="capstone" class="capstone-h"\1', body)
    toc = re.sub(r'<a href="#[^"]*"(>\s*(?:\U0001F6E0️?\s*)?Capstone)',
                 r'<a href="#capstone" class="toc-capstone"\1', toc)
    return body, toc


def main(md_path, out_path, cfg, word_target):
    import pathlib
    raw = pathlib.Path(md_path).read_text(encoding="utf-8")
    m = re.match(r"#\s+(.+)\n", raw)
    title_full = m.group(1).strip() if m else "Lesson"
    body_src = raw[m.end():] if m else raw

    meta_block = ""
    bm = re.match(r"\s*((?:^>.*\n?)+)", body_src, re.M)
    if bm:
        meta_block = bm.group(1)
        body_src = body_src[bm.end():]

    def field(label):
        mm = re.search(r"\*\*" + label + r":?\*\*\s*(.+)", meta_block)
        return mm.group(1).strip() if mm else ""

    speaker = field("Speaker").split(",")[0].strip() or "Instructor"
    time_short = re.sub(r"\s*\(.*\)", "", field("Estimated time")).strip() or "45 to 60 min"
    yt = re.search(r"\((https?://[^)]*(?:youtube\.com|youtu\.be)[^)]*)\)", meta_block)
    yt_url = yt.group(1) if yt else ""

    if ": " in title_full:
        eyebrow, hero_title = title_full.split(": ", 1)
    else:
        eyebrow, hero_title = "Lesson", title_full
    bits = hero_title.rsplit(" ", 1)
    hero_title_html = (html.escape(bits[0]) + ' <span class="accent">' + html.escape(bits[1]) + "</span>") \
        if len(bits) == 2 else html.escape(hero_title)

    lead = ""
    lm = re.search(r"##\s+In one sentence\s*\n+([^\n#]+(?:\n[^\n#]+)*)", body_src)
    if lm:
        lead = re.sub(r"\s+", " ", lm.group(1)).strip()
        lead = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", lead)
        lead = re.sub(r"\*\*(.+?)\*\*", r"\1", lead)
        lead = re.sub(r"`([^`]+)`", r"\1", lead)

    # global word target used by plan_pages
    import build_lesson_paged as blp
    blp.WORD_TARGET = word_target

    sections = split_sections(body_src)
    pages = plan_pages(sections)
    n = len(pages)
    labels = [page_label(p) for p in pages]

    rendered = [render_page("\n".join(c for _, c in pg)) for pg in pages]

    # ---- assemble ----
    template = bl.TEMPLATE.replace("</style>\n</head>", PAGER_CSS + EXTRA_CSS + "</style>\n</head>")

    def pager(i, where):
        seg = '<div class="seg">' + "".join(
            f'<a data-go="{j}" class="{"cur" if j == i else ""}" title="{html.escape(labels[j-1])}">{j}</a>'
            for j in range(1, n + 1)) + '</div>'
        count = f'<span class="pcount">Page {i} of {n} &middot; {html.escape(labels[i-1])}</span>'
        prev_c = "disabled" if i == 1 else ""
        next_c = "disabled" if i == n else ""
        btns = (f'<div class="pbtns">'
                f'<a class="pbtn prev {prev_c}" data-go="{i-1}">&#8592; Prev</a>'
                f'<a class="pbtn next {next_c}" data-go="{i+1}">Next &#8594;</a></div>')
        return f'<div class="pager {where}">{count}{seg}{btns}</div>'

    banner = ('<div class="pv-banner">&#128064; Preview of the multi-page-lesson prototype '
              '&mdash; use the pager (Prev / Next / numbers) to switch pages. Nothing here is '
              'live yet; this is a standalone demo file.</div>')

    pages_html = ""
    for i, (body_html, _toc) in enumerate(rendered, 1):
        inner = pager(i, "top") + body_html + pager(i, "bottom")
        if i == 1:
            inner = banner + inner
        pages_html += f'<div class="pv-page{" on" if i == 1 else ""}" data-page="{i}">{inner}</div>'

    toc_blocks = ""
    for i, (_b, toc) in enumerate(rendered, 1):
        toc_blocks += f'<div class="toc-block{" on" if i == 1 else ""}" data-toc="{i}">{toc}</div>'

    compact_header = (
        '<header class="lp-head" id="hero-compact"><div class="wrap">'
        f'<span class="eyebrow">&#10022; {html.escape(eyebrow)}</span>'
        f'<h1>{hero_title_html}</h1>'
        f'<p class="part" id="compact-part"></p>'
        '</div></header>'
    )

    pyg_css = HtmlFormatter(style="one-dark").get_style_defs(".codehilite")
    watch = (f'<a class="play" href="{html.escape(yt_url)}" target="_blank" rel="noopener">'
             f'<span class="circ">&#9654;</span> Watch the talk</a>') if yt_url else ""

    out = template
    # tag the big hero so we can hide it on later pages, and add compact header after it
    out = out.replace('<header class="hero">', '<header class="hero" id="hero-full">')
    out = out.replace('</header>\n\n<div class="layout">', '</header>\n' + compact_header + '\n<div class="layout">')
    # replace the single {{TOC}} card body with our toggling blocks
    out = out.replace("{{TOC}}", toc_blocks)
    # replace the single {{BODY}} with all page divs
    out = out.replace("{{BODY}}", pages_html)

    nav = ('<nav class="lessonnav">'
           '<a class="ln home" href="#" onclick="return false"><b>All lessons (demo)</b></a>'
           '</nav>')

    # per-page labels for JS
    labels_js = "[" + ",".join('"' + l.replace('"', '\\"') + '"' for l in labels) + "]"
    switch_js = f"""
<script>
(function(){{
  var N={n}, labels={labels_js};
  function show(i){{
    if(i<1||i>N) return;
    document.querySelectorAll('.pv-page').forEach(function(p){{p.classList.toggle('on', +p.dataset.page===i);}});
    document.querySelectorAll('.toc-block').forEach(function(t){{t.classList.toggle('on', +t.dataset.toc===i);}});
    document.body.classList.toggle('compact', i>1);
    var cp=document.getElementById('compact-part');
    if(cp) cp.textContent='Part '+i+' of '+N+' · '+labels[i-1];
    window.scrollTo(0,0);
  }}
  document.addEventListener('click',function(e){{
    var t=e.target.closest('[data-go]'); if(!t) return;
    if(t.classList.contains('disabled')) return;
    e.preventDefault(); show(parseInt(t.dataset.go,10));
  }});
}})();
</script>
"""
    out = out.replace("</body>", switch_js + "</body>")

    out = (out
           .replace("{{TITLE}}", html.escape(title_full) + " (preview)")
           .replace("{{COURSE}}", html.escape(cfg.get("title", bl.DEFAULT_CFG["title"])))
           .replace("{{SOURCE_LABEL}}", html.escape(cfg.get("source_label", bl.DEFAULT_CFG["source_label"])))
           .replace("{{FOOTER_NOTE}}", html.escape(cfg.get("footer_note", bl.DEFAULT_CFG["footer_note"])))
           .replace("{{EYEBROW}}", html.escape(eyebrow))
           .replace("{{HERO_TITLE}}", hero_title_html)
           .replace("{{LEAD}}", html.escape(lead))
           .replace("{{SPEAKER}}", html.escape(speaker))
           .replace("{{TIME}}", html.escape(time_short))
           .replace("{{WATCH}}", watch)
           .replace("{{HOME}}", "#")
           .replace("{{NAV}}", nav)
           .replace("{{PYGMENTS_CSS}}", pyg_css))

    pathlib.Path(out_path).write_text(out, encoding="utf-8")
    print(f"wrote {out_path} ({len(out)//1024} KB, {n} pages)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: build_preview_single.py <input.md> <output.html> [course.json] [word_target]")
    wt = int(sys.argv[4]) if len(sys.argv) > 4 else WORD_TARGET
    cfg = bl.load_cfg(sys.argv[3] if len(sys.argv) > 3 else None)
    main(sys.argv[1], sys.argv[2], cfg, wt)
