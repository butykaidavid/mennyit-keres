# ☁️ Cloud Deployment - Számítógép Nélküli Futtatás

## 🎯 Áttekintés

Ez az útmutató bemutatja, hogyan futtathatod a projektet különböző cloud platformokon, **akár számítógép nélkül**, csak böngészőből!

---

## 🚀 Ajánlott Platformok

### 1. 🔷 **Railway.app** (⭐ LEGJOBB - Teljes Stack)

**Előnyök:**
- ✅ Ingyenes tier ($5 credit/hónap)
- ✅ PostgreSQL, Redis beépítve
- ✅ Docker support
- ✅ Automatikus HTTPS
- ✅ GitHub integráció (push = auto deploy)
- ✅ Nincs hitelkártya szükséges kezdéshez

**Deployment lépések:**

#### A) GitHub-ról (ajánlott)

1. **Regisztráció**
   - Menj a https://railway.app
   - Sign up with GitHub

2. **Új projekt**
   - "New Project" gomb
   - "Deploy from GitHub repo"
   - Válaszd ki a repot

3. **Services hozzáadása**
   ```
   + New Service
   → Database → PostgreSQL (automatikus)
   → Database → Redis (automatikus)
   → GitHub Repo → Backend (main.py)
   → GitHub Repo → Scraper
   ```

4. **Environment Variables**
   - Backend service → Variables tab
   - Add meg:
   ```
   DATABASE_URL=${POSTGRESQL_URL}
   REDIS_URL=${REDIS_URL}
   OPENAI_API_KEY=your-key
   SECRET_KEY=your-secret
   PORT=8000
   ```

5. **Deploy**
   - Automatikus minden push után
   - URL: `your-app.railway.app`

**Költségek:** $5 ingyenes credit → ~500 óra futás

---

### 2. 🔷 **Render.com** (Ingyenes Backend + DB)

**Előnyök:**
- ✅ Teljesen ingyenes tier
- ✅ PostgreSQL ingyen
- ✅ Docker support
- ✅ Automatikus SSL
- ✅ GitHub deploy

**Deployment lépések:**

1. **Backend Deploy**
   - https://render.com → Sign up with GitHub
   - "New +" → "Web Service"
   - Connect GitHub repo
   - Settings:
     ```
     Name: fizetesek-backend
     Environment: Docker
     Docker Command: (empty, uses Dockerfile)
     Plan: Free
     ```

2. **PostgreSQL**
   - "New +" → "PostgreSQL"
   - Name: fizetesek-db
   - Plan: Free
   - Copy "Internal Database URL"

3. **Environment Variables**
   ```
   DATABASE_URL=<internal-db-url>
   OPENAI_API_KEY=your-key
   SECRET_KEY=your-secret
   REDIS_URL=<redis-url-from-upstash>
   ```

4. **Redis (Upstash)**
   - https://upstash.com (ingyenes Redis)
   - Create database
   - Copy REST URL

**Limitációk (Free tier):**
- Backend: 750 óra/hó
- Database: 1GB storage
- Inaktivitás után leáll (cold start)

---

### 3. ⚡ **Vercel** (Frontend) + **Supabase** (Backend)

**Legjobb Frontend-hez!**

#### Vercel (Frontend)

1. **Deploy Next.js**
   - https://vercel.com → Sign up with GitHub
   - "Add New Project"
   - Import GitHub repo
   - Root Directory: `frontend`
   - Framework: Next.js (auto-detect)
   - Deploy!

2. **Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=<your-backend-url>
   ```

**100% ingyenes frontend hosting!**

#### Supabase (Backend adatbázis)

1. **Projekt létrehozás**
   - https://supabase.com → Start your project
   - Create organization
   - New project

2. **Database**
   - Automatikus PostgreSQL
   - SQL Editor-ban futtasd az `init.sql` scriptet

3. **API**
   - Project Settings → API
   - Copy `URL` és `anon public key`

**Ingyenes tier:** 500MB database, 2GB bandwidth

---

### 4. 🐳 **Google Cloud Run** (Serverless Docker)

**Előnyök:**
- ✅ Pay-as-you-go (ingyenes limit)
- ✅ Auto-scaling
- ✅ Docker support

**GitHub Actions Deploy:**

1. **Google Cloud Setup**
   - https://console.cloud.google.com
   - Create project
   - Enable Cloud Run API

2. **.github/workflows/deploy-cloudrun.yml**
   ```yaml
   name: Deploy to Cloud Run

   on:
     push:
       branches: [main]

   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         
         - name: Setup Cloud SDK
           uses: google-github-actions/setup-gcloud@v0
           with:
             service_account_key: ${{ secrets.GCP_SA_KEY }}
             project_id: ${{ secrets.GCP_PROJECT_ID }}
         
         - name: Build and Push
           run: |
             gcloud builds submit --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/fizetesek-backend ./backend
         
         - name: Deploy
           run: |
             gcloud run deploy fizetesek-backend \
               --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/fizetesek-backend \
               --platform managed \
               --region europe-west1 \
               --allow-unauthenticated
   ```

3. **Database** - Cloud SQL vagy Supabase

**Költség:** ~$0-5/hó (kis forgalom esetén)

---

### 5. 🟦 **Azure Container Apps**

**Microsoft Azure serverless containers**

1. **Azure Portal**
   - https://portal.azure.com
   - Create Resource → Container Apps

2. **GitHub Actions**
   ```yaml
   - name: Deploy to Azure
     uses: azure/container-apps-deploy-action@v1
     with:
       containerAppName: fizetesek-backend
       resourceGroup: fizetesek-rg
       imageToDeploy: ${{ secrets.REGISTRY }}/backend:latest
   ```

**Ingyenes tier:** 180,000 vCPU-seconds/hó

---

## 📊 Költség Összehasonlítás

| Platform | Backend | Database | Redis | Összesen/hó |
|----------|---------|----------|-------|-------------|
| **Railway** | $5 credit | Included | Included | **$0-5** |
| **Render** | Free (750h) | Free (1GB) | Upstash Free | **$0** |
| **Vercel + Supabase** | Supabase Free | Free (500MB) | - | **$0** |
| **Google Cloud Run** | Pay-as-go | Cloud SQL $10 | - | **$10-20** |
| **Heroku** | $7/dyno | $9/db | $15/redis | **$31** |

---

## 🎯 Ajánlás Felhasználási Eset Szerint

### 🆓 **Ingyenes / Hobby projekt**
→ **Railway** vagy **Render** + **Upstash Redis**

### 💼 **Prototípus / MVP**
→ **Vercel (frontend)** + **Railway (backend)**

### 🏢 **Production / Startup**
→ **Google Cloud Run** vagy **AWS ECS**

### 🚀 **Enterprise**
→ **Kubernetes** (GKE, EKS, AKS)

---

## 📱 Teljes Stack Deploy - Railway.app (Részletes)

### Lépésről lépésre (10 perc):

#### 1. **GitHub Repo előkészítés**
   ```bash
   # Ha még nincs GitHub repo:
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/your-username/fizetesek.git
   git push -u origin main
   ```

#### 2. **Railway.app regisztráció**
   - Menj a https://railway.app
   - "Login with GitHub"
   - Authorize Railway

#### 3. **Új projekt létrehozás**
   - Dashboard → "New Project"
   - "Deploy from GitHub repo"
   - Select repository: `fizetesek`
   - Railway automatikusan felismeri a `docker-compose.yml`-t

#### 4. **Services konfigurálás**

   **A) PostgreSQL**
   - "+ New" → "Database" → "Add PostgreSQL"
   - Automatikusan generál `DATABASE_URL`-t

   **B) Redis**
   - "+ New" → "Database" → "Add Redis"
   - Automatikusan generál `REDIS_URL`-t

   **C) Backend**
   - "+ New" → "GitHub Repo"
   - Root directory: `backend`
   - Settings → Variables:
     ```
     DATABASE_URL: ${{Postgres.DATABASE_URL}}
     REDIS_URL: ${{Redis.REDIS_URL}}
     OPENAI_API_KEY: your-openai-key
     SECRET_KEY: your-secret-key
     PORT: 8000
     ```
   - Settings → Networking:
     - Generate Domain
     - Pl: `fizetesek-backend-production.up.railway.app`

   **D) Scraper**
   - "+ New" → "GitHub Repo"
   - Root directory: `scraper`
   - Environment variables: ugyanazok mint backend

#### 5. **Deploy!**
   - Railway automatikusan deploy-ol
   - Logs tab: nézd meg a deployment progresst
   - Deployments tab: history

#### 6. **Ellenőrzés**
   ```bash
   curl https://your-backend.up.railway.app/health
   # → {"status": "healthy"}

   curl https://your-backend.up.railway.app/docs
   # → Swagger UI
   ```

#### 7. **Frontend (Vercel)**
   - https://vercel.com
   - "New Project" → Import Git repo
   - Root Directory: `frontend`
   - Environment Variables:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
     ```
   - Deploy!

---

## 🔄 CI/CD - Automatikus Deploy

### Railway (Automatikus)
✅ Minden `git push` után automatikusan deploy-ol!

### GitHub Actions + Cloud Platform

**.github/workflows/deploy.yml**
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Railway
        run: |
          npm i -g @railway/cli
          railway login --browserless
          railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

---

## 🌍 Custom Domain

### Railway
1. Settings → Networking → Custom Domain
2. Add domain: `fizetesek.hu`
3. DNS settings:
   ```
   CNAME fizetesek.hu → your-app.up.railway.app
   ```
4. SSL automatikus (Let's Encrypt)

### Vercel
1. Project Settings → Domains
2. Add domain: `fizetesek.hu`
3. Update DNS:
   ```
   CNAME www → cname.vercel-dns.com
   A @ → 76.76.21.21
   ```

---

## 🔐 Secrets Management

### Railway
- Dashboard → Variables → Add Variable
- Reference: `${{OPENAI_API_KEY}}`

### Vercel
- Project Settings → Environment Variables
- Add all secrets

### GitHub Actions
- Repo Settings → Secrets → New repository secret

---

## 📊 Monitoring

### Railway
- Built-in metrics (CPU, Memory, Network)
- Logs real-time

### Sentry (Error Tracking)
```python
# backend/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    environment="production"
)
```

### Uptime Monitoring
- https://uptimerobot.com (ingyenes)
- Check: `https://your-backend.up.railway.app/health`
- Alert: email/SMS ha down

---

## 💡 Pro Tips

1. **Use Railway for everything initially** (legegyszerűbb)
2. **Frontend always on Vercel** (ingyenes, gyors)
3. **Database backups** - Railway auto-backup vagy manual export
4. **Environment-specific configs** - dev/staging/prod
5. **Secrets rotation** - változtasd rendszeresen
6. **Monitoring** - állíts be Sentry-t és Uptime Robot-ot
7. **Budget alerts** - állíts be spending limit-et

---

## ❓ Gyakori Problémák

### "Out of memory"
→ Növeld a RAM limitet vagy optimalizálj

### "Database connection failed"
→ Ellenőrizd a `DATABASE_URL` environment variable-t

### "Cold start" (Render free tier)
→ Első kérés lassú (15-30s), normális ingyenes tier-en

### "Build failed"
→ Ellenőrizd a `Dockerfile`-t és a build logs-ot

---

## 🎓 Következő Lépések

1. ✅ Deploy-old Railway-re (15 perc)
2. ✅ Frontend Vercel-re (5 perc)
3. ✅ Custom domain beállítás (opcionális)
4. ✅ Monitoring setup (Sentry, Uptime Robot)
5. ✅ Backup stratégia (database exports)

---

## 📞 További Segítség

- **Railway Discord:** https://discord.gg/railway
- **Render Community:** https://community.render.com
- **Vercel Discord:** https://vercel.com/discord
- **Project Docs:** [README.md](../README.md)

---

**Utolsó frissítés:** 2025-11-09
