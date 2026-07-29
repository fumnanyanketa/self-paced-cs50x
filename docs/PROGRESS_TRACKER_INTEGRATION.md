# Built-in progress tracker: integration guide

This document describes the **embedded progress-tracker system** added to the
Self-Paced CS50x course, written so it can be reproduced on any course built with
the same generator (a `course.json` + `lessons/**/*.md` + `tools/` build system).

It has two parts:

- **Part A — Update the course-creator skill**, so every *new* course you generate
  ships with the tracker automatically.
- **Part B — Retrofit an existing course** that was already built.

Both parts use the same set of files, listed in full in the **Appendix**. Hand this
whole file to the Claude instance that owns the skill (Part A) or the existing
course (Part B).

---

## What the tracker adds

1. **A persistent progress bar on every lesson page** — a slim strip fixed to the
   bottom of the viewport showing `X/N · %` complete plus a day-streak. It updates
   live when a lesson is marked complete, and links to the full tracker.
2. **The home/landing page becomes the tracker** — a live "Your progress" panel
   (lessons done, % complete, streak, projected finish), a checkbox on every lesson
   row with completion dates, per-module counts, a pace selector, Google sign-in,
   and backup/restore/reset.
3. **`progress.html` becomes a redirect** to the home page, so any old link to the
   standalone tracker still works.
4. **Optional cross-device sync** via Firebase (Google sign-in + Firestore). Until
   configured, everything still works and saves in one browser (localStorage).

## How it works (architecture)

- **`lessons-html/assets/sync.js`** — the `CourseSync` engine. Holds progress in
  `localStorage`, optionally mirrors to Firebase, exposes shared stats
  (`stats()`, `streak()`, …), auto-wires each lesson's "Mark complete" button, and
  injects the persistent bottom bar on lesson pages. **Single source of truth.**
- **`lessons-html/assets/sync-config.js`** — the Firebase web config (four
  `REPLACE_ME` values). Not secret; protected by Firestore security rules.
- **`lessons-html/assets/course-data.js`** — *generated* by the index builder.
  Sets `window.COURSE_DATA = { coreTotal, optionalIds }` so the per-lesson bar and
  the home tracker share one definition of the core-lesson total.
- **`tools/build_lesson.py`** — when `course.json` has a `sync` block, injects the
  per-lesson "Mark complete" control, a `data-home` attribute (so the bar knows
  where the tracker lives), and loads `course-data.js` *before* `sync.js`.
- **`tools/build_index.py`** — renders the landing page **as** the tracker
  (checkboxes, stats panel, pace, account, backup/restore) and writes
  `assets/course-data.js`.
- **`course.json`** — must contain `"sync": {"provider": "firebase"}` to switch the
  injection on.

The trigger for the whole system is the `sync` block in `course.json`. With it
present, the build scripts wire everything up; without it, the course builds as a
plain static site.

---

## Part A — Update the course-creator skill (future courses)

Do this once in the skill so every course you generate afterward has the tracker.

1. **Add the two front-end assets to the skill's asset template** (the files the
   skill copies into every course's `lessons-html/assets/`):
   - `assets/sync.js`  → use the full contents in the Appendix.
   - `assets/sync-config.js` → use the full contents in the Appendix.
2. **Replace the skill's `scripts/build_index.py`** with the version in the
   Appendix. It renders the tracker UI and emits `assets/course-data.js`.
3. **Patch the skill's `scripts/build_lesson.py`** — apply the one-block change in
   the Appendix (adds `data-home`, points the in-lesson link at the home tracker,
   and loads `course-data.js` before `sync.js`).
4. **Make the skill write a `sync` block into every generated `course.json`:**
   add `"sync": {"provider": "firebase"}` to the course-config template.
5. **(Optional) Ship a `FIREBASE_SETUP.md`** in each course so the author can turn
   on cross-device sync later. The tracker works fully without it.

That's it — the next course the skill builds will have the persistent bar, the
home-page tracker, and the redirect, with sync ready to switch on.

---

## Part B — Retrofit a course you already built

For a course that already exists (same build system: `course.json`, `lessons/`,
`tools/`). All steps are copy-in-then-rebuild.

1. **Drop the two assets in** `lessons-html/assets/`:
   `sync.js` and `sync-config.js` (Appendix). If the course already had an older
   `sync.js`, overwrite it.
2. **Update the build scripts** in `tools/` (or wherever the course keeps them):
   - Replace `build_index.py` with the Appendix version.
   - Apply the `build_lesson.py` block change from the Appendix.
3. **Turn the tracker on** in `course.json` by adding (if not already there):
   `"sync": {"provider": "firebase"}`.
4. **Replace `lessons-html/progress.html`** with the redirect stub (Appendix), or
   delete it — the home page is the tracker now.
5. **Rebuild the whole site** from the course root:

   `python tools/build_course.py .`

   This regenerates every lesson page (now with the bar), rewrites the home page as
   the tracker, and writes `assets/course-data.js`.
6. **(Optional) Enable cross-device sync** by following `FIREBASE_SETUP.md` and
   pasting your four Firebase values into `assets/sync-config.js`.
7. **Commit, push, and deploy** however that course ships (e.g. push to the branch
   your GitHub Pages workflow deploys from).

### Verifying the retrofit
- Open a lesson page: a bar should sit at the bottom showing `0/N · 0%`. Click
  **Mark this lesson complete** — it should tick to `1/N` with a streak.
- Open the home page: the "Your progress" panel and per-lesson checkboxes should
  reflect that mark. Tick another lesson; the count and its module tally update.
- Open `progress.html`: it should redirect to the home page.
- Note: Google Fonts, the Firebase CDN, and sign-in only work over http(s), not
  from a double-clicked `file://` page. Use `python -m http.server` locally.

---

# Appendix — full file contents


## `lessons-html/assets/sync.js`

~~~javascript
// ---------------------------------------------------------------------------
// CourseSync: cross-device progress for Self-Paced CS50x.
//
// Signed out (or before Firebase is configured): progress is kept in this
// browser's localStorage, so the course still works fully offline.
// Signed in with Google: progress is stored in Firestore under your account and
// mirrored to every device you sign in on. localStorage stays as an offline
// cache, so the page paints instantly and queued writes sync when back online.
// ---------------------------------------------------------------------------
import { firebaseConfig } from "./sync-config.js";

const FB_VER = "10.12.0";
const LS_LESSONS = "spcs50x:progress";
const LS_PACE = "spcs50x:pace";
const CONFIGURED = !!(firebaseConfig && firebaseConfig.projectId && firebaseConfig.projectId !== "REPLACE_ME");

let user = null;
let auth = null, db = null, userDocRef = null, unsubDoc = null, fb = null;
const listeners = new Set();
let state = { lessons: loadLocalLessons(), pace: loadLocalPace() };

function loadLocalLessons() { try { return JSON.parse(localStorage.getItem(LS_LESSONS)) || {}; } catch (e) { return {}; } }
function loadLocalPace() { const p = parseInt(localStorage.getItem(LS_PACE) || "1", 10); return isNaN(p) ? 1 : p; }
function saveLocal() { localStorage.setItem(LS_LESSONS, JSON.stringify(state.lessons)); localStorage.setItem(LS_PACE, String(state.pace)); }
function emit() { listeners.forEach(fn => { try { fn(); } catch (e) {} }); }
function todayISO() { const d = new Date(); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
function daysBetween(a, b) { return Math.round((new Date(b + "T00:00") - new Date(a + "T00:00")) / 86400000); }

async function pushCloud() {
  if (user && userDocRef && fb) {
    try { await fb.setDoc(userDocRef, { lessons: state.lessons, pace: state.pace, updated: Date.now() }, { merge: true }); } catch (e) {}
  }
}

const CourseSync = {
  configured() { return CONFIGURED; },
  ready() { return true; },
  state() { return state; },
  user() { return user; },
  isDone(n) { return !!state.lessons[String(n)]; },
  dateOf(n) { return state.lessons[String(n)] || ""; },
  onChange(fn) { listeners.add(fn); return () => listeners.delete(fn); },
  // ---- shared progress stats (single source of truth for the bar + tracker) ----
  coreTotal() { return (window.COURSE_DATA && window.COURSE_DATA.coreTotal) || 43; },
  optionalIds() { return (window.COURSE_DATA && window.COURSE_DATA.optionalIds) || [0]; },
  coreDone() {
    const opt = new Set(this.optionalIds().map(String));
    return Object.keys(state.lessons).filter(k => !opt.has(String(k))).length;
  },
  streak() {
    const dates = [...new Set(Object.values(state.lessons))].sort();
    if (!dates.length) return 0;
    if (daysBetween(dates[dates.length - 1], todayISO()) > 1) return 0;
    let s = 1;
    for (let i = dates.length - 1; i > 0; i--) { if (daysBetween(dates[i - 1], dates[i]) === 1) s++; else break; }
    return s;
  },
  weekCount() {
    const t = todayISO();
    return Object.values(state.lessons).filter(d => { const n = daysBetween(d, t); return n >= 0 && n < 7; }).length;
  },
  stats() {
    const total = this.coreTotal();
    const done = Math.min(this.coreDone(), total);
    return { done, total, pct: total ? Math.round(done / total * 100) : 0, streak: this.streak(), week: this.weekCount() };
  },
  toggleLesson(n) { this.setLesson(n, !this.isDone(n)); },
  setLesson(n, done) {
    n = String(n);
    if (done) { if (!state.lessons[n]) state.lessons[n] = todayISO(); }
    else { delete state.lessons[n]; }
    saveLocal(); emit(); pushCloud();
  },
  setPace(p) { state.pace = p; saveLocal(); emit(); pushCloud(); },
  exportData() { return JSON.stringify(state.lessons); },
  importData(str) { try { const o = JSON.parse(str); if (o && typeof o === "object") { state.lessons = o; saveLocal(); emit(); pushCloud(); return true; } } catch (e) {} return false; },
  reset() { state.lessons = {}; saveLocal(); emit(); pushCloud(); },
  async signIn() {
    if (!CONFIGURED) { alert("Cross-device sync is not set up yet.\nAdd your Firebase config to assets/sync-config.js to enable sign-in."); return; }
    if (!auth || !fb) { alert("Still starting up. Try again in a second."); return; }
    try { await fb.signInWithPopup(auth, new fb.GoogleAuthProvider()); }
    catch (e) { alert("Sign-in failed: " + ((e && e.message) || e)); }
  },
  async signOut() {
    if (auth && fb) { try { await fb.signOut(auth); } catch (e) {} }
    user = null; state.lessons = loadLocalLessons(); emit();
  }
};
window.CourseSync = CourseSync;

async function initFirebase() {
  if (!CONFIGURED) { emit(); return; }
  try {
    const [appMod, authMod, fsMod] = await Promise.all([
      import(`https://www.gstatic.com/firebasejs/${FB_VER}/firebase-app.js`),
      import(`https://www.gstatic.com/firebasejs/${FB_VER}/firebase-auth.js`),
      import(`https://www.gstatic.com/firebasejs/${FB_VER}/firebase-firestore.js`)
    ]);
    const app = appMod.initializeApp(firebaseConfig);
    auth = authMod.getAuth(app);
    try { db = fsMod.initializeFirestore(app, { localCache: fsMod.persistentLocalCache({ tabManager: fsMod.persistentMultipleTabManager() }) }); }
    catch (e) { db = fsMod.getFirestore(app); }
    fb = {
      GoogleAuthProvider: authMod.GoogleAuthProvider,
      signInWithPopup: authMod.signInWithPopup,
      signOut: authMod.signOut,
      doc: fsMod.doc, onSnapshot: fsMod.onSnapshot, setDoc: fsMod.setDoc, getDoc: fsMod.getDoc
    };
    authMod.onAuthStateChanged(auth, async (u) => {
      if (unsubDoc) { unsubDoc(); unsubDoc = null; }
      user = u ? { name: u.displayName || u.email, email: u.email, uid: u.uid } : null;
      if (u) {
        userDocRef = fb.doc(db, "progress", u.uid);
        await mergeLocalIntoCloud();
        unsubDoc = fb.onSnapshot(userDocRef, (snap) => {
          const data = (snap && snap.data && snap.data()) || {};
          state.lessons = data.lessons || {};
          if (typeof data.pace === "number") state.pace = data.pace;
          saveLocal(); emit();
        });
      }
      emit();
    });
  } catch (e) {
    console.warn("CourseSync: Firebase init failed, staying in local-only mode.", e);
    emit();
  }
}

async function mergeLocalIntoCloud() {
  try {
    const snap = await fb.getDoc(userDocRef);
    const cloud = (snap.exists() ? (snap.data().lessons || {}) : {});
    let changed = false;
    for (const k in state.lessons) { if (!cloud[k]) { cloud[k] = state.lessons[k]; changed = true; } }
    if (!snap.exists() || changed) {
      await fb.setDoc(userDocRef, { lessons: cloud, pace: state.pace, updated: Date.now() }, { merge: true });
    }
  } catch (e) {}
}

// ---- auto-wire a "Mark this lesson complete" button on lesson pages ----
function paintBox(box) {
  const n = box.getAttribute("data-lesson-id");
  const btn = box.querySelector("[data-lesson-complete]");
  const status = box.querySelector("[data-sync-status]");
  const done = CourseSync.isDone(n);
  box.classList.toggle("done", done);
  if (btn) btn.textContent = done ? "✓  Completed (click to undo)" : "Mark this lesson complete";
  if (status) {
    if (!CourseSync.configured()) status.textContent = "saved in this browser";
    else if (!CourseSync.user()) status.innerHTML = '<a href="#" data-signin>Sign in to sync across your devices</a>';
    else status.textContent = "synced as " + (CourseSync.user().name || "you");
  }
}
function wireLessonButtons() {
  document.querySelectorAll("[data-lesson-id]").forEach(box => {
    const btn = box.querySelector("[data-lesson-complete]");
    if (btn && !btn._wired) { btn._wired = true; btn.addEventListener("click", () => CourseSync.toggleLesson(box.getAttribute("data-lesson-id"))); }
    paintBox(box);
  });
}
document.addEventListener("click", (e) => { const a = e.target.closest("[data-signin]"); if (a) { e.preventDefault(); CourseSync.signIn(); } });
CourseSync.onChange(() => document.querySelectorAll("[data-lesson-id]").forEach(paintBox));

// ---- styles for the lesson button (injected once) ----
const css = `
.lesson-sync{margin:38px 0 8px;padding:18px 20px;border:1px solid #1e3a5a;border-radius:14px;background:#0f243d;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.lesson-sync.done{background:linear-gradient(90deg,rgba(45,212,191,.12),#0f243d 60%);border-color:#2dd4bf}
.lesson-sync .ls-inner{display:flex;align-items:center;gap:14px;flex-wrap:wrap;flex:1 1 auto}
.lesson-sync .ls-btn{background:#2dd4bf;color:#05202a;border:0;border-radius:10px;padding:11px 18px;font:600 1rem system-ui,sans-serif;cursor:pointer}
.lesson-sync.done .ls-btn{background:#16324f;color:#e8eef6;border:1px solid #2dd4bf}
.lesson-sync .ls-btn:hover{filter:brightness(1.06)}
.lesson-sync .ls-status{color:#9fb3c8;font-size:.85rem}
.lesson-sync .ls-status a{color:#2dd4bf}
.lesson-sync .ls-track{color:#2dd4bf;font-size:.9rem;text-decoration:none;white-space:nowrap}
.lesson-sync .ls-track:hover{text-decoration:underline}`;
const st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

// ---- persistent course-progress bar on every lesson page ----
// Always-visible strip fixed to the bottom of the viewport so a learner never
// has to remember a separate tracker page: their standing is always on screen,
// and the whole bar links to the home page (which is the full tracker).
const barCss = `
#course-progress-bar{position:fixed;left:0;right:0;bottom:0;z-index:150;background:#0a1a2f;border-top:1px solid #1e3a5a;color:#e8eef6;display:flex;align-items:center;gap:14px;padding:9px 16px;font:600 .85rem system-ui,-apple-system,Segoe UI,Roboto,sans-serif;text-decoration:none;box-shadow:0 -6px 20px rgba(0,0,0,.28)}
#course-progress-bar:hover{background:#0c1f38}
#course-progress-bar .cpb-label{color:#9fb3c8;font-weight:600;white-space:nowrap}
#course-progress-bar .cpb-track{flex:1 1 auto;height:8px;background:#16324f;border-radius:999px;overflow:hidden;min-width:70px;max-width:360px}
#course-progress-bar .cpb-fill{display:block;height:100%;width:0;background:linear-gradient(90deg,#2dd4bf,#34d399);transition:width .4s ease}
#course-progress-bar .cpb-count{color:#2dd4bf;white-space:nowrap}
#course-progress-bar .cpb-pct{color:#e8eef6;white-space:nowrap}
#course-progress-bar .cpb-streak{color:#f5c451;white-space:nowrap}
#course-progress-bar .cpb-cta{margin-left:auto;color:#9fb3c8;white-space:nowrap}
#course-progress-bar:hover .cpb-cta{color:#2dd4bf}
@media(max-width:560px){#course-progress-bar .cpb-label{display:none}#course-progress-bar{gap:10px;padding:8px 12px;font-size:.8rem}}`;
function injectCourseBar() {
  const box = document.querySelector("[data-lesson-id]");
  if (!box) return;                                   // lesson pages only
  if (document.getElementById("course-progress-bar")) return;
  const bs = document.createElement("style"); bs.textContent = barCss; document.head.appendChild(bs);
  const home = box.getAttribute("data-home") || "../index.html";
  const bar = document.createElement("a");
  bar.id = "course-progress-bar";
  bar.href = home;
  bar.innerHTML =
    '<span class="cpb-label">Course progress</span>' +
    '<span class="cpb-track"><span class="cpb-fill"></span></span>' +
    '<span class="cpb-count"></span>' +
    '<span class="cpb-pct"></span>' +
    '<span class="cpb-streak" style="display:none"></span>' +
    '<span class="cpb-cta">View tracker &#8594;</span>';
  document.body.appendChild(bar);
  document.body.style.paddingBottom = "56px";
  paintCourseBar();
}
function paintCourseBar() {
  const bar = document.getElementById("course-progress-bar");
  if (!bar) return;
  const s = CourseSync.stats();
  bar.querySelector(".cpb-fill").style.width = s.pct + "%";
  bar.querySelector(".cpb-count").textContent = s.done + "/" + s.total;
  bar.querySelector(".cpb-pct").textContent = s.pct + "%";
  const streak = bar.querySelector(".cpb-streak");
  if (s.streak > 0) { streak.style.display = ""; streak.textContent = "\u{1F525} " + s.streak; }
  else streak.style.display = "none";
}
CourseSync.onChange(paintCourseBar);

if (document.readyState !== "loading") { wireLessonButtons(); injectCourseBar(); }
else document.addEventListener("DOMContentLoaded", () => { wireLessonButtons(); injectCourseBar(); });
initFirebase();
~~~

## `lessons-html/assets/sync-config.js`

~~~javascript
// ---------------------------------------------------------------------------
// Firebase config for cross-device progress sync.
//
// HOW TO FILL THIS IN (one time):
//   1. Go to https://console.firebase.google.com and create a free project.
//   2. Add a "Web app" to it; Firebase shows you a config object.
//   3. Copy those values into the object below (replace every REPLACE_ME).
//   4. In the console: Build > Authentication > enable "Google" sign-in.
//   5. In the console: Build > Firestore Database > create it (production mode),
//      then paste the security rules from FIREBASE_SETUP.md.
//   6. Authentication > Settings > Authorized domains: add your GitHub Pages
//      domain (for example  yourname.github.io ). localhost is already allowed.
//
// Until you fill this in, the tracker still works, but only in this one browser
// (no cross-device sync, no sign-in). Nothing here is secret: a Firebase web
// config is meant to live in client code. Your data is protected by the
// Firestore security rules, not by hiding these values.
// ---------------------------------------------------------------------------
export const firebaseConfig = {
  apiKey: "REPLACE_ME",
  authDomain: "REPLACE_ME.firebaseapp.com",
  projectId: "REPLACE_ME",
  appId: "REPLACE_ME"
};
~~~

## `tools/build_index.py` (full replacement)

~~~python
#!/usr/bin/env python3
"""Build the course landing page (lessons-html/index.html) from the lesson files.

The landing page doubles as the progress tracker: it shows live stats (lessons
done, percent complete, streak, projected finish), a per-lesson checkbox on every
row, sign-in for cross-device sync, and backup/restore/reset. All progress logic
lives in assets/sync.js (window.CourseSync); this page renders against it.

Generic, config-driven. Scans lessons/**/*.md, reads each H1
("# Module N · Lesson M: Title") and the Speaker / Estimated time from the meta
blockquote, groups by module, and writes an index page in the same LMS style as
the lessons. Module names, blurbs, and course branding come from course.json.

It also emits lessons-html/assets/course-data.js (window.COURSE_DATA) so the
persistent progress bar on every lesson page shares one source of truth for the
core-lesson total.

Usage (normally called by build_course.py):
    python3 build_index.py [course-root]   # default: current directory
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path.cwd()
LESSONS = ROOT / "lessons"
CFG_PATH = ROOT / "course.json"

cfg = json.loads(CFG_PATH.read_text(encoding="utf-8")) if CFG_PATH.exists() else {}
COURSE = cfg.get("title", "The Course")
ACCENT = cfg.get("accent_word", "")            # a word in the title to color coral
TAGLINE = cfg.get("tagline", "A hands-on, self-paced course.")
FOOTER_NOTE = cfg.get("footer_note", "A self-paced course.")
START_HERE = cfg.get("start_here", "")          # optional path to an orientation page
MODULES = {int(k): v for k, v in cfg.get("modules", {}).items()}

# Headline = course title with the accent word (if any) colored.
if ACCENT and ACCENT in COURSE:
    head_html = html.escape(COURSE).replace(html.escape(ACCENT), f'<span class="a">{html.escape(ACCENT)}</span>', 1)
else:
    head_html = html.escape(COURSE)

lessons = []
for md in sorted(LESSONS.glob("*/*.md")):
    text = md.read_text(encoding="utf-8")
    m = re.match(r"#\s+Module\s+(\d+)\s+·\s+Lesson\s+(\d+):\s+(.+)", text)
    if not m:
        continue
    mod, num, title = int(m.group(1)), int(m.group(2)), m.group(3).strip()
    sm = re.search(r"\*\*Speaker:?\*\*\s*(.+)", text)
    speaker = sm.group(1).strip() if sm else ""
    tm = re.search(r"\*\*Estimated time:?\*\*\s*(.+)", text)
    time = re.sub(r"\s*\(.*\)", "", tm.group(1)).strip() if tm else ""
    href = str(md.relative_to(LESSONS)).replace(".md", ".html")  # index sits inside lessons-html
    lessons.append((mod, num, title, speaker, time, href))

lessons.sort(key=lambda x: x[1])
by_mod = {}
for L in lessons:
    by_mod.setdefault(L[0], []).append(L)

# Module 0 is an optional pre-flight and is not counted in the core total.
def is_optional(mod):
    return mod == 0

cards = []
for mod in sorted(by_mod):
    items = ""
    for (_, num, title, speaker, time, href) in by_mod[mod]:
        sub = " · ".join(x for x in [html.escape(speaker), html.escape(time)] if x)
        opt_badge = '<span class="opt">optional</span>' if is_optional(mod) else ""
        items += (
            f'<div class="lesson" data-n="{num}">'
            f'<span class="box" data-n="{num}" role="checkbox" aria-checked="false" tabindex="0" '
            f'aria-label="Mark lesson {num} complete">&#10003;</span>'
            f'<a class="lbody" href="{html.escape(href)}">'
            f'<span class="num">{num:02d}</span>'
            f'<span class="ltext"><span class="lt">{html.escape(title)}</span>'
            f'<span class="ls">{sub}</span></span>'
            f'{opt_badge}'
            f'<span class="ldate" data-date="{num}"></span>'
            f'<span class="arr">&#8594;</span></a>'
            f'</div>'
        )
    mname = MODULES.get(mod, {}).get("name", f"Module {mod}")
    mblurb = MODULES.get(mod, {}).get("blurb", "")
    mtag = "Optional" if is_optional(mod) else f"Module {mod}"
    cards.append(
        f'<section class="modcard"><div class="modhead">'
        f'<div class="modrow"><span class="modtag">{mtag}</span>'
        f'<span class="modcount" data-mod="{mod}"></span></div>'
        f'<h2>{html.escape(mname)}</h2>'
        f'<p>{html.escape(mblurb)}</p></div>'
        f'<div class="lessons">{items}</div></section>')

# Headline counts describe the core curriculum (Modules 1+); an optional
# pre-flight (Module 0) is rendered as a card but not counted in the stats.
core_modules = len([m for m in by_mod if m >= 1])
core_lessons = len([L for L in lessons if L[0] >= 1])

start_btn = (f'<div style="margin-top:30px"><a href="{html.escape(START_HERE)}" '
             f'style="display:inline-flex;align-items:center;gap:9px;background:#18c4a0;color:#04231c;'
             f'font-weight:600;border-radius:999px;padding:13px 26px;text-decoration:none;font-family:Inter">'
             f'New here? Start with the orientation &#8594;</a></div>') if START_HERE else ""

# ---- shared course data for the per-lesson progress bar --------------------
optional_ids = sorted(n for (mod, n, *_ ) in lessons if is_optional(mod))
course_data = {
    "course": COURSE,
    "coreTotal": core_lessons,
    "optionalIds": optional_ids,
}
(ROOT / "lessons-html" / "assets").mkdir(parents=True, exist_ok=True)
(ROOT / "lessons-html" / "assets" / "course-data.js").write_text(
    "// Generated by build_index.py. Do not edit by hand.\n"
    "window.COURSE_DATA = " + json.dumps(course_data) + ";\n",
    encoding="utf-8")

# JS lesson registry: [num, module, optional(0/1)].
lessons_js = "[" + ",".join(
    f"[{num},{mod},{1 if is_optional(mod) else 0}]" for (mod, num, *_ ) in lessons
) + "]"

CSS = """
:root{--navy:#0a1a2f;--navy-2:#0f243d;--navy-3:#15314f;--teal:#18c4a0;--teal-d:#0fa385;--coral:#f24d63;--gold:#f5c451;--green:#34d399;--ink:#152230;--muted:#5f6c7b;--line:#e9eef2;--soft:#f4fbf9;--shadow:0 10px 30px rgba(13,30,52,.08)}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);font-family:Inter,system-ui,sans-serif;line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{text-decoration:none;color:inherit}
h1,h2{font-family:Poppins,sans-serif;letter-spacing:-.01em}
.wrap{max-width:1100px;margin:0 auto;padding:0 26px}
.hero{position:relative;background:radial-gradient(120% 120% at 80% 0%,var(--navy-3),var(--navy) 60%);color:#eaf1f8;overflow:hidden;text-align:center;padding:80px 0 90px}
.hero::before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.12) 1.3px,transparent 1.3px);background-size:22px 22px;opacity:.22;mask:radial-gradient(70% 70% at 50% 20%,#000,transparent)}
.blob{position:absolute;border-radius:50%;filter:blur(10px);opacity:.5}
.blob.t{width:240px;height:240px;background:rgba(24,196,160,.30);top:-70px;left:6%}
.blob.c{width:170px;height:170px;background:rgba(242,77,99,.26);bottom:-50px;right:10%}
.hero .in{position:relative;z-index:2}
.eyebrow{display:inline-flex;gap:8px;color:var(--teal);font-weight:600;letter-spacing:.04em;text-transform:uppercase;font-size:14px;margin-bottom:16px}
.hero h1{font-size:52px;line-height:1.08;margin:0 0 16px;color:#fff;font-weight:800}
.hero h1 .a{color:var(--coral)}
.hero p{color:#b9c6d6;font-size:18px;max-width:40em;margin:0 auto 26px}
.hstats{display:flex;gap:34px;justify-content:center;flex-wrap:wrap;margin-top:30px}
.hstat .n{font-family:Poppins;font-weight:800;font-size:30px;color:#fff}
.hstat .l{color:#9fb0c2;font-size:13.5px}
main{padding:0 0 100px}

/* ---- progress panel (the tracker, folded into the home page) ---- */
.panel-wrap{max-width:1100px;margin:-52px auto 0;padding:0 26px;position:relative;z-index:5}
.progress-panel{background:var(--navy-2);border:1px solid #1e3a5a;border-radius:20px;padding:24px 24px 22px;box-shadow:0 24px 60px rgba(8,19,31,.35);color:#e8eef6}
.pp-head{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-bottom:6px}
.pp-title{color:var(--teal);font-weight:700;letter-spacing:.06em;text-transform:uppercase;font-size:.74rem}
.account{display:flex;align-items:center;gap:12px;flex-wrap:wrap;background:var(--navy-3);border:1px solid #1e3a5a;border-radius:12px;padding:9px 13px}
.account .dot{width:9px;height:9px;border-radius:50%;background:#9fb3c8;flex:0 0 auto}
.account.on .dot{background:var(--green)}
.account #acct-msg{color:#9fb3c8;font-size:.85rem}
.account button{background:var(--teal);color:#05202a;border:0;border-radius:9px;padding:7px 13px;font:600 .88rem system-ui;cursor:pointer}
.account button.ghost{background:var(--navy);color:#e8eef6;border:1px solid #1e3a5a}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin:16px 0 6px}
.tile{background:var(--navy-3);border:1px solid #1e3a5a;border-radius:14px;padding:14px 15px 12px}
.tile .big{font-size:1.75rem;font-weight:700;line-height:1.1;font-family:Poppins}
.tile .lbl{color:#9fb3c8;font-size:.76rem;margin-top:3px}
.tile.accent .big{color:var(--teal)} .tile.streak .big{color:var(--gold)}
.tile.finish .big{font-size:1.1rem;padding-top:7px}
.barwrap{background:var(--navy-3);border:1px solid #1e3a5a;border-radius:999px;height:15px;overflow:hidden;margin:10px 0 4px}
#bar{height:100%;width:0;background:linear-gradient(90deg,var(--teal),var(--green));transition:width .4s ease}
.barrow{display:flex;justify-content:space-between;color:#9fb3c8;font-size:.8rem}
.pace{display:flex;align-items:center;gap:9px;margin:18px 0 2px;flex-wrap:wrap}
.pace>span{color:#9fb3c8;font-size:.88rem}
.pace button{background:var(--navy-3);color:#e8eef6;border:1px solid #1e3a5a;border-radius:8px;padding:6px 12px;cursor:pointer;font:inherit;font-size:.88rem}
.pace button.on{background:var(--teal);color:#05202a;border-color:var(--teal);font-weight:600}
#pace-note{color:#9fb3c8;font-size:.82rem}
.actions{margin-top:16px;display:flex;gap:9px;flex-wrap:wrap}
.actions button{background:var(--navy-3);color:#e8eef6;border:1px solid #1e3a5a;border-radius:8px;padding:7px 13px;cursor:pointer;font:inherit;font-size:.86rem}
.actions button:hover{border-color:var(--teal)}
.actions button.danger:hover{border-color:var(--coral);color:var(--coral)}

main.wrap{padding-bottom:100px}
.intro{text-align:center;max-width:40em;margin:48px auto 30px;color:var(--muted)}
.modcard{border:1px solid var(--line);border-radius:20px;padding:26px;margin:22px 0;box-shadow:var(--shadow)}
.modhead{margin-bottom:16px}
.modrow{display:flex;align-items:center;justify-content:space-between;gap:10px}
.modtag{display:inline-block;background:var(--soft);color:var(--teal-d);font-weight:700;font-size:12px;letter-spacing:.08em;text-transform:uppercase;padding:5px 12px;border-radius:999px}
.modcount{color:var(--muted);font-size:12.5px;font-weight:600;white-space:nowrap}
.modcount.complete{color:var(--teal-d)}
.modhead h2{font-size:24px;margin:12px 0 4px}
.modhead p{margin:0;color:var(--muted);font-size:15px}
.lessons{display:grid;gap:10px;margin-top:8px}
.lesson{display:flex;align-items:center;gap:14px;padding:12px 16px;border:1px solid var(--line);border-radius:14px;transition:.15s;background:#fff}
.lesson:hover{border-color:var(--teal);box-shadow:var(--shadow)}
.lesson.done{background:linear-gradient(90deg,rgba(24,196,160,.09),#fff 55%)}
.lesson .box{flex:0 0 auto;width:24px;height:24px;border:2px solid var(--line);border-radius:7px;cursor:pointer;display:grid;place-items:center;color:transparent;font-weight:800;font-size:.9rem;user-select:none;transition:.15s}
.lesson .box:hover{border-color:var(--teal)}
.lesson.done .box{background:var(--teal);border-color:var(--teal);color:#04231c}
.lbody{display:flex;align-items:center;gap:16px;flex:1;min-width:0;color:inherit}
.lesson .num{font-family:Poppins;font-weight:800;color:var(--teal);font-size:18px;min-width:34px}
.ltext{display:flex;flex-direction:column;flex:1;min-width:0}
.lt{font-weight:600}
.lesson.done .lt{color:var(--muted);text-decoration:line-through}
.ls{color:var(--muted);font-size:13px}
.opt{color:var(--gold);font-size:11px;font-weight:700;border:1px solid var(--gold);border-radius:6px;padding:0 6px;white-space:nowrap}
.ldate{color:var(--muted);font-size:12px;white-space:nowrap}
.arr{color:var(--teal);font-size:20px}
footer{background:var(--navy);color:#aebccb;text-align:center;padding:40px 26px;font-size:14px}
.logo{font-family:Poppins;font-weight:800;font-size:22px;color:#fff}
.logo .d{color:var(--teal)}
dialog{background:var(--navy-2);color:#e8eef6;border:1px solid #1e3a5a;border-radius:12px;max-width:520px;width:92%}
dialog textarea{width:100%;height:150px;background:var(--navy);color:#e8eef6;border:1px solid #1e3a5a;border-radius:8px;padding:10px;font:13px/1.4 ui-monospace,monospace}
dialog p{margin:0 0 8px}
dialog .row{display:flex;gap:8px;justify-content:flex-end;margin-top:10px}
dialog button{background:var(--navy-3);color:#e8eef6;border:1px solid #1e3a5a;border-radius:8px;padding:8px 14px;cursor:pointer;font:inherit}
@media(max-width:700px){.hero h1{font-size:34px}.hero{padding:56px 0 72px}.hstats{gap:22px}.stats{grid-template-columns:repeat(2,1fr)}main.wrap{padding-bottom:64px}}
"""

PANEL = """
<section class="progress-panel">
  <div class="pp-head">
    <span class="pp-title">&#10022; Your progress</span>
    <div class="account" id="account"><span class="dot"></span><span id="acct-msg">Starting up&hellip;</span><button id="acct-btn" style="display:none"></button></div>
  </div>
  <div class="stats">
    <div class="tile accent"><div class="big" id="s-count">0/0</div><div class="lbl">core lessons done</div></div>
    <div class="tile"><div class="big" id="s-pct">0%</div><div class="lbl">of the course</div></div>
    <div class="tile streak"><div class="big" id="s-streak">0</div><div class="lbl">day streak</div></div>
    <div class="tile finish"><div class="big" id="s-finish">set a pace</div><div class="lbl">projected finish</div></div>
  </div>
  <div class="barwrap"><div id="bar"></div></div>
  <div class="barrow"><span id="b-left"></span><span id="b-week">0 done in the last 7 days</span></div>
  <div class="pace"><span>My pace:</span>
    <button data-p="1">1 / day</button><button data-p="2">2 / day</button>
    <button data-p="3">3 / day</button><button data-p="5">5 / day</button>
    <span id="pace-note"></span>
  </div>
  <div class="actions"><button id="backup">Back up my progress</button><button id="restore">Restore from backup</button><button class="danger" id="reset">Reset all</button></div>
</section>
"""

DIALOG = """
<dialog id="dlg">
  <p id="dlg-msg"></p>
  <textarea id="dlg-text"></textarea>
  <div class="row"><button id="dlg-cancel">Close</button><button id="dlg-ok" style="display:none">Restore</button></div>
</dialog>
"""

SCRIPT = """
const CS = window.CourseSync;
const LESSONS = __LESSONS__;
const byMod = {};
LESSONS.forEach(([n, mod]) => { (byMod[mod] = byMod[mod] || []).push(n); });

function fmt(iso){ if(!iso) return ""; const [y,m,d]=iso.split("-").map(Number); return new Date(y,m-1,d).toLocaleDateString(undefined,{month:"short",day:"numeric"}); }

function render(){
  document.querySelectorAll(".lesson").forEach(row=>{
    const n=row.getAttribute("data-n"); const done=CS.isDone(n);
    row.classList.toggle("done",done);
    const box=row.querySelector(".box"); if(box) box.setAttribute("aria-checked",done?"true":"false");
    const dd=row.querySelector(".ldate"); if(dd) dd.textContent=done?fmt(CS.dateOf(n)):"";
  });
  document.querySelectorAll(".modcount").forEach(el=>{
    const mod=+el.getAttribute("data-mod"); const arr=byMod[mod]||[];
    const done=arr.filter(n=>CS.isDone(n)).length;
    el.textContent=done+"/"+arr.length+" done";
    el.classList.toggle("complete",arr.length>0 && done===arr.length);
  });
  updateStats(); paintPace(); paintAccount();
}
function updateStats(){
  const s=CS.stats();
  document.getElementById("s-count").textContent=s.done+"/"+s.total;
  document.getElementById("s-pct").textContent=s.pct+"%";
  document.getElementById("bar").style.width=s.pct+"%";
  const left=s.total-s.done;
  document.getElementById("b-left").textContent=left===0?"All core lessons complete \\u{1F389}":left+" lesson"+(left===1?"":"s")+" to go";
  document.getElementById("s-streak").textContent=s.streak;
  document.getElementById("b-week").textContent=s.week+" done in the last 7 days";
  const fin=document.getElementById("s-finish"), pace=CS.state().pace||1;
  if(left===0){ fin.textContent="Done!"; document.getElementById("pace-note").textContent=""; }
  else{ const days=Math.ceil(left/pace); const d=new Date(); d.setDate(d.getDate()+days);
    fin.textContent=d.toLocaleDateString(undefined,{month:"short",day:"numeric",year:"numeric"});
    document.getElementById("pace-note").textContent="at "+pace+"/day, about "+days+" day"+(days===1?"":"s")+" left"; }
}
function paintPace(){ document.querySelectorAll(".pace button").forEach(b=>b.classList.toggle("on",+b.dataset.p===(CS.state().pace||1))); }
function paintAccount(){
  const box=document.getElementById("account"), msg=document.getElementById("acct-msg"), btn=document.getElementById("acct-btn");
  const u=CS.user();
  box.classList.toggle("on",!!u);
  if(!CS.configured()){ msg.textContent="Progress is saved in this browser. Set up sync to follow you across devices."; btn.style.display="none"; }
  else if(u){ msg.textContent="Synced as "+(u.name||u.email||"you")+"."; btn.style.display=""; btn.textContent="Sign out"; btn.className="ghost"; }
  else{ msg.textContent="Sign in to sync across your laptop and phone."; btn.style.display=""; btn.textContent="Sign in with Google"; btn.className=""; }
}

document.querySelectorAll(".box").forEach(b=>{
  const n=b.getAttribute("data-n");
  b.addEventListener("click",e=>{ e.preventDefault(); CS.toggleLesson(n); });
  b.addEventListener("keydown",e=>{ if(e.key===" "||e.key==="Enter"){ e.preventDefault(); CS.toggleLesson(n); } });
});
document.querySelectorAll(".pace button").forEach(b=>b.addEventListener("click",()=>CS.setPace(+b.dataset.p)));
document.getElementById("acct-btn").addEventListener("click",()=>{ CS.user()?CS.signOut():CS.signIn(); });

const dlg=document.getElementById("dlg"), dtext=document.getElementById("dlg-text"),
      dmsg=document.getElementById("dlg-msg"), dok=document.getElementById("dlg-ok");
document.getElementById("backup").addEventListener("click",()=>{
  dmsg.textContent="Copy this and keep it safe. Paste it back with Restore to recover your progress.";
  dtext.value=CS.exportData(); dtext.readOnly=true; dok.style.display="none"; dlg.showModal(); dtext.select();
});
document.getElementById("restore").addEventListener("click",()=>{
  dmsg.textContent="Paste a backup here and press Restore. This replaces your current progress.";
  dtext.value=""; dtext.readOnly=false; dok.style.display=""; dlg.showModal();
});
dok.addEventListener("click",()=>{ if(CS.importData(dtext.value.trim())) dlg.close(); else alert("That does not look like a valid backup."); });
document.getElementById("dlg-cancel").addEventListener("click",()=>dlg.close());
document.getElementById("reset").addEventListener("click",()=>{ if(confirm("Clear all progress? Back it up first if you want a copy.")) CS.reset(); });

CS.onChange(render);
render();
""".replace("__LESSONS__", lessons_js)

PAGE = (
    "<!doctype html>\n<html lang=\"en\"><head>\n"
    "<meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
    f"<title>{html.escape(COURSE)} | A self-paced course</title>\n"
    "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
    "<link href=\"https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap\" rel=\"stylesheet\">\n"
    "<style>" + CSS + "</style></head>\n<body>\n"
    "<header class=\"hero\"><span class=\"blob t\"></span><span class=\"blob c\"></span>\n"
    "  <div class=\"in wrap\">\n"
    "    <span class=\"eyebrow\">&#10022; Self-paced course</span>\n"
    f"    <h1>{head_html}</h1>\n"
    f"    <p>{html.escape(TAGLINE)}</p>\n"
    "    <div class=\"hstats\">\n"
    f"      <div class=\"hstat\"><div class=\"n\">{core_modules}</div><div class=\"l\">modules</div></div>\n"
    f"      <div class=\"hstat\"><div class=\"n\">{core_lessons}</div><div class=\"l\">lessons</div></div>\n"
    f"      <div class=\"hstat\"><div class=\"n\">{core_lessons}</div><div class=\"l\">hands-on capstones</div></div>\n"
    "    </div>\n"
    f"    {start_btn}\n"
    "  </div>\n"
    "</header>\n"
    "<div class=\"panel-wrap\">" + PANEL + "</div>\n"
    "<main class=\"wrap\">\n"
    "  <div class=\"intro\">Tick a lesson when you finish it &mdash; or use the &ldquo;Mark complete&rdquo; button on the lesson itself. Your progress shows here and on every lesson page. Work top to bottom, or jump to the module that fits you.</div>\n"
    "  " + "".join(cards) + "\n"
    "</main>\n"
    f"<footer><div class=\"logo\">{html.escape(COURSE)}<span class=\"d\">.</span></div>\n"
    f"<p>{html.escape(FOOTER_NOTE)}</p></footer>\n"
    + DIALOG +
    "<script src=\"assets/course-data.js\"></script>\n"
    "<script type=\"module\" src=\"assets/sync.js\"></script>\n"
    "<script type=\"module\">" + SCRIPT + "</script>\n"
    "</body></html>"
)

out = ROOT / "lessons-html" / "index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(PAGE, encoding="utf-8")
print(f"wrote {out} with {len(lessons)} lessons across {len(by_mod)} modules")
~~~

## `tools/build_lesson.py` — the one block to change

Inside `convert(...)`, in the `if cfg.get("sync"):` section, change the injected
`block` and `script` as follows.

**Before:**

~~~python
            block = (
                f'<section class="lesson-sync" data-lesson-id="{num}">'
                '<div class="ls-inner">'
                '<button type="button" class="ls-btn" data-lesson-complete>Mark this lesson complete</button>'
                '<span class="ls-status" data-sync-status></span>'
                '</div>'
                f'<a class="ls-track" href="{base}/progress.html">Progress tracker &#8594;</a>'
                '</section>'
            )
            script = f'<script type="module" src="{base}/assets/sync.js"></script>'
~~~

**After:**

~~~python
            block = (
                f'<section class="lesson-sync" data-lesson-id="{num}" data-home="{base}/index.html">'
                '<div class="ls-inner">'
                '<button type="button" class="ls-btn" data-lesson-complete>Mark this lesson complete</button>'
                '<span class="ls-status" data-sync-status></span>'
                '</div>'
                f'<a class="ls-track" href="{base}/index.html">Your progress &#8594;</a>'
                '</section>'
            )
            # course-data.js (generated, classic script) must load before the
            # sync module so window.COURSE_DATA is set when the bar renders.
            script = (f'<script src="{base}/assets/course-data.js"></script>'
                      f'<script type="module" src="{base}/assets/sync.js"></script>')
~~~

## `course.json` — the trigger

Add this top-level key (the whole system is off without it):

~~~json
"sync": {"provider": "firebase"}
~~~


## `lessons-html/progress.html` — redirect stub

~~~html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url=index.html">
<link rel="canonical" href="index.html">
<title>Progress Tracker: Self-Paced CS50x</title>
<style>body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#0a1a2f;color:#e8eef6;text-align:center;padding:60px 20px}a{color:#2dd4bf}</style>
</head>
<body>
<p>The progress tracker now lives on the course home page.</p>
<p>Redirecting&hellip; if nothing happens, open <a href="index.html">the course home page &rarr;</a>.</p>
</body>
</html>
~~~

