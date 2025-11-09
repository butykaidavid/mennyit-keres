# 🚀 LEGEGYSZERŰBB DEPLOY - Railway.app

## ⚡ 15 perc alatt élesben, számítógép nélkül!

---

## 🎯 Miért Railway?

✅ **Teljesen ingyenes kezdéshez** ($5 credit, ~500 óra futás)  
✅ **Nincs hitelkártya** szükséges  
✅ **Automatikus deploy** minden git push után  
✅ **PostgreSQL + Redis** beépítve  
✅ **HTTPS** automatikusan  
✅ **Egyetlen platform** az egész projekthez  

---

## 📝 Lépésről Lépésre (15 perc)

### 1️⃣ **GitHub Repo** (5 perc)

Ha még nincs:

```bash
# Terminálban:
git init
git add .
git commit -m "Initial commit"
git branch -M main

# GitHub-on: Create new repository
# Majd:
git remote add origin https://github.com/your-username/fizetesek.git
git push -u origin main
```

**Vagy GitHub Desktop / VS Code UI-on keresztül is!**

---

### 2️⃣ **Railway Regisztráció** (1 perc)

1. Menj a **https://railway.app**
2. Kattints: **"Login with GitHub"**
3. Authorize Railway (1 kattintás)
4. ✅ Kész! Be vagy jelentkezve

---

### 3️⃣ **Projekt Létrehozás** (5 perc)

#### A) Új Projekt

1. Dashboard → **"New Project"**
2. Válaszd: **"Deploy from GitHub repo"**
3. Keresd meg és válaszd ki: **`fizetesek`** repo
4. Railway automatikusan észleli a Dockerfile-okat

#### B) PostgreSQL Hozzáadás

1. A projekt dashboardon: **"+ New"**
2. **"Database"** → **"Add PostgreSQL"**
3. ✅ Automatikus setup!

#### C) Redis Hozzáadás

1. Ismét: **"+ New"**
2. **"Database"** → **"Add Redis"**
3. ✅ Automatikus setup!

---

### 4️⃣ **Backend Konfiguráció** (3 perc)

1. Kattints a **Backend** service-re
2. **"Variables"** tab
3. Add hozzá:

```env
DATABASE_URL       = ${{Postgres.DATABASE_URL}}
REDIS_URL          = ${{Redis.REDIS_URL}}
OPENAI_API_KEY     = sk-your-actual-openai-key-here
SECRET_KEY         = generate-a-random-string-here
PORT               = 8000
CORS_ORIGINS       = *
```

**SECRET_KEY generálás:**
- Menj ide: https://generate-secret.vercel.app/32
- Vagy használd: `your-super-secret-key-change-this`

4. **"Settings"** tab → **"Networking"**
5. **"Generate Domain"** → Kapsz egy URL-t pl:
   ```
   fizetesek-backend-production.up.railway.app
   ```

---

### 5️⃣ **Scraper Konfiguráció** (1 perc)

1. Kattints a **Scraper** service-re
2. **"Variables"** tab
3. Ugyanazokat az environment variable-okat add hozzá mint a Backend-nél

---

### 6️⃣ **Deploy!** (Automatikus)

✅ Railway **automatikusan deploy-ol**!

**Nézd meg:**
- **"Deployments"** tab → Latest deployment
- **"Logs"** tab → Build és runtime logs
- Ha minden zöld → Sikeres! 🎉

---

### 7️⃣ **Ellenőrzés** (1 perc)

Nyisd meg böngészőben:

```
https://your-backend-name.up.railway.app/health
```

Látnod kell:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production"
}
```

**API Dokumentáció:**
```
https://your-backend-name.up.railway.app/docs
```

✅ **KÉSZ! Az API fut!** 🎉

---

## 🎨 Frontend Deploy (Vercel) - Opcionális

### 1️⃣ **Vercel Regisztráció**

1. Menj a **https://vercel.com**
2. **"Sign Up with GitHub"**
3. ✅ Kész!

### 2️⃣ **Deploy**

1. **"Add New..."** → **"Project"**
2. **"Import Git Repository"** → Válaszd a `fizetesek` repo-t
3. **"Root Directory"**: `frontend`
4. **"Framework Preset"**: Next.js (auto-detect)
5. **"Environment Variables"**:
   ```
   NEXT_PUBLIC_API_URL = https://your-backend.up.railway.app
   ```
6. **"Deploy"** → 2 perc múlva kész!

Frontend URL:
```
https://fizetesek.vercel.app
```

---

## 📊 Költségek

### Railway
- **$5 ingyenes credit** havonta
- ~**500 óra futás** (kis projektnek elég)
- Ha elfogy → $0.000463/GB-sec ($10-20/hó)

### Vercel
- **Frontend 100% ingyenes** (hobby projekt)
- Korlátlan bandwidth

**Összesen: $0-5/hó** kezdéshez!

---

## 🔄 Automatikus Deploy

**Minden `git push` után automatikus deploy!**

```bash
# Változtatsz valamit:
git add .
git commit -m "Update scraper"
git push

# Railway automatikusan:
# 1. Észleli a változást
# 2. Build-eli az új verziót
# 3. Deploy-olja
# 4. Kész! 🎉
```

---

## 🔧 Hasznos Railway Funkciók

### Logs nézés
- Dashboard → Service → **"Logs"** tab
- Real-time logs láthatók

### Database kezelés
- PostgreSQL service → **"Data"** tab
- SQL query futtatás: **"Query"** tab

### Metrics
- Service → **"Metrics"** tab
- CPU, Memory, Network usage

### Rollback
- **"Deployments"** tab → Old deployment → **"Rollback"**

---

## ❓ Problémamegoldás

### Build Fails

**Logs ellenőrzés:**
1. Service → **"Deployments"**
2. Failed deployment → Click
3. Nézd meg a **"Build Logs"**

**Gyakori problémák:**
- Missing `Dockerfile` → ellenőrizd a repo-t
- Wrong directory → Settings → **"Root Directory"** = `backend` vagy `scraper`
- Missing dependencies → ellenőrizd a `requirements.txt`-t

### Database Connection Error

**Ellenőrizd:**
1. Backend Variables → `DATABASE_URL` létezik?
2. PostgreSQL service fut?
3. Logs tab → nézzed meg a pontos error üzenetet

### Application Timeout

**Lehetséges okok:**
- Cold start (első kérés lassú)
- Memory limit (növeld: Settings → **"Resources"**)
- Database nem elérhető

---

## 🎯 Következő Lépések

1. ✅ **Tesztelés**
   - API végpontok kipróbálása (`/docs`)
   - Scraping indítás (`POST /api/admin/scrape/trigger`)

2. ✅ **Custom Domain** (opcionális)
   - Settings → Networking → **"Custom Domain"**
   - Add: `fizetesek.hu`
   - DNS update (CNAME)

3. ✅ **Monitoring**
   - Sentry.io (error tracking)
   - Uptime Robot (uptime monitoring)

4. ✅ **Scaling**
   - Ha túlléped az ingyenes limitet
   - Settings → **"Resources"** → Increase

---

## 💡 Pro Tips

1. **Free tier hack:** 2 Railway account = $10/hó credit 😉
2. **Development vs Production:** Külön Railway project
3. **Secrets security:** Soha ne commitold a .env-t!
4. **Regular backups:** Database export hetente
5. **Monitoring alerts:** Állíts be email alert-et ha down

---

## 📞 Segítség

- **Railway Docs:** https://docs.railway.app
- **Railway Discord:** https://discord.gg/railway (nagyon aktív!)
- **Project Issues:** GitHub Issues tab

---

## ✅ Checklist

- [ ] GitHub repo létrehozva és pusholva
- [ ] Railway.app regisztráció
- [ ] Projekt létrehozva Railway-en
- [ ] PostgreSQL hozzáadva
- [ ] Redis hozzáadva
- [ ] Backend environment variables beállítva
- [ ] Scraper environment variables beállítva
- [ ] Backend domain generálva
- [ ] `/health` endpoint működik
- [ ] `/docs` endpoint elérhető
- [ ] (Opcionális) Frontend Vercel-en

---

## 🎉 Gratulálok!

**A projekted élesben fut a felhőben!** ☁️

Nincs szükség saját szerverre vagy számítógépre, minden a cloud-ban fut!

Most már csak fejleszd tovább és push-old GitHub-ra → automatikus deploy! 🚀

---

**Létrehozva:** 2025-11-09  
**Platform:** Railway.app  
**Költség:** $0-5/hó  

---

**További információ:** [CLOUD_DEPLOYMENT.md](docs/CLOUD_DEPLOYMENT.md)
