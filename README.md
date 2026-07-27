# Self-Paced CS50x

An unofficial, self-paced companion course built from the **CS50x 2026 lecture
transcripts** by David J. Malan, Harvard University. 12 core modules plus an
optional pre-flight, 43 lessons, each ending in a hands-on capstone.

CS50 is created by Harvard University. Watch the original lectures and do the
official problem sets at https://cs50.harvard.edu/x. This companion is for
learning the lectures deeply, not a replacement for the official course.

## View the course
Open **`lessons-html/index.html`** for the landing page, or
**`lessons-html/progress.html`** for the progress tracker (bookmark this one as
your home base). Everything is static HTML, so it runs anywhere.

To preview locally with the tracker and sign-in working, run a local server from
this folder (ES modules and cloud sign-in do not run from `file://`):

```
python -m http.server 8000
```

then open http://localhost:8000/lessons-html/progress.html

## Cross-device progress sync
Progress can sync across your devices via Firebase (Google sign-in + Firestore).
See **`FIREBASE_SETUP.md`** for the one-time setup. Until then, the tracker still
works and saves progress in one browser.

## Layout
- `lessons-html/` : the built course site (open this)
- `lessons-html/assets/` : progress-sync engine and your Firebase config
- `lessons/` : the lesson source in Markdown (edit these, then rebuild)
- `transcripts/` : the source lecture transcripts
- `PROGRESS.md` : a plain-text progress checklist
- `course.json` : course title, branding, module names

## Rebuild after editing a lesson
```
python <path-to-course-builder-skill>/scripts/build_course.py .
```
