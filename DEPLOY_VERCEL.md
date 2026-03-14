# 🚀 Deploy MVS AQUA to Vercel — Step by Step

## What you need
- GitHub account (free) → https://github.com
- Vercel account (free) → https://vercel.com
- That's it!

---

## STEP 1 — Push code to GitHub

### 1a. Download and install Git
https://git-scm.com/download/win

### 1b. Open terminal in the mvs_aqua_final folder
Right-click folder → "Open in Terminal"

### 1c. Run these commands one by one:
```
git init
git add .
git commit -m "MVS AQUA website"
```

### 1d. Create GitHub repo
1. Go to https://github.com/new
2. Name it: `mvs-aqua`
3. Keep it Public
4. Click "Create repository"

### 1e. Push to GitHub (copy commands from GitHub page)
```
git remote add origin https://github.com/YOURUSERNAME/mvs-aqua.git
git branch -M main
git push -u origin main
```

---

## STEP 2 — Deploy on Vercel

1. Go to https://vercel.com and sign up with GitHub
2. Click **"Add New Project"**
3. Click **"Import"** next to your `mvs-aqua` repo
4. Vercel auto-detects settings — just click **"Deploy"**
5. Wait ~2 minutes...
6. ✅ Your site is LIVE at `https://mvs-aqua.vercel.app`

---

## STEP 3 — Set Environment Variables on Vercel

In Vercel Dashboard → Your Project → Settings → Environment Variables

Add these:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `mvs-aqua-super-secret-key-change-this-2025` |
| `DEBUG` | `False` |
| `ADMIN_WHATSAPP` | `919490255775` |
| `ALLOWED_HOSTS` | `*.vercel.app` |

Click **Save** → Then **Redeploy**

---

## STEP 4 — Create admin account on live site

After deploy, open Vercel terminal or run locally:
```
python manage.py createsuperuser
```
Or seed_data.py already creates: admin / mvsaqua2025

---

## ⚠️ Important Notes

1. **SQLite on Vercel** — Works for testing but Vercel is serverless
   (each request may use a fresh container, so cart/sessions may reset).
   For permanent data, upgrade to PostgreSQL (see below).

2. **Free PostgreSQL** — Add Vercel Postgres:
   - Vercel Dashboard → Storage → Create Database → Postgres
   - Copy DATABASE_URL → Add to Environment Variables
   - That's it! Permanent database with free tier.

3. **Media uploads** — Product images uploaded via admin won't persist
   on Vercel (no permanent disk). Use Cloudinary or AWS S3 for images.

---

## 🎯 Recommended Setup for Live Store

For a real live store, use this free stack:

| Service | Purpose | Cost |
|---------|---------|------|
| Vercel | Website hosting | FREE |
| Vercel Postgres | Database | FREE (256MB) |
| Cloudinary | Product images | FREE (25GB) |
| GitHub | Code storage | FREE |

---

## URLs after deployment
- Store: `https://mvs-aqua.vercel.app/`
- Admin: `https://mvs-aqua.vercel.app/dashboard/login/`
- Login: `admin` / `mvsaqua2025`

