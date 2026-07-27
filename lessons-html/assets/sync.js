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

if (document.readyState !== "loading") wireLessonButtons();
else document.addEventListener("DOMContentLoaded", wireLessonButtons);
initFirebase();
