<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6C63FF,100:3B82F6&height=180&section=header&text=WebToAPK&fontSize=52&fontColor=ffffff&fontAlignY=38&desc=HTML%20%2B%20CSS%20%2B%20JS%20→%20Android%20APK%20in%205%20Minutes&descAlignY=58&descSize=16" width="100%"/>

<br/>

[![Build](https://github.com/AKIB473/web-to-apk/actions/workflows/build.yml/badge.svg)](https://github.com/AKIB473/web-to-apk/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Android](https://img.shields.io/badge/Android-7.0%2B-3DDC84?logo=android&logoColor=white)](https://developer.android.com)
[![Capacitor](https://img.shields.io/badge/Capacitor-6.x-119EFF?logo=capacitor)](https://capacitorjs.com)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Stars](https://img.shields.io/github/stars/AKIB473/web-to-apk?style=social)](https://github.com/AKIB473/web-to-apk/stargazers)

<br/>

### Turn **any HTML/CSS/JavaScript** website into a real Android app
### No Android Studio · No local setup · No device needed

<br/>

[**🚀 Get Started**](#-how-to-use) · [**📥 Download Example APK**](https://github.com/AKIB473/web-to-apk/releases/latest) · [**🌟 Star this repo**](https://github.com/AKIB473/web-to-apk/stargazers)

</div>

---

## 🎯 Who is this for?

| You are... | This helps you... |
|---|---|
| 👩‍🎓 **Student** learning web dev | See your HTML project run as a real Android app |
| 💻 **Web Developer** | Package your web app for Android without learning native code |
| 📱 **Phone user** | Build a simple app for yourself or your friends |
| 🧑‍🏫 **Teacher** | Demonstrate how web → mobile works in a classroom |
| 🚀 **Startup / Freelancer** | Quickly prototype an Android app from your existing website |

**No experience with Android, Java, Kotlin, or Gradle required.**
If you can write HTML, you can ship an Android app.

---

## ✨ What problem does this solve?

Building an Android APK normally requires:
- Installing Android Studio (3 GB download)
- Setting up Java, Gradle, Android SDK
- Configuring signing keystores manually
- Learning Gradle build scripts
- A powerful computer with 8 GB+ RAM

**This repo removes all of that.**

You push your HTML files to GitHub. GitHub's servers do all the heavy lifting for free. You get a signed APK file you can install on any Android phone.

---

## 🛠️ How it works (under the hood)

```
Your HTML/CSS/JS files in www/
          │
          ▼
  GitHub Actions CI starts
  (runs on GitHub's free servers)
          │
          ▼
  npm ci  →  Capacitor syncs www/ into Android project
          │
          ▼
  Keystore setup (auto or real)
  ┌─────────────────────────────────┐
  │  No secrets set?               │
  │  → GitHub server generates     │
  │    a fresh keystore using      │
  │    Java keytool (real method,  │
  │    same as every Android dev)  │
  │                                │
  │  Secrets set?                  │
  │  → Uses your permanent key     │
  │    (required for Play Store)   │
  └─────────────────────────────────┘
          │
          ▼
  Gradle assembleRelease  →  APK built
  Gradle bundleRelease    →  AAB built
          │
          ▼
  Both files uploaded as Artifacts
  (available for 30 days)
          │
          ▼
  You download and install on your phone ✅
```

**Total build time:** ~5 minutes (first build ~10 min to download Android tools)

---

## 🚀 How to use

### Step 1 — Fork this repository

Click **Fork** at the top right of this page.
Name it anything you want (e.g. `my-android-app`).

> **What is forking?** It creates a copy of this repo in your GitHub account. You own it completely. You can change everything.

---

### Step 2 — Put your files in `www/`

Open your forked repo on GitHub. Go into the `www/` folder.

**Replace or edit the files** with your own HTML, CSS, and JavaScript:

```
www/
  index.html    ← your main page (REQUIRED)
  style.css     ← your styles
  app.js        ← your JavaScript
  images/       ← your images
  fonts/        ← your fonts
  (anything else you need)
```

**You can edit directly on GitHub** — no need to clone locally:
1. Click on `www/index.html`
2. Click the pencil ✏️ icon (top right)
3. Edit your HTML
4. Click **Commit changes**

---

### Step 3 — Watch the build run

After you commit, go to the **Actions** tab of your repo.
You'll see a build running automatically.

```
Actions tab → "Build Android APK" → Watch it run
```

Each step shows what's happening:
- ✅ Checkout — downloads your code
- ✅ Install npm packages — gets Capacitor
- ✅ Capacitor sync — puts your HTML into the Android project
- ✅ Setup signing keystore — creates or loads the signing key
- ✅ Build APK — Gradle compiles the Android APK
- ✅ Build AAB — creates the Play Store bundle
- ✅ Upload artifacts — saves the files for you to download

---

### Step 4 — Download your APK

1. Click the completed build run
2. Scroll down to **Artifacts**
3. Download **APK-v1.0.0**
4. You'll get a `.zip` file — extract it to find the `.apk`

---

### Step 5 — Install on your Android phone

**Method A: Via file manager**
1. Copy the `.apk` to your Android phone (USB, WhatsApp, Telegram, email — anything)
2. Open the file on your phone
3. If prompted: tap **Settings** → enable **"Install from unknown sources"**
4. Tap **Install**

**Method B: Directly from GitHub (on phone)**
1. Open this repo on your Android phone's browser
2. Go to **Actions** → latest build → **Artifacts**
3. Tap to download the APK
4. Install it

> **"Install from unknown sources"** just means your phone allows APKs from outside the Play Store. This is safe for APKs you built yourself.

---

## 📱 Example app

The `www/index.html` in this repo is a working demo app. It shows:
- A beautiful mobile UI with gradient background
- A button that responds to taps
- Device info (screen size, platform, language)

**Replace it completely with your own HTML.** The demo is just to show it works.

---

## 🔑 About the signing keystore

Every Android APK must be digitally signed before it can be installed. This is done with a **keystore** — a small file that contains your digital signature.

### What this repo does automatically:

| Situation | What happens |
|---|---|
| **No secrets set** (default) | GitHub's server generates a fresh keystore on every build using Java `keytool`. The APK is real and signed. Works on any Android device. NOT suitable for Play Store (key changes each build). |
| **Secrets set** (for Play Store) | Uses your permanent keystore. Same key every build. Required if you want to update your app on Google Play. |

### Is the auto-generated keystore "fake"?

**No.** It's generated using the exact same `keytool` command that every Android developer uses. The APK is properly signed and will install on any Android device. The only limitation is that since a new key is generated each build, you cannot use it for Play Store updates (Play Store requires the same key for updates).

---

## 🏪 Google Play Store setup (optional)

If you want to publish your app on Google Play, you need a **permanent keystore** that stays the same across all builds.

**Run this workflow once:**

1. Go to **Actions** tab
2. Click **"Setup Keystore (Run Once for Play Store)"**
3. Click **Run workflow** (top right)
4. Fill in:
   - **App name** — your app's name (e.g. `My Weather App`)
   - **Key alias** — any short name (e.g. `myapp`)
   - **Store password** — min 6 characters. **SAVE THIS — you need it forever**
   - **Key password** — can be same as store password
5. Click **Run workflow**
6. When done: download the **keystore-backup-KEEP-SAFE** artifact
7. Save the `release.jks` file somewhere safe (password manager, USB drive)

**After that:**
- Your signing passwords are saved automatically as GitHub Secrets
- Every future build uses your permanent keystore
- You can submit the AAB to Google Play Console
- You can update your app on Play Store forever with the same key

> ⚠️ **IMPORTANT:** If you lose your keystore file, you CANNOT update your app on Play Store. Google Play does not allow changing keys. Back it up in at least 2 places.

---

## 📁 Project structure

```
web-to-apk/
│
├── www/                          ← PUT YOUR WEB APP HERE
│   └── index.html                ← your main HTML page
│
├── .github/
│   └── workflows/
│       ├── build.yml             ← main build pipeline (runs on every push)
│       └── setup-keystore.yml   ← one-time Play Store key generator
│
├── ci/
│   ├── setup_keystore.py        ← handles signing (auto or real key)
│   └── save_secrets.py          ← saves your key as GitHub Secrets
│
├── capacitor.config.json        ← Capacitor settings (app ID, name, webDir)
├── package.json                 ← Node.js dependencies
└── README.md                    ← this file
```

**The only folder you need to touch is `www/`.**
Everything else is handled by the CI pipeline.

---

## ⚙️ Customize your app

### Change app name and ID

Edit `capacitor.config.json`:

```json
{
  "appId": "com.yourname.yourapp",
  "appName": "Your App Name",
  "webDir": "www"
}
```

- **appId** — unique identifier like a domain in reverse (e.g. `com.john.myweather`)
- **appName** — name shown on the phone's home screen

### Change version

Edit `package.json`:

```json
{
  "version": "1.2.0"
}
```

The version code (internal number Android uses) auto-increments with each commit.

### Add Capacitor plugins

Want to access the camera, GPS, notifications, storage, etc.? Add Capacitor plugins:

```bash
npm install @capacitor/camera
npm install @capacitor/geolocation
npm install @capacitor/push-notifications
```

Then use them in your JavaScript. [Full plugin list →](https://capacitorjs.com/docs/plugins)

---

## 🚨 Troubleshooting

<details>
<summary><strong>Build fails — "www/index.html not found"</strong></summary>

Make sure:
- Your main HTML file is named exactly `index.html`
- It is inside the `www/` folder (not in a subfolder inside www)
- You committed the file to GitHub

</details>

<details>
<summary><strong>APK won't install — "App not installed" or "Install blocked"</strong></summary>

On your Android phone:
- Go to **Settings** → **Security** (or **Privacy**)
- Enable **"Install unknown apps"** or **"Unknown sources"**
- On Android 8+: you may need to allow it per-app (e.g. allow your browser or file manager)

</details>

<details>
<summary><strong>App looks bad on phone (text too small or too big)</strong></summary>

Add this to your `www/index.html` inside `<head>`:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
```

</details>

<details>
<summary><strong>My website uses an API — it doesn't work in the app</strong></summary>

If your web app calls an API (fetch, axios, etc.):
- Make sure the API URL uses **https://** not http://
- If your own server: enable CORS headers

If you need to call http:// APIs, edit `capacitor.config.json` and add:
```json
"android": { "allowMixedContent": true }
```

</details>

<details>
<summary><strong>Build takes too long</strong></summary>

- **First build:** ~8-10 minutes (downloads Android build tools, ~500 MB)
- **Repeat builds:** ~4-5 minutes (Gradle is cached)
- **After 7 days without a build:** cache expires, next build is slow again

This is normal. GitHub gives free CI minutes for public repos.

</details>

<details>
<summary><strong>I want to use React / Vue / Angular</strong></summary>

Yes, you can! Just make sure your framework builds into the `www/` folder.

For React (Create React App): change build output to `www/` in `package.json`:
```json
"scripts": {
  "build": "react-scripts build && cp -r build/* www/"
}
```

For Vite: edit `vite.config.js`:
```js
export default { build: { outDir: 'www' } }
```

For Vue CLI:
```js
// vue.config.js
module.exports = { outputDir: 'www' }
```

</details>

---

## 📊 Build artifacts

After every successful build, you get:

| Artifact | Size | Use |
|---|---|---|
| **APK-v1.0.0** | ~1-5 MB | Install directly on Android phone |
| **AAB-v1.0.0** | ~1-5 MB | Upload to Google Play Store |

Artifacts are kept for **30 days**. After that, just push any change to regenerate.

---

## 🤔 Frequently asked questions

**Q: Is this free?**
Yes. GitHub Actions gives 2,000 free minutes/month for public repos. For private repos, 500 minutes/month free.

**Q: Can I make money from apps built with this?**
Yes. The MIT license allows commercial use. You own your app.

**Q: Can I submit to Google Play?**
Yes, but you need to run the **Setup Keystore** workflow first to get a permanent signing key. Then upload the AAB file to [Google Play Console](https://play.google.com/console).

**Q: Does it work with iOS too?**
This repo only builds Android APKs. iOS requires a Mac, Xcode, and an Apple Developer account ($99/year).

**Q: My app needs local storage / camera / GPS — can I use those?**
Yes! Use [Capacitor plugins](https://capacitorjs.com/docs/plugins). Add the npm package, use it in JavaScript. No Java/Kotlin needed.

**Q: Can I use this offline without GitHub?**
Yes, but you need Node.js, Java, and Android SDK installed locally. For beginners, the GitHub Actions approach is much easier.

---

## 🤝 Contributing

Found a bug? Have an improvement idea? Pull requests welcome!

1. Fork this repo
2. Create a branch: `git checkout -b fix/your-fix`
3. Make your changes
4. Push and open a Pull Request

---

## 📄 License

MIT — free to use, modify, and distribute.

---

<div align="center">

Built with ❤️ by [AKIBUZZAMAN AKIB](https://github.com/AKIB473)

**If this helped you, please ⭐ star the repo — it helps others find it!**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6C63FF,100:3B82F6&height=100&section=footer" width="100%"/>

</div>
