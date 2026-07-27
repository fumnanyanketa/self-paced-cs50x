# Turn on cross-device progress sync (Firebase)

Your progress tracker already works in one browser. To make it follow you across
your laptop and phone, do this one-time setup. It is free and takes about ten
minutes. You never touch code except pasting four values into one file.

## What you are setting up
A free Firebase project gives you two things: **Google sign-in** (so each device
knows it is you) and **Firestore** (a small cloud database that holds your
progress). The course front-end is already wired to both.

## Step 1: Create the project
1. Go to https://console.firebase.google.com and sign in with a Google account.
2. Click **Add project**, give it a name (for example `my-cs50-progress`), and
   finish. You can turn off Google Analytics; it is not needed.

## Step 2: Add a web app and copy the config
1. On the project home, click the **web icon** ( `</>` ) to add a web app.
2. Give it any nickname and click **Register app**. You do NOT need Firebase
   Hosting.
3. Firebase shows a `firebaseConfig = { ... }` object. Copy the values for
   `apiKey`, `authDomain`, `projectId`, and `appId`.
4. Open **`lessons-html/assets/sync-config.js`** and paste those four values in,
   replacing every `REPLACE_ME`. Save the file.

These values are not secret. A Firebase web config is meant to live in client
code; your data is protected by the security rules in Step 4, not by hiding it.

## Step 3: Enable Google sign-in
1. In the console left menu: **Build > Authentication > Get started**.
2. On the **Sign-in method** tab, click **Google**, toggle it **Enable**, pick a
   support email, and **Save**.

## Step 4: Create the database and lock it to each user
1. In the left menu: **Build > Firestore Database > Create database**.
2. Choose a location near you and start in **production mode**.
3. Open the **Rules** tab, replace everything with the rules below, and
   **Publish**. These let each signed-in person read and write only their own
   progress document, and nothing else:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /progress/{uid} {
      allow read, write: if request.auth != null && request.auth.uid == uid;
    }
  }
}
```

## Step 5: Authorize your web address
Google sign-in only runs on approved domains.
1. **Authentication > Settings > Authorized domains**.
2. `localhost` is already there (for local testing). Once your site is on GitHub
   Pages, click **Add domain** and add your Pages host, for example
   `yourname.github.io`.

## Step 6: Try it
- Open your site (the GitHub Pages URL, or a local server such as
  `python -m http.server` from the course folder). Opening files by double-click
  will not work for sign-in, because browsers block cloud sign-in on `file://`.
- Open `progress.html`, click **Sign in with Google**, and mark a lesson.
- Open the same page on your phone, sign in with the same Google account, and
  your progress is already there.

## Notes
- Signed out, the tracker still works and saves in that one browser. Signed in,
  everything syncs.
- The free Firebase (Spark) plan is far more than enough for one learner. No
  billing or card is required.
- If the sign-in popup is ever blocked on mobile, tell me and I will switch the
  code from a popup to a full-page redirect, which some phone browsers prefer.
