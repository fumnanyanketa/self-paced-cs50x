#!/usr/bin/env python3
"""Build the whole course: render every lesson (with prev/next/home links) + the index.

Generic, config-driven. Point it at a course root that contains:
    course.json                 (branding + module names/blurbs)
    lessons/module-N-slug/NN-slug.md

It writes lessons-html/ next to lessons/, mirroring the folder structure, plus
lessons-html/index.html (the landing page) and a root index.html redirect.

Usage:
    python3 build_course.py [course-root]      # default: current directory

Dependencies (markdown, pygments) are auto-installed on first run if missing.
"""
import importlib
import os
import pathlib
import re
import subprocess
import sys

# --- bootstrap dependencies so the script "just works" ----------------------
for pkg in ("markdown", "pygments"):
    try:
        importlib.import_module(pkg)
    except ImportError:
        print(f"installing {pkg} ...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", pkg], check=True)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_lesson as bl  # noqa: E402

ROOT = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path.cwd()
LESSONS = ROOT / "lessons"
OUT_ROOT = ROOT / "lessons-html"
CFG_PATH = ROOT / "course.json"

if not LESSONS.exists():
    sys.exit(f"no lessons/ directory under {ROOT}")

cfg = bl.load_cfg(str(CFG_PATH))

# When course.json enables the progress tracker ("sync" block), scaffold the
# tracker engine into lessons-html/assets/. The engine (sync.js) is refreshed on
# every build so courses pick up fixes; sync-config.js (which holds the user's
# Firebase keys) is written only if absent, so a filled-in config is never lost.
if cfg.get("sync"):
    import shutil
    bundled = pathlib.Path(__file__).resolve().parent / "assets"
    dest = OUT_ROOT / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    if (bundled / "sync.js").exists():
        shutil.copyfile(bundled / "sync.js", dest / "sync.js")
    if (bundled / "sync-config.js").exists() and not (dest / "sync-config.js").exists():
        shutil.copyfile(bundled / "sync-config.js", dest / "sync-config.js")
        print("scaffolded assets/sync-config.js (fill in Firebase keys to enable cross-device sync)")

# Course-supplied static files. A course may keep its own assets/ directory
# (favicons, images, anything the pages link to) beside course.json; those are
# copied verbatim into lessons-html/assets/ on every build. This is the only
# supported way to get a hand-made file into the generated site, since
# lessons-html/ is wiped and rewritten and must never be hand-edited.
_src_assets = ROOT / "assets"
if _src_assets.is_dir():
    import shutil
    dest = OUT_ROOT / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    _copied = 0
    for f in sorted(_src_assets.iterdir()):
        if f.is_file() and not f.name.startswith("."):
            shutil.copyfile(f, dest / f.name)
            _copied += 1
    if _copied:
        print(f"copied {_copied} course asset(s) from assets/")

# Only emit favicon tags when the course actually ships one, so a course without
# icons does not serve four 404s on every page load.
if (_src_assets / "favicon.svg").exists():
    cfg["_icons"] = True

def relhref(target, start):
    """Relative link with forward slashes, so pages work when served over HTTP.

    os.path.relpath emits backslashes on Windows, which a web server treats as a
    literal character rather than a path separator, so every link 404s.
    """
    return os.path.relpath(target, start).replace(os.sep, "/")


# Vocabulary. Defaults keep every existing course working unchanged.
_labels = cfg.get("unit_labels", {})
GROUP = _labels.get("group", "Module")
ITEM = _labels.get("item", "Lesson")

items = []
for md in LESSONS.glob("*/*.md"):
    text = md.read_text(encoding="utf-8")
    m = re.match(rf"#\s+{GROUP}\s+\d+\s+·\s+{ITEM}\s+(\d+):\s+(.+)", text)
    if not m:
        print(f"skip (no '{GROUP} N · {ITEM} M: Title' H1):", md)
        continue
    num = int(m.group(1))
    title = m.group(2).strip()
    out = (OUT_ROOT / md.relative_to(LESSONS)).with_suffix(".html")
    items.append({"num": num, "title": title, "md": md, "out": out})

items.sort(key=lambda x: x["num"])

for i, it in enumerate(items):
    it["out"].parent.mkdir(parents=True, exist_ok=True)
    prev = nxt = None
    if i > 0:
        p = items[i - 1]
        prev = {"title": p["title"], "href": relhref(p["out"], it["out"].parent)}
    if i < len(items) - 1:
        n = items[i + 1]
        nxt = {"title": n["title"], "href": relhref(n["out"], it["out"].parent)}
    home = relhref(OUT_ROOT / "index.html", it["out"].parent)
    bl.convert(str(it["md"]), str(it["out"]), cfg=cfg, home=home, prev=prev, nxt=nxt)

print(f"rendered {len(items)} lessons")

# Rebuild the landing page.
subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve().parent / "build_index.py"), str(ROOT)], check=True)

# Root redirect so opening the project root lands on the course.
(ROOT / "index.html").write_text(
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta http-equiv="refresh" content="0; url=lessons-html/index.html">'
    '<link rel="canonical" href="lessons-html/index.html">'
    f'<title>{cfg.get("title", "Course")}</title></head>'
    '<body style="font-family:system-ui;text-align:center;padding:60px">'
    'Redirecting to the course. If nothing happens, open '
    '<a href="lessons-html/index.html">the course</a>.</body></html>',
    encoding="utf-8")

print(f"done. open {OUT_ROOT / 'index.html'}")
