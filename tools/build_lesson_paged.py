#!/usr/bin/env python3
"""PROTOTYPE: render one lesson (Markdown) as several short, linked pages.

Splits a lesson's content across multiple HTML pages at H2 (`## `) section
boundaries, targeting roughly `WORD_TARGET` words per page, and always starting
a fresh page at the Capstone. Content is NOT changed — only sliced. Each page
reuses the exact same template/CSS as build_lesson.py, plus an in-lesson pager
(prev / next + segment pills). The "mark complete" sync hook is placed on the
LAST page only, so one lesson still equals one tracked unit.

Usage:
    python3 build_lesson_paged.py <input.md> <out_dir> [course.json] [word_target]

Writes <out_dir>/1.html .. <out_dir>/N.html
"""
import html
import json
import pathlib
import re
import sys

import markdown
from pygments.formatters import HtmlFormatter

import build_lesson as bl

WORD_TARGET = 1900  # aim per page; sections are never split mid-way


# ---- pager CSS injected into the template's first <style> block -------------
PAGER_CSS = r"""
/* ---- in-lesson pager (prototype) ---- */
.lp-head{background:radial-gradient(120% 120% at 85% 0%,var(--navy-3),var(--navy) 62%);color:#eaf1f8;position:relative;overflow:hidden}
.lp-head::before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.12) 1.3px,transparent 1.3px);background-size:22px 22px;opacity:.22;mask:radial-gradient(60% 60% at 20% 30%,#000,transparent)}
.lp-head .wrap{position:relative;z-index:2;padding:34px 28px 30px}
.lp-head .eyebrow{margin-bottom:12px}
.lp-head h1{font-family:Poppins;font-weight:800;font-size:30px;line-height:1.12;margin:0;color:#fff}
.lp-head .part{color:#b9c6d6;font-size:15px;margin:10px 0 0}
.pager{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:0 0 30px;padding:14px 16px;background:var(--soft);border:1px solid var(--line);border-radius:14px}
.pager .seg{display:flex;gap:7px;flex-wrap:wrap;flex:1;min-width:160px}
.pager .seg a{width:26px;height:26px;border-radius:8px;display:grid;place-items:center;font-size:12.5px;font-weight:700;font-family:Poppins;color:var(--muted);background:#fff;border:1px solid var(--line);transition:.15s}
.pager .seg a:hover{border-color:var(--teal);color:var(--teal-d)}
.pager .seg a.cur{background:var(--teal);border-color:var(--teal);color:#04231c}
.pager .pcount{font-size:13.5px;color:var(--muted);font-weight:600;white-space:nowrap}
.pager .pbtns{display:flex;gap:9px;margin-left:auto}
.pbtn{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:999px;padding:9px 16px;font-weight:600;font-size:14px;transition:.15s;cursor:pointer}
.pbtn:hover{border-color:var(--teal);color:var(--teal-d);transform:translateY(-1px)}
.pbtn.disabled{opacity:.4;pointer-events:none}
.pbtn.next{background:var(--teal);border-color:var(--teal);color:#04231c}
.pbtn.next:hover{background:var(--teal-d);color:#fff}
.pager.bottom{margin:44px 0 0}
@media(max-width:920px){.lp-head .wrap{padding:26px 20px 24px}.lp-head h1{font-size:24px}.pager .pbtns{margin-left:0;width:100%}.pbtn{flex:1;justify-content:center}}
"""


def split_sections(body_src):
    """Split markdown (after the meta block) into (heading_text, chunk) sections
    at H2 boundaries. Any preamble before the first H2 is attached to nothing
    (there is none in these lessons)."""
    parts = re.split(r"(?m)^(?=## )", body_src)
    out = []
    for p in parts:
        if not p.strip():
            continue
        hm = re.match(r"##\s+(.+)", p)
        heading = hm.group(1).strip() if hm else ""
        out.append((heading, p))
    return out


def wc(text):
    return len(re.findall(r"\w+", re.sub(r"```.*?```", "", text, flags=re.S)))


def plan_pages(sections):
    """Greedy pack sections into pages by word target; force a new page at the
    Capstone so the hands-on project always starts a page."""
    pages, cur, cur_w = [], [], 0
    for heading, chunk in sections:
        is_capstone = "capstone" in heading.lower()
        w = wc(chunk)
        if cur and (is_capstone or cur_w + w > WORD_TARGET):
            pages.append(cur)
            cur, cur_w = [], 0
        cur.append((heading, chunk))
        cur_w += w
    if cur:
        pages.append(cur)
    return pages


def page_label(sections):
    """Short human label for a page from its sections."""
    heads = [h for h, _ in sections]
    if any("In one sentence" in h for h in heads):
        return "Start here"
    if any("capstone" in h.lower() for h in heads):
        return "Capstone & wrap-up"
    nums = [int(pm.group(1)) for h in heads for pm in [re.match(r"Part\s+(\d+)", h)] if pm]
    if nums:
        return f"Part {nums[0]}" if len(nums) == 1 else f"Parts {nums[0]}–{nums[-1]}"
    if any("Key takeaways" in h for h in heads):
        return "Wrap-up"
    return heads[0][:22] if heads else ""


def build(md_path, out_dir, cfg, home="../../lessons-html/index.html"):
    raw = pathlib.Path(md_path).read_text(encoding="utf-8")
    m = re.match(r"#\s+(.+)\n", raw)
    title_full = m.group(1).strip() if m else "Lesson"
    body_src = raw[m.end():] if m else raw

    # peel meta block (hero fields) exactly like build_lesson
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

    sections = split_sections(body_src)
    pages = plan_pages(sections)
    n = len(pages)
    labels = [page_label(p) for p in pages]

    lesson_num = ""
    lm2 = re.search(r"Lesson\s+(\d+)", title_full)
    if lm2:
        lesson_num = lm2.group(1)

    pyg_css = HtmlFormatter(style="one-dark").get_style_defs(".codehilite")
    watch = ""
    if yt_url:
        watch = (f'<a class="play" href="{html.escape(yt_url)}" target="_blank" rel="noopener">'
                 f'<span class="circ">&#9654;</span> Watch the talk</a>')

    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, page in enumerate(pages, 1):
        page_md = "\n".join(chunk for _, chunk in page)
        md = markdown.Markdown(
            extensions=["fenced_code", "tables", "toc", "sane_lists", "attr_list", "codehilite"],
            extension_configs={"codehilite": {"guess_lang": False, "css_class": "codehilite"},
                               "toc": {"toc_depth": "2-3"}},
        )
        body_html = md.convert(page_md)
        toc_html = md.toc
        body_html = re.sub(r'<h2 id="[^"]*"(>\s*(?:\U0001F6E0️?\s*)?Capstone)',
                           r'<h2 id="capstone" class="capstone-h"\1', body_html)
        toc_html = re.sub(r'<a href="#[^"]*"(>\s*(?:\U0001F6E0️?\s*)?Capstone)',
                          r'<a href="#capstone" class="toc-capstone"\1', toc_html)

        # ---- pager markup ----
        def pager(where):
            seg = '<div class="seg">' + "".join(
                f'<a href="{j}.html" class="{"cur" if j == i else ""}" title="{html.escape(labels[j-1])}">{j}</a>'
                for j in range(1, n + 1)) + '</div>'
            count = f'<span class="pcount">Page {i} of {n} &middot; {html.escape(labels[i-1])}</span>'
            prev_c = "disabled" if i == 1 else ""
            next_c = "disabled" if i == n else ""
            prev_h = "#" if i == 1 else f"{i-1}.html"
            next_h = "#" if i == n else f"{i+1}.html"
            btns = (f'<div class="pbtns">'
                    f'<a class="pbtn prev {prev_c}" href="{prev_h}">&#8592; Prev</a>'
                    f'<a class="pbtn next {next_c}" href="{next_h}">Next &#8594;</a></div>')
            return f'<div class="pager {where}">{count}{seg}{btns}</div>'

        # ---- header: full hero on page 1, compact strip on later pages ----
        template = bl.TEMPLATE.replace("</style>\n</head>", PAGER_CSS + "</style>\n</head>")
        if i == 1:
            out = template
        else:
            compact = (
                '<header class="lp-head"><div class="wrap">'
                f'<span class="eyebrow">&#10022; {html.escape(eyebrow)}</span>'
                f'<h1>{hero_title_html}</h1>'
                f'<p class="part">Part {i} of {n} &middot; {html.escape(labels[i-1])}</p>'
                '</div></header>'
            )
            out = re.sub(r'<header class="hero">.*?</header>', compact, template, flags=re.S)

        # nav: only page 1 shows prev-lesson, only last page shows next-lesson;
        # here (prototype) just a home link.
        nav = ('<nav class="lessonnav">'
               f'<a class="ln home" href="{html.escape(home)}"><b>All lessons</b></a>'
               '</nav>')

        body_with_pager = pager("top") + body_html + pager("bottom")

        out = (out
               .replace("{{TITLE}}", html.escape(title_full) + f" (p{i}/{n})")
               .replace("{{COURSE}}", html.escape(cfg.get("title", bl.DEFAULT_CFG["title"])))
               .replace("{{SOURCE_LABEL}}", html.escape(cfg.get("source_label", bl.DEFAULT_CFG["source_label"])))
               .replace("{{FOOTER_NOTE}}", html.escape(cfg.get("footer_note", bl.DEFAULT_CFG["footer_note"])))
               .replace("{{EYEBROW}}", html.escape(eyebrow))
               .replace("{{HERO_TITLE}}", hero_title_html)
               .replace("{{LEAD}}", html.escape(lead))
               .replace("{{SPEAKER}}", html.escape(speaker))
               .replace("{{TIME}}", html.escape(time_short))
               .replace("{{WATCH}}", watch)
               .replace("{{HOME}}", html.escape(home))
               .replace("{{NAV}}", nav)
               .replace("{{TOC}}", toc_html)
               .replace("{{BODY}}", body_with_pager)
               .replace("{{PYGMENTS_CSS}}", pyg_css))

        # sync "mark complete" only on the LAST page
        if cfg.get("sync") and i == n and lesson_num:
            block = (
                f'<section class="lesson-sync" data-lesson-id="{lesson_num}" data-home="{home}">'
                '<div class="ls-inner">'
                '<button type="button" class="ls-btn" data-lesson-complete>Mark this lesson complete</button>'
                '<span class="ls-status" data-sync-status></span></div>'
                f'<a class="ls-track" href="{home}">Your progress &#8594;</a></section>')
            base = "../../lessons-html"
            script = (f'<script src="{base}/assets/course-data.js"></script>'
                      f'<script type="module" src="{base}/assets/sync.js"></script>')
            out = out.replace('<nav class="lessonnav">', block + '<nav class="lessonnav">', 1)
            out = out.replace("</body>", script + "</body>", 1)

        (out_dir / f"{i}.html").write_text(out, encoding="utf-8")
        print(f"  page {i}/{n} [{labels[i-1]}] -> {out_dir / f'{i}.html'} ({wc(page_md)} words)")

    print(f"done: {n} pages, target {WORD_TARGET} words/page")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: build_lesson_paged.py <input.md> <out_dir> [course.json] [word_target]")
    if len(sys.argv) > 4:
        WORD_TARGET = int(sys.argv[4])
    cfg = bl.load_cfg(sys.argv[3] if len(sys.argv) > 3 else None)
    build(sys.argv[1], sys.argv[2], cfg)
