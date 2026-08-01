#!/usr/bin/env python3
"""Render one course lesson (Markdown) into a polished, LMS-style HTML page.

This is the generic, config-driven version of the lesson renderer. All branding
(course title, source label, footer note) comes from a `course.json` at the
course root, so the same template renders any course.

Usage (normally called by build_course.py, but works standalone):
    python3 build_lesson.py <input.md> <output.html> [course.json]

Visual style: friendly modern learning-platform look. Dark navy hero with teal
and coral accents, rounded floating cards, sparkle and squiggle motifs, a clean
white content area. Interactive: sticky TOC + scrollspy, reading-progress bar,
copy buttons on code, emoji-driven callouts, check-off for objectives/milestones.
One template renders every lesson consistently.

Requires: `markdown` and `pygments` (pip install markdown pygments).
"""
import html
import json
import pathlib
import re
import sys

import markdown
from pygments.formatters import HtmlFormatter

LEAD_HEADING = "In one sentence"  # overridden per course by cfg["lead_heading"]
ITEM_LABEL = "Lesson"             # overridden per course by cfg["unit_labels"]["item"]

HERO_CARD_HTML = """    <div style="position:relative">
      <div class="hero-card">
        <div class="ring">
          <svg width="74" height="74"><circle cx="37" cy="37" r="31" stroke="#eef2f5" stroke-width="7" fill="none"/><circle cx="37" cy="37" r="31" stroke="#18c4a0" stroke-width="7" fill="none" stroke-linecap="round" stroke-dasharray="195" stroke-dashoffset="40"/></svg>
          <span class="lab">&#10022;</span>
        </div>
        <h3>What you&#39;ll get</h3>
        <ul>
          <li><span class="ic">&#9989;</span><span>Plain-language teaching with every term defined</span></li>
          <li><span class="ic">&#128221;</span><span>Code snippets pulled from the talk</span></li>
          <li><span class="ic">&#128296;</span><span>A hands-on capstone you build step by step</span></li>
          <li><span class="ic">&#127919;</span><span>Optional practice drills to reinforce each skill</span></li>
        </ul>
        <a class="btn btn-coral" href="{{CAPSTONE_HREF}}" style="width:100%;justify-content:center">Jump to the project</a>
      </div>
    </div>"""


def icon_links(prefix):
    """Favicon and home-screen icon tags, resolved against the site root.

    `prefix` is the relative path from the page to lessons-html/ ("." for the
    index, ".." for a lesson page), so one helper serves both depths. The course
    supplies the files in its own assets/ directory; build_course.py copies them
    and sets cfg["_icons"] only when assets/favicon.svg is actually present.

    Four tags rather than one because no single format covers everything: SVG is
    the crisp modern default, the 32px PNG is what browsers that ignore SVG take,
    apple-touch-icon is what iOS uses when a page is added to the home screen,
    and the .ico is the last-resort fallback some tools still probe for at /.
    """
    p = (prefix or ".").rstrip("/")
    return (
        f'<link rel="icon" href="{p}/assets/favicon.svg" type="image/svg+xml">\n'
        f'<link rel="icon" href="{p}/assets/favicon-32.png" sizes="32x32" type="image/png">\n'
        f'<link rel="apple-touch-icon" href="{p}/assets/apple-touch-icon.png">\n'
        f'<link rel="shortcut icon" href="{p}/assets/favicon.ico">'
    )


TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}} | {{COURSE}}</title>
{{ICONS}}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --navy:#0a1a2f; --navy-2:#0f243d; --navy-3:#15314f;
  --teal:#18c4a0; --teal-d:#0fa385; --teal-soft:#e4f8f2;
  --coral:#f24d63; --coral-d:#d83a50; --coral-soft:#feecee;
  --ink:#152230; --muted:#5f6c7b; --line:#e9eef2; --bg:#ffffff;
  --soft:#f4fbf9; --card:#ffffff; --code-bg:#21252b; --max:780px;
  --k:#2f8fb3; --k-bg:#e8f4f9; --tip:#c4881f; --tip-bg:#fdf4e3; --ok:#1f9d6b; --ok-bg:#e6f6ef;
  --no:#e0533f; --no-bg:#fdecea; --goal:#7b54c9; --goal-bg:#f1ebfb;
  --shadow:0 10px 30px rgba(13,30,52,.08); --shadow-sm:0 4px 14px rgba(13,30,52,.07);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.72;font-size:17px;-webkit-font-smoothing:antialiased;overflow-x:hidden}
#progress{position:fixed;top:0;left:0;height:4px;width:0;background:linear-gradient(90deg,var(--teal),var(--coral));z-index:200;transition:width .1s linear}
a{color:var(--teal-d);text-decoration:none}
a:hover{color:var(--coral)}
h1,h2,h3{font-family:Poppins,sans-serif;color:var(--ink);letter-spacing:-.01em}
.accent{color:var(--coral)}
.wrap{max-width:1200px;margin:0 auto;padding:0 28px}

/* ---------- Top welcome strip ---------- */
.topbar{background:var(--navy);color:#cdd8e4;font-size:13.5px}
.topbar .wrap{display:flex;justify-content:space-between;align-items:center;height:42px;gap:18px}
.topbar b{color:#fff;font-weight:600}
.topbar .right{display:flex;gap:18px;align-items:center}
.topbar a{color:#cdd8e4}.topbar a:hover{color:var(--teal)}

/* ---------- Nav ---------- */
nav.bar{background:var(--navy-2);position:sticky;top:0;z-index:120;box-shadow:0 2px 20px rgba(0,0,0,.25)}
nav.bar .wrap{display:flex;align-items:center;height:68px;gap:26px}
.logo{font-family:Poppins;font-weight:800;font-size:22px;color:#fff;letter-spacing:.02em;cursor:pointer;text-decoration:none}
a.logo:hover{color:var(--teal)}
.lessonnav{display:flex;gap:14px;align-items:stretch;margin:60px 0 0;flex-wrap:wrap}
.lessonnav .ln{flex:1;min-width:200px;display:flex;flex-direction:column;gap:3px;border:1px solid var(--line);border-radius:14px;padding:16px 18px;color:var(--muted);transition:.15s;background:#fff}
.lessonnav .ln:hover{border-color:var(--teal);box-shadow:var(--shadow-sm);transform:translateY(-1px)}
.lessonnav .ln .dir{font-size:13px;font-weight:600;color:var(--teal-d)}
.lessonnav .ln b{color:var(--ink);font-family:Poppins;font-size:15px}
.lessonnav .ln.next{text-align:right}
.lessonnav .ln.home{flex:0 0 auto;justify-content:center;align-items:center;text-align:center;background:var(--soft)}
.lessonnav .ln.home b{color:var(--teal-d)}
.logo .dot{color:var(--teal)}

/* in-lesson pager + compact header (multi-page lessons) */
.lp-head{background:radial-gradient(120% 120% at 85% 0%,var(--navy-3),var(--navy) 62%);color:#eaf1f8;position:relative;overflow:hidden}
.lp-head::before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.12) 1.3px,transparent 1.3px);background-size:22px 22px;opacity:.22;mask:radial-gradient(60% 60% at 20% 30%,#000,transparent)}
.lp-head .wrap{position:relative;z-index:2;padding:34px 28px 30px}
.lp-head .eyebrow{margin-bottom:12px}
.lp-head h1{font-family:Poppins;font-weight:800;font-size:30px;line-height:1.12;margin:0;color:#fff}
.lp-head .part{color:#b9c6d6;font-size:15px;margin:10px 0 0}
.pager{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:0 0 30px;padding:14px 16px;background:var(--soft);border:1px solid var(--line);border-radius:14px}
.pager .seg{display:flex;gap:7px;flex-wrap:wrap;flex:1;min-width:150px}
.pager .seg a{width:26px;height:26px;border-radius:8px;display:grid;place-items:center;font-size:12.5px;font-weight:700;font-family:Poppins;color:var(--muted);background:#fff;border:1px solid var(--line);transition:.15s}
.pager .seg a:hover{border-color:var(--teal);color:var(--teal-d)}
.pager .seg a.cur{background:var(--teal);border-color:var(--teal);color:#04231c}
.pager .pcount{font-size:13.5px;color:var(--muted);font-weight:600;white-space:nowrap}
.pager .pbtns{display:flex;gap:9px;margin-left:auto}
.pbtn{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:999px;padding:9px 16px;font-weight:600;font-size:14px;transition:.15s;text-decoration:none}
.pbtn:hover{border-color:var(--teal);color:var(--teal-d);transform:translateY(-1px)}
.pbtn.disabled{opacity:.4;pointer-events:none}
.pbtn.next{background:var(--teal);border-color:var(--teal);color:#04231c}
.pbtn.next:hover{background:var(--teal-d);color:#fff}
.pager.bottom{margin:44px 0 0}
@media(max-width:920px){.lp-head .wrap{padding:26px 20px 24px}.lp-head h1{font-size:24px}.pager .pbtns{margin-left:0;width:100%}.pbtn{flex:1;justify-content:center}}

.navlinks{display:flex;gap:24px;margin-left:8px}
.navlinks a{color:#dde6ef;font-weight:500;font-size:15px}
.navlinks a:hover{color:var(--teal)}
.nav-cta{margin-left:auto;display:flex;gap:12px;align-items:center}
.btn{display:inline-flex;align-items:center;gap:9px;border:none;cursor:pointer;font-family:Inter;font-weight:600;border-radius:999px;transition:.18s;font-size:15px;text-decoration:none}
.btn-primary{background:var(--teal);color:#04231c;padding:12px 22px}
.btn-primary:hover{background:var(--teal-d);color:#fff;transform:translateY(-1px)}
.btn-outline{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.35);padding:10px 20px}
.btn-outline:hover{border-color:var(--teal);color:var(--teal)}
.btn-coral{background:var(--coral);color:#fff;padding:12px 22px}
.btn-coral:hover{background:var(--coral-d);color:#fff;transform:translateY(-1px)}

/* ---------- Hero ---------- */
.hero{position:relative;background:radial-gradient(120% 120% at 80% 0%,var(--navy-3),var(--navy) 60%);color:#eaf1f8;overflow:hidden}
.hero::before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.12) 1.3px,transparent 1.3px);background-size:22px 22px;opacity:.25;mask:radial-gradient(60% 60% at 20% 30%,#000,transparent)}
.blob{position:absolute;border-radius:50%;filter:blur(8px);opacity:.5;z-index:0}
.blob.t{width:230px;height:230px;background:rgba(24,196,160,.30);top:-60px;right:8%}
.blob.c{width:160px;height:160px;background:rgba(242,77,99,.28);bottom:-40px;left:42%}
.squiggle{position:absolute;z-index:1;opacity:.85}
.hero .wrap{position:relative;z-index:2;display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center;padding:70px 28px 90px}
.eyebrow{display:inline-flex;align-items:center;gap:8px;color:var(--teal);font-weight:600;font-size:14px;letter-spacing:.03em;text-transform:uppercase;margin-bottom:18px}
.hero h1{font-size:54px;line-height:1.08;font-weight:800;margin:0 0 20px;color:#fff}
.hero .lead{font-size:18px;color:#b9c6d6;max-width:34em;margin:0 0 30px}
.hero-actions{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:30px}
.play{display:inline-flex;align-items:center;gap:12px;color:#fff;font-weight:600}
.play .circ{width:52px;height:52px;border-radius:50%;background:var(--coral);display:grid;place-items:center;box-shadow:0 8px 22px rgba(242,77,99,.45);font-size:16px;animation:pulse 2.4s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(242,77,99,.45)}70%{box-shadow:0 0 0 16px rgba(242,77,99,0)}100%{box-shadow:0 0 0 0 rgba(242,77,99,0)}}
.chips{display:flex;gap:10px;flex-wrap:wrap}
.chip{display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);color:#dce6f0;padding:8px 14px;border-radius:999px;font-size:13.5px;font-weight:500}
.chip b{color:#fff}
/* hero card */
.hero-card{position:relative;background:#fff;color:var(--ink);border-radius:22px;padding:26px;box-shadow:0 24px 60px rgba(0,0,0,.35)}
.hero-card .ring{position:absolute;top:-26px;right:-18px;width:96px;height:96px;background:#fff;border-radius:50%;box-shadow:var(--shadow);display:grid;place-items:center}
.hero-card .ring svg{transform:rotate(-90deg)}
.hero-card .ring .lab{position:absolute;font-family:Poppins;font-weight:700;font-size:18px;color:var(--teal-d)}
.hero-card h3{margin:4px 0 14px;font-size:19px}
.hero-card ul{list-style:none;margin:0 0 18px;padding:0}
.hero-card li{display:flex;gap:11px;align-items:flex-start;padding:9px 0;border-bottom:1px dashed var(--line);font-size:14.5px;color:#36424f}
.hero-card li:last-child{border-bottom:none}
.hero-card li .ic{font-size:17px;line-height:1.4}
.float-badge{position:absolute;left:18px;bottom:-26px;background:#fff;border-radius:14px;box-shadow:var(--shadow);padding:12px 16px;display:flex;gap:10px;align-items:center;font-size:13px;font-weight:600;color:var(--ink)}
.float-badge .n{font-family:Poppins;font-weight:800;color:var(--coral);font-size:20px}

/* ---------- Content layout ---------- */
.layout{display:grid;grid-template-columns:268px minmax(0,1fr);gap:46px;max-width:1200px;margin:0 auto;padding:0 28px}
aside{position:sticky;top:84px;align-self:start;height:calc(100vh - 100px);overflow-y:auto;padding:26px 0}
.toc-card{background:var(--soft);border:1px solid var(--line);border-radius:18px;padding:18px}
.toc-close{display:none;position:absolute;top:-6px;right:-4px;width:36px;height:36px;border:none;background:var(--navy-2);color:#fff;border-radius:50%;font-size:22px;line-height:1;cursor:pointer}
.toc-close:hover{background:var(--coral)}
.toc-title{font-family:Poppins;font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--teal-d);margin:0 0 10px;font-weight:700}
.toc ul{list-style:none;margin:0;padding:0}
.toc a{display:block;color:var(--muted);font-size:14px;padding:6px 12px;border-radius:8px;border-left:2px solid transparent;line-height:1.4}
.toc a:hover{color:var(--ink);background:#fff}
.toc a.active{color:var(--teal-d);background:#fff;border-left-color:var(--teal);font-weight:600}
.toc .toc li li a{padding-left:24px;font-size:13px}
.toc a.toc-capstone{color:var(--coral);font-weight:600}
main{padding:54px 0 120px;min-width:0}
article{max-width:var(--max)}

/* typography */
article h2{font-size:30px;margin:56px 0 16px;font-weight:700;position:relative}
article h2::before{content:"\2726";color:var(--teal);font-size:18px;margin-right:10px;vertical-align:2px}
article h3{font-size:21px;margin:34px 0 10px;font-weight:600}
article h2+h3{margin-top:18px}
article p,article li{font-size:16.5px}
article ul,article ol{padding-left:24px}
article li{margin:7px 0}
article strong{font-weight:700;color:#0f1b28}
hr{border:none;height:1px;background:var(--line);margin:42px 0}

/* tables */
table{border-collapse:separate;border-spacing:0;width:100%;margin:24px 0;font-size:15px;border:1px solid var(--line);border-radius:14px;overflow:hidden;display:block;overflow-x:auto}
th,td{padding:12px 15px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
th{background:var(--navy-2);color:#eaf1f8;font-family:Poppins;font-weight:600;font-size:14px}
tr:last-child td{border-bottom:none}
tbody tr:nth-child(even){background:var(--soft)}

/* inline + block code */
code{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:.86em;background:var(--teal-soft);color:#0c6a55;padding:.13em .42em;border-radius:6px}
.codehilite,pre{position:relative;background:var(--code-bg);border-radius:14px;margin:22px 0;overflow:hidden;box-shadow:var(--shadow-sm)}
.codehilite pre{margin:0;border-radius:0;box-shadow:none;background:transparent}
.codehilite pre,pre>code{display:block;padding:42px 18px 18px;overflow-x:auto}
.codehilite code,pre code{background:none;color:#dfe6ee;padding:0;font-size:13.5px;line-height:1.7}
.code-bar{position:absolute;top:0;left:0;right:0;height:34px;display:flex;align-items:center;gap:7px;padding:0 15px;background:rgba(255,255,255,.05);border-bottom:1px solid rgba(255,255,255,.07)}
.code-bar .dot{width:11px;height:11px;border-radius:50%}
.dot.r{background:#ff5f57}.dot.y{background:#febc2e}.dot.g{background:#28c840}
.copy-btn{position:absolute;top:5px;right:9px;z-index:3;background:rgba(255,255,255,.08);color:#dfe6ee;border:1px solid rgba(255,255,255,.14);border-radius:8px;font-size:12px;padding:4px 11px;cursor:pointer;font-family:Inter;transition:.15s}
.copy-btn:hover{background:var(--teal);border-color:var(--teal);color:#04231c}
.copy-btn.done{background:var(--teal);color:#04231c;border-color:var(--teal)}

/* callouts */
blockquote{margin:24px 0;padding:18px 22px;border-radius:14px;background:var(--soft);border:1px solid var(--line);box-shadow:var(--shadow)}
blockquote p{margin:7px 0}blockquote p:first-child{margin-top:0}blockquote p:last-child{margin-bottom:0}
blockquote.cl-key{background:var(--k-bg);border-color:transparent}
blockquote.cl-tip{background:var(--tip-bg);border-color:transparent}
blockquote.cl-ok{background:var(--ok-bg);border-color:transparent}
blockquote.cl-no{background:var(--no-bg);border-color:transparent}
blockquote.cl-goal{background:var(--goal-bg);border-color:transparent}

/* capstone banner */
h2.capstone-h{background:linear-gradient(115deg,var(--navy),var(--navy-3));color:#fff;border-radius:20px;padding:30px 28px 26px;margin-top:64px;box-shadow:0 20px 50px rgba(10,26,47,.3);overflow:hidden;position:relative}
h2.capstone-h::before{content:"\1F6E0\FE0F  HANDS-ON PROJECT";display:block;font-family:Poppins;font-size:12px;font-weight:700;letter-spacing:.14em;color:var(--teal);margin:0 0 8px}
h2.capstone-h::after{content:"";position:absolute;width:150px;height:150px;border-radius:50%;background:rgba(24,196,160,.25);filter:blur(10px);top:-50px;right:-30px}

/* check-off */
.checkable{list-style:none;padding-left:0}
.checkable li{position:relative;padding-left:36px;cursor:pointer;margin:9px 0}
.checkable li::before{content:"";position:absolute;left:0;top:3px;width:22px;height:22px;border:2px solid var(--teal);border-radius:7px;background:#fff;transition:.15s}
.checkable li.checked::before{background:var(--teal);border-color:var(--teal)}
.checkable li.checked::after{content:"\2713";position:absolute;left:5px;top:1px;color:#fff;font-weight:800;font-size:15px}
.checkable li.checked{color:var(--muted)}

/* footer */
footer.site{background:var(--navy);color:#aebccb;margin-top:90px}
footer.site .wrap{padding:46px 28px;display:flex;justify-content:space-between;gap:26px;flex-wrap:wrap;align-items:center}
footer.site .logo{font-size:20px}
footer.site .fnote{max-width:46em;font-size:13.5px;line-height:1.7}

#menuBtn{display:none}
@media(max-width:920px){
  .topbar{display:none}
  .nav-cta{display:none}
  .float-badge{display:none}
  nav.bar .wrap{gap:14px;height:60px}
  .wrap{padding:0 20px}
  .logo{font-size:18px;white-space:nowrap}
  .hero .wrap{grid-template-columns:1fr;gap:30px;padding:42px 20px 56px}
  .hero h1{font-size:33px}
  .hero .lead{font-size:16.5px}
  .hero-actions{gap:14px}
  .hero-actions .btn-primary{flex:1;justify-content:center}
  .layout{grid-template-columns:1fr;gap:0}
  aside{position:fixed;top:0;left:0;width:84vw;max-width:320px;height:100vh;background:#fff;z-index:130;transform:translateX(-100%);transition:.25s;box-shadow:var(--shadow);padding:24px}
  aside.open{transform:none}
  #menuBtn{display:inline-flex}
  .toc-close{display:block}
  .navlinks{display:none}
  main{padding:34px 0 80px}
  body{font-size:16px}
  article h2{font-size:25px}
  h2.capstone-h{padding:24px 20px}
}
@media(max-width:420px){
  .hero h1{font-size:29px}
  .hero-actions{flex-direction:column;align-items:stretch}
  .hero-actions .play{justify-content:center}
}
</style>
</head>
<body>
<div id="progress"></div>

{{TOPBAR}}

<nav class="bar"><div class="wrap">
  <button class="btn btn-outline" id="menuBtn" style="padding:8px 14px">&#9776;</button>
  <a class="logo" href="{{HOME}}">{{COURSE}}<span class="dot">.</span></a>
  <div class="navlinks">
    <a href="{{HOME}}">{{HOME_LABEL}}</a>{{NAV_EXTRA}}
  </div>
{{NAV_CTA}}
</div></nav>

<header class="hero">
  <span class="blob t"></span><span class="blob c"></span>
{{SQUIGGLES}}
  <div class="wrap" id="overview">
    <div>
      <span class="eyebrow">&#10022; {{EYEBROW}}</span>
      <h1>{{HERO_TITLE}}</h1>
      <p class="lead">{{LEAD}}</p>
{{HERO_ACTIONS}}
{{CHIPS}}
    </div>
{{HERO_CARD}}
  </div>
</header>

<div class="layout">
  <aside id="sidebar"><div class="toc-card">
    <button class="toc-close" id="tocClose" aria-label="Close menu">&times;</button>
    <p class="toc-title">On this page</p>
    {{TOC}}
  </div></aside>
  <main id="start">
    <article>
      {{BODY}}
    </article>
    {{NAV}}
  </main>
</div>

<footer class="site"><div class="wrap">
  <a class="logo" href="{{HOME}}">{{COURSE}}<span class="dot">.</span></a>
  <span class="fnote">{{FOOTER_NOTE}}</span>
</div></footer>

<style>{{PYGMENTS_CSS}}</style>
<script>
// mobile menu
const sb=document.getElementById('sidebar'),mb=document.getElementById('menuBtn');
if(mb){mb.onclick=()=>sb.classList.toggle('open');sb.addEventListener('click',e=>{if(e.target.tagName==='A')sb.classList.remove('open')});}
const tc=document.getElementById('tocClose');if(tc){tc.onclick=()=>sb.classList.remove('open');}
// progress
const prog=document.getElementById('progress');
addEventListener('scroll',()=>{const h=document.body.scrollHeight-innerHeight;prog.style.width=(h>0?scrollY/h*100:0)+'%'});
// code chrome + copy
document.querySelectorAll('.codehilite, pre').forEach(block=>{
  if(block.parentElement.classList.contains('codehilite'))return;
  const bar=document.createElement('div');bar.className='code-bar';
  bar.innerHTML='<span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>';
  block.appendChild(bar);
  const btn=document.createElement('button');btn.className='copy-btn';btn.textContent='Copy';
  btn.onclick=()=>{const t=block.querySelector('code')?.innerText||block.innerText;
    navigator.clipboard.writeText(t.replace(/\nCopy$/,''));btn.textContent='Copied!';btn.classList.add('done');
    setTimeout(()=>{btn.textContent='Copy';btn.classList.remove('done')},1500)};
  block.appendChild(btn);
});
// callouts by leading emoji
const map={'\u{1F511}':'cl-key','\u{1F4A1}':'cl-tip','✅':'cl-ok','❌':'cl-no','\u{1F3AF}':'cl-goal','\u{1F6E0}':'cl-goal'};
document.querySelectorAll('blockquote').forEach(q=>{const t=(q.textContent||'').trim();for(const e in map){if(t.startsWith(e)){q.classList.add(map[e]);break}}});
// check-off
function wireList(el){if(el.dataset.wired)return;el.dataset.wired='1';el.classList.add('checkable');
  el.querySelectorAll(':scope>li').forEach(li=>{const key='cwc:'+location.pathname+':'+li.textContent.slice(0,60);
    if(localStorage.getItem(key))li.classList.add('checked');
    li.addEventListener('click',ev=>{if(ev.target.tagName==='A')return;li.classList.toggle('checked');
      li.classList.contains('checked')?localStorage.setItem(key,'1'):localStorage.removeItem(key)});});}
function makeCheckable(rx){document.querySelectorAll('h2,h3').forEach(h=>{if(!rx.test(h.textContent))return;let el=h.nextElementSibling;
  while(el&&!/^H[1-3]$/.test(el.tagName)){if(el.tagName==='OL'||el.tagName==='UL')wireList(el);el=el.nextElementSibling;}});}
makeCheckable(/learning objectives|milestones|done when/i);
// lists written as `- [ ] thing` are check-off lists wherever they appear
document.querySelectorAll('ul.checkable,ol.checkable').forEach(wireList);
// scrollspy
const links=[...document.querySelectorAll('.toc a')];
const heads=links.map(a=>a.getAttribute('href')).filter(h=>h&&h.startsWith('#')).map(h=>document.getElementById(h.slice(1))).filter(Boolean);
const spy=()=>{let cur=heads[0]?.id;for(const h of heads){if(h.getBoundingClientRect().top<150)cur=h.id}
  links.forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+cur))};
addEventListener('scroll',spy);spy();
</script>
</body>
</html>
'''

DEFAULT_CFG = {
    "title": "The Course",
    "source_label": "Self-paced course",
    "footer_note": "A self-paced course generated from source talks. Code snippets are "
                   "illustrative reconstructions of the approaches shown. Adapt them to the current SDK.",
}


def load_cfg(course_json=None):
    """Load course.json if present; fall back to sensible defaults."""
    cfg = dict(DEFAULT_CFG)
    if course_json and pathlib.Path(course_json).exists():
        cfg.update(json.loads(pathlib.Path(course_json).read_text(encoding="utf-8")))
    return cfg


# Long lessons are split into several short, linked pages. A page break can
# only fall between whole `## ` sections (never mid-section, so no content is
# altered); sections are packed greedily up to PAGE_WORDS reading-words, and the
# Capstone always starts a fresh page. One page for short lessons.
PAGE_WORDS = 1900


def _split_sections(body_src):
    """Split lesson markdown (after the meta block) into (heading, chunk) at H2."""
    out = []
    for p in re.split(r"(?m)^(?=## )", body_src):
        if not p.strip():
            continue
        hm = re.match(r"##\s+(.+)", p)
        out.append((hm.group(1).strip() if hm else "", p))
    return out


_TASK_LI = re.compile(r"<li>\s*\[([ xX])\]\s*")


def _task_lists(body_html):
    """Turn GitHub-style task lists into check-off lists.

    python-markdown has no task-list extension enabled, so `- [ ] thing`
    renders as the literal text "[ ] thing". Any list whose items carry the
    marker is instead stripped of the markers and tagged `checkable`, which
    the page script wires up and persists in localStorage. Lists without the
    marker are untouched, so existing courses render exactly as before.
    """
    def fix(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        if not _TASK_LI.search(inner):
            return m.group(0)
        inner = _TASK_LI.sub(
            lambda t: '<li class="checked">' if t.group(1) in "xX" else "<li>", inner)
        if "checkable" not in attrs:
            attrs = (attrs + ' class="checkable"') if "class=" not in attrs else \
                re.sub(r'class="', 'class="checkable ', attrs, count=1)
        return f"<{tag}{attrs}>{inner}</{tag}>"

    return re.sub(r"<(ul|ol)([^>]*)>(.*?)</\1>", fix, body_html, flags=re.S)


def _wc(text):
    """Rough reading-word count, ignoring fenced code blocks."""
    return len(re.findall(r"\w+", re.sub(r"```.*?```", "", text, flags=re.S)))


def _plan_pages(sections):
    """Greedy-pack sections into pages by word budget; force a break at Capstone."""
    pages, cur, cur_w = [], [], 0
    for heading, chunk in sections:
        is_capstone = "capstone" in heading.lower()
        w = _wc(chunk)
        if cur and (is_capstone or cur_w + w > PAGE_WORDS):
            pages.append(cur)
            cur, cur_w = [], 0
        cur.append((heading, chunk))
        cur_w += w
    if cur:
        pages.append(cur)
    return pages or [[]]


def _page_label(sections):
    """Short human label for a page, from its section headings."""
    heads = [h for h, _ in sections]
    if any(LEAD_HEADING in h for h in heads):
        return "Start here"
    if any("capstone" in h.lower() for h in heads):
        return "Capstone & wrap-up"
    nums = [int(pm.group(1)) for h in heads for pm in [re.match(r"Part\s+(\d+)", h)] if pm]
    if nums:
        return f"Part {nums[0]}" if len(nums) == 1 else f"Parts {nums[0]}-{nums[-1]}"
    if any("Key takeaways" in h for h in heads):
        return "Wrap-up"
    return (heads[0][:22] if heads else "")


def convert(md_path, out_path, cfg=None, home="../index.html", prev=None, nxt=None):
    cfg = cfg or dict(DEFAULT_CFG)
    raw = pathlib.Path(md_path).read_text(encoding="utf-8")

    m = re.match(r"#\s+(.+)\n", raw)
    title_full = m.group(1).strip() if m else "Lesson"
    body_src = raw[m.end():] if m else raw

    # Meta block (first blockquote) -> hero fields.
    meta_block = ""
    bm = re.match(r"\s*((?:^>.*\n?)+)", body_src, re.M)
    if bm:
        meta_block = bm.group(1)
        body_src = body_src[bm.end():]

    global LEAD_HEADING, ITEM_LABEL
    LEAD_HEADING = cfg.get("lead_heading", "In one sentence")
    ITEM_LABEL = cfg.get("unit_labels", {}).get("item", "Lesson")

    def field(label):
        mm = re.search(r"\*\*" + label + r":?\*\*\s*(.+)", meta_block)
        return mm.group(1).strip() if mm else ""

    # Optional. Courses that do not credit a speaker per lesson simply omit the chip.
    speaker = field("Speaker").split(",")[0].strip()
    speaker_chip = (f'<span class="chip">&#127908; <b>{html.escape(speaker)}</b></span>'
                    if speaker else "")
    time_raw = field("Estimated time")
    time_short = re.sub(r"\s*\(.*\)", "", time_raw).strip() or "45 to 60 min"
    yt = re.search(r"\((https?://[^)]*(?:youtube\.com|youtu\.be)[^)]*)\)", meta_block)
    yt_url = yt.group(1) if yt else ""

    # Eyebrow + hero title (split on the first ": ").
    if ": " in title_full:
        eyebrow, hero_title = title_full.split(": ", 1)
    else:
        eyebrow, hero_title = "Lesson", title_full
    bits = hero_title.rsplit(" ", 1)
    hero_title_html = (html.escape(bits[0]) + ' <span class="accent">' + html.escape(bits[1]) + "</span>") \
        if len(bits) == 2 else html.escape(hero_title)

    # Lead = first paragraph under the configured lead heading ("In one
    # sentence" by default, "Where you are" for the protocol).
    lead = ""
    lm = re.search(r"##\s+" + re.escape(LEAD_HEADING) + r"\s*\n+([^\n#]+(?:\n[^\n#]+)*)",
                   body_src)
    if lm:
        lead = re.sub(r"\s+", " ", lm.group(1)).strip()
        # The lead is placed into the hero as plain text, so strip inline
        # markdown (bold/italic/code/links) that would otherwise show as raw
        # markers like **word**.
        lead = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", lead)   # [text](url) -> text
        lead = re.sub(r"\*\*(.+?)\*\*", r"\1", lead)            # **bold**
        lead = re.sub(r"__(.+?)__", r"\1", lead)                 # __bold__
        lead = re.sub(r"`([^`]+)`", r"\1", lead)                 # `code`
        lead = re.sub(r"(?<![\w*])\*(?!\s)([^*]+?)(?<!\s)\*(?!\w)", r"\1", lead)  # *italic*

    # ---- paginate into short, linked pages --------------------------------
    sections = _split_sections(body_src)
    pages = _plan_pages(sections)
    n = len(pages)
    labels = [_page_label(pg) for pg in pages]

    out_path = pathlib.Path(out_path)
    stem, suf = out_path.stem, out_path.suffix

    def page_file(i):
        return out_path.name if i == 1 else f"{stem}-{i}{suf}"

    first_file, last_file = page_file(1), page_file(n)

    # Remove stale extra pages from any previous build with more pages.
    for old in out_path.parent.glob(f"{stem}-*{suf}"):
        if re.fullmatch(rf"{re.escape(stem)}-\d+{re.escape(suf)}", old.name):
            old.unlink()

    # The unit number out of the H1, used as the sync id. Keyed off the
    # configured item label, so "Phase 1 · Session 7" yields 7 exactly as
    # "Module 2 · Lesson 7" does. Hardcoding "Lesson" here silently disabled
    # the mark-complete button and the progress strip on every protocol page.
    lm2 = re.search(re.escape(ITEM_LABEL) + r"\s+(\d+)", title_full)
    lesson_num = lm2.group(1) if lm2 else ""

    home_fwd = home.replace("\\", "/")
    base = home_fwd.rsplit("/", 1)[0] if "/" in home_fwd else "."

    pyg_css = HtmlFormatter(style="one-dark").get_style_defs(".codehilite")
    if yt_url:
        watch = (f'<a class="play" href="{html.escape(yt_url)}" target="_blank" rel="noopener">'
                 f'<span class="circ">&#9654;</span> Watch the talk</a>')
    else:
        watch = ""

    def pager(i, where):
        if n < 2:
            return ""
        seg = '<div class="seg">' + "".join(
            f'<a href="{html.escape(page_file(j))}" class="{"cur" if j == i else ""}" '
            f'title="{html.escape(labels[j - 1])}">{j}</a>' for j in range(1, n + 1)) + '</div>'
        count = f'<span class="pcount">Page {i} of {n} &middot; {html.escape(labels[i - 1])}</span>'
        prev_c = "disabled" if i == 1 else ""
        next_c = "disabled" if i == n else ""
        prev_h = "#" if i == 1 else html.escape(page_file(i - 1))
        next_h = "#" if i == n else html.escape(page_file(i + 1))
        btns = (f'<div class="pbtns">'
                f'<a class="pbtn prev {prev_c}" href="{prev_h}">&#8592; Prev</a>'
                f'<a class="pbtn next {next_c}" href="{next_h}">Next &#8594;</a></div>')
        return f'<div class="pager {where}">{count}{seg}{btns}</div>'

    for i, page in enumerate(pages, 1):
        page_md = "\n".join(chunk for _, chunk in page)
        md = markdown.Markdown(
            extensions=["fenced_code", "tables", "toc", "sane_lists", "attr_list", "codehilite"],
            extension_configs={
                "codehilite": {"guess_lang": False, "css_class": "codehilite"},
                "toc": {"toc_depth": "2-3"},
            },
        )
        body_html = _task_lists(md.convert(page_md))
        toc_html = md.toc

        # Stable "capstone" id so nav/hero buttons and the TOC link always reach it.
        body_html = re.sub(r'<h2 id="[^"]*"(>\s*(?:\U0001F6E0️?\s*)?Capstone)',
                           r'<h2 id="capstone" class="capstone-h"\1', body_html)
        toc_html = re.sub(r'<a href="#[^"]*"(>\s*(?:\U0001F6E0️?\s*)?Capstone)',
                          r'<a href="#capstone" class="toc-capstone"\1', toc_html)

        # Between-lesson cards: previous lesson only on page 1, next only on last.
        nav = '<nav class="lessonnav">'
        if i == 1 and prev:
            nav += (f'<a class="ln prev" href="{html.escape(prev["href"])}">'
                    f'<span class="dir">&#8592; Previous {ITEM_LABEL.lower()}</span><b>{html.escape(prev["title"])}</b></a>')
        nav += f'<a class="ln home" href="{html.escape(home)}"><b>All {ITEM_LABEL.lower()}s</b></a>'
        if i == n and nxt:
            nav += (f'<a class="ln next" href="{html.escape(nxt["href"])}">'
                    f'<span class="dir">Next {ITEM_LABEL.lower()} &#8594;</span><b>{html.escape(nxt["title"])}</b></a>')
        nav += '</nav>'

        overview_href = "#overview" if i == 1 else html.escape(first_file) + "#overview"
        capstone_href = "#capstone" if i == n else html.escape(last_file) + "#capstone"
        body_with_pager = pager(i, "top") + body_html + pager(i, "bottom")

        # Full hero on page 1; compact header strip on later pages.
        template = TEMPLATE
        if i > 1:
            compact = (
                '<header class="lp-head"><div class="wrap">'
                f'<span class="eyebrow">&#10022; {html.escape(eyebrow)}</span>'
                f'<h1>{hero_title_html}</h1>'
                f'<p class="part">Part {i} of {n} &middot; {html.escape(labels[i - 1])}</p>'
                '</div></header>'
            )
            template = re.sub(r'<header class="hero">.*?</header>', compact, template, flags=re.S)

        # ---- optional chrome -----------------------------------------------
        # Every flag defaults to True, so existing courses render exactly as
        # before. A course opts out with "chrome": {"topbar": false, ...}.
        ch = cfg.get("chrome", {})
        def on(k):
            return ch.get(k, True)
        plural = ITEM_LABEL.lower() + "s"
        topbar_html = ('<div class="topbar"><div class="wrap">'
                       '<div>&#10024; Welcome to <b>' + html.escape(cfg.get("title", "")) + '</b> &middot; a self-paced course</div>'
                       '<div class="right"><span>' + html.escape(cfg.get("source_label", "")) + '</span></div>'
                       '</div></div>') if on("topbar") else ""
        nav_extra = ('<a href="{{OVERVIEW_HREF}}">Overview</a>'
                     '<a href="{{CAPSTONE_HREF}}">Capstone</a>') if on("nav_links") else ""
        nav_cta = ('<div class="nav-cta"><a class="btn btn-primary" href="#start">Start the '
                   + ITEM_LABEL.lower() + ' &#8594;</a></div>') if on("start_button") else ""
        squiggles = ('<svg class="squiggle" style="top:120px;left:46%;" width="90" height="26" viewBox="0 0 90 26" fill="none"><path d="M2 13c8-14 16 14 24 0s16 14 24 0 16 14 24 0" stroke="#18c4a0" stroke-width="4" stroke-linecap="round"/></svg>'
                     '<svg class="squiggle" style="bottom:60px;right:40%;" width="70" height="22" viewBox="0 0 90 26" fill="none"><path d="M2 13c8-14 16 14 24 0s16 14 24 0 16 14 24 0" stroke="#f24d63" stroke-width="4" stroke-linecap="round"/></svg>') if on("squiggles") else ""
        hero_actions = ('<div class="hero-actions"><a class="btn btn-primary" href="#start">Start the '
                        + ITEM_LABEL.lower() + ' &#8594;</a>' + watch + '</div>') if on("hero_actions") else ""
        chips_html = ('<div class="chips">' + speaker_chip
                      + '<span class="chip">&#9201; <b>' + html.escape(time_short) + '</b></span>'
                      + ('<span class="chip">&#128296; <b>Hands-on capstone</b></span>' if on("capstone_chip") else "")
                      + '</div>') if on("chips") else ""
        hero_card = HERO_CARD_HTML if on("hero_card") else ""

        out = (template
               .replace("{{TITLE}}", html.escape(title_full) + ("" if n < 2 else f" (p{i}/{n})"))
               .replace("{{COURSE}}", html.escape(cfg.get("title", DEFAULT_CFG["title"])))
               .replace("{{SOURCE_LABEL}}", html.escape(cfg.get("source_label", DEFAULT_CFG["source_label"])))
               .replace("{{FOOTER_NOTE}}", html.escape(cfg.get("footer_note", DEFAULT_CFG["footer_note"])))
               .replace("{{EYEBROW}}", html.escape(eyebrow))
               .replace("{{HERO_TITLE}}", hero_title_html)
               .replace("{{LEAD}}", html.escape(lead))
               .replace("{{SPEAKER_CHIP}}", speaker_chip)
               .replace("{{TOPBAR}}", topbar_html)
               .replace("{{HOME_LABEL}}", "All " + plural)
               .replace("{{NAV_EXTRA}}", nav_extra)
               .replace("{{NAV_CTA}}", nav_cta)
               .replace("{{SQUIGGLES}}", squiggles)
               .replace("{{HERO_ACTIONS}}", hero_actions)
               .replace("{{CHIPS}}", chips_html)
               .replace("{{HERO_CARD}}", hero_card)
               .replace("{{TIME}}", html.escape(time_short))
               .replace("{{WATCH}}", watch)
               # The newline is part of the match so a course with no icons
               # loses the whole line rather than leaving a blank one.
               .replace("{{ICONS}}\n", icon_links(base) + "\n" if cfg.get("_icons") else "")
               .replace("{{HOME}}", html.escape(home))
               .replace("{{OVERVIEW_HREF}}", overview_href)
               .replace("{{CAPSTONE_HREF}}", capstone_href)
               .replace("{{NAV}}", nav)
               .replace("{{TOC}}", toc_html)
               .replace("{{BODY}}", body_with_pager)
               .replace("{{PYGMENTS_CSS}}", pyg_css))

        # Progress sync: bottom bar on every page; "mark complete" only on the
        # last page (one lesson = one tracked unit). Non-last pages carry an
        # invisible marker so the fixed progress bar still renders.
        if cfg.get("sync") and lesson_num:
            if i == n:
                hook = (
                    f'<section class="lesson-sync" data-lesson-id="{lesson_num}" data-home="{base}/index.html">'
                    '<div class="ls-inner">'
                    '<button type="button" class="ls-btn" data-lesson-complete>'
                    f'Mark this {ITEM_LABEL.lower()} complete</button>'
                    '<span class="ls-status" data-sync-status></span>'
                    '</div>'
                    f'<a class="ls-track" href="{base}/index.html">Your progress &#8594;</a>'
                    '</section>'
                )
            else:
                hook = (f'<div class="ls-marker" data-lesson-id="{lesson_num}" '
                        f'data-home="{base}/index.html" style="display:none"></div>')
            script = (f'<script src="{base}/assets/course-data.js"></script>'
                      f'<script type="module" src="{base}/assets/sync.js"></script>')
            if '<nav class="lessonnav">' in out:
                out = out.replace('<nav class="lessonnav">', hook + '<nav class="lessonnav">', 1)
            else:
                out = out.replace("</body>", hook + "</body>", 1)
            out = out.replace("</body>", script + "</body>", 1)

        dest = out_path if i == 1 else out_path.with_name(page_file(i))
        dest.write_text(out, encoding="utf-8")

    total_kb = sum(out_path.with_name(page_file(i)).stat().st_size for i in range(1, n + 1)) // 1024
    print(f"wrote {out_path} + {n - 1} more page(s) [{n} pages, {total_kb} KB]")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: build_lesson.py <input.md> <output.html> [course.json]")
    cfg = load_cfg(sys.argv[3] if len(sys.argv) > 3 else None)
    convert(sys.argv[1], sys.argv[2], cfg=cfg)
