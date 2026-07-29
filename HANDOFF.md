# Handoff notes — continue from here

Continuation notes for another Claude instance (or a future session) picking up
this repo. Read this first, then check the "Outstanding" list below.

_Last updated: 2026-07-29._

## The project in one paragraph

`fumnanyanketa/self-paced-cs50x` is a static, self-paced companion course built
from CS50x 2026 lecture transcripts: 13 modules, 43 core lessons (+ an optional
pre-flight), each ending in a hands-on capstone. Source lessons are Markdown in
`lessons/`; the site is generated into `lessons-html/` by the scripts in `tools/`.
It deploys to GitHub Pages automatically on every push to `main`.

- **Live site:** https://fumnanyanketa.github.io/self-paced-cs50x/
- **Live tracker (= the home page):** same URL; the landing page *is* the tracker.
- **Deploy:** `.github/workflows/deploy.yml` runs `python tools/build_course.py .`
  and publishes on push to `main`. No manual step.
- **Local preview:** `python -m http.server` from the repo root, then open
  `http://localhost:8000/lessons-html/index.html`. Sign-in and ES modules do not
  work from a `file://` path.
- **Note for cloud/sandbox sessions:** outbound fetches to `*.github.io` are
  blocked by the sandbox proxy (403). Verify builds locally with a static server
  + headless Chromium instead of curling the public URL.

## What is already done

- **Progress tracker embedded into the course** (merged, live — was PR #1):
  - A persistent progress bar fixed to the bottom of every lesson page
    (`X/43 · % · streak`), updates live, links to the tracker.
  - The home page (`lessons-html/index.html`) is now the full tracker: live stats
    panel, per-lesson checkboxes, per-module counts, pace selector, Google
    sign-in, backup/restore/reset.
  - `lessons-html/progress.html` is now a redirect to the home page.
  - Engine: `lessons-html/assets/sync.js` (+ generated `assets/course-data.js`).
- **Integration guide** `docs/PROGRESS_TRACKER_INTEGRATION.md` (merged — was PR #2):
  full instructions + code to (A) update the course-creator skill and (B) retrofit
  another course with this tracker.

## Outstanding — what's left to do

### 1. Turn on Firebase cross-device sync  (waiting on the user)
Progress currently saves per-browser only. To sync across devices:
- The user creates a free Firebase project and gets 4 web-config values:
  `apiKey`, `authDomain`, `projectId`, `appId` (see `FIREBASE_SETUP.md`).
- Paste them into `lessons-html/assets/sync-config.js` (replace every `REPLACE_ME`).
- In the Firebase console: enable **Google** sign-in; create **Firestore** in
  production mode with the security rules from `FIREBASE_SETUP.md`; add
  `fumnanyanketa.github.io` to **Authentication → Authorized domains**.
- Commit + push to `main` (auto-deploys). No rebuild needed — it's a static asset,
  but running `python tools/build_course.py .` is harmless.
- Verify: the home-page panel should stop saying "saved in this browser" and show
  a working "Sign in with Google".

### 2. Update the course-creator skill  (must be done where the skill lives)
The skill that generates courses is **not** in this repo or the cloud environment
used for the tracker work — only this course's self-contained `tools/` copy is.
On the machine/instance that owns the skill, apply **Part A** of
`docs/PROGRESS_TRACKER_INTEGRATION.md` so every new course ships with the tracker.

### 3. The pending HTML correction  (needs the user to specify it)
Early on the user mentioned wanting to correct "something on the main file" and
never described what it was (we moved on to the tracker). Nothing has been changed
for this. Next step: ask the user which page and what the change is, then edit the
Markdown source in `lessons/` (or the relevant builder in `tools/`), rebuild, and
push. Do **not** hand-edit files in `lessons-html/` — they are generated and will
be overwritten on the next build.

## How to make and ship a change (quick reference)

1. Develop on branch `claude/repo-state-overview-bvpoyi` (or a fresh branch off
   `main`). Never push straight to `main`.
2. Edit **sources**: lesson content in `lessons/**/*.md`, branding/modules in
   `course.json`, templates/logic in `tools/*.py`, tracker engine in
   `lessons-html/assets/sync.js`.
3. Rebuild: `python tools/build_course.py .` (auto-installs `markdown`+`pygments`).
4. Verify locally with a static server + headless browser.
5. Commit, push, open a PR to `main`; merging `main` triggers the deploy.
