# 🚀 Deployment Útmutató - Railway és Vercel

Ez az útmutató lépésről lépésre végigvezet a Fizetési Info Platform telepítésén Railway (backend) és Vercel (frontend) platformokon, **automatizált környezeti változó felismeréssel**.

## 📋 Tartalomjegyzék

1. [Railway Deployment (Backend)](#railway-deployment-backend)
2. [Vercel Deployment (Frontend)](#vercel-deployment-frontend)
3. [Környezeti változók összefoglalója](#környezeti-változók-összefoglalója)
4. [Tesztelés és ellenőrzés](#tesztelés-és-ellenőrzés)

---

## 🚂 Railway Deployment (Backend)

### 1. Előkészületek

Railway automatikusan felismeri és beállítja a környezeti változókat a `railway.json` fájl alapján.

### 2. PostgreSQL és Redis hozzáadása

```bash
# Railway Dashboard-on:
1. Új projekt létrehozása
2. PostgreSQL service hozzáadása (New Service → Database → PostgreSQL)
3. Redis service hozzáadása (New Service → Database → Redis)
```

**✅ Automatikusan beállított változók:**
- `DATABASE_URL` - PostgreSQL kapcsolati URL
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`, `POSTGRES_PORT`
- `REDIS_URL`, `REDIS_HOST`, `REDIS_PORT`
- `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`

### 3. Backend Service Deploy

```bash
# Railway Dashboard-on:
1. "New Service" → "GitHub Repo"
2. Repository kiválasztása
3. Railway automatikusan észleli a railway.json-t
```

### 4. Manuálisan beállítandó változók

Csak ezeket kell beállítani a Railway Dashboard → Variables menüpontban:

#### 🔐 Kötelező biztonsági változók:

```bash
# Generálás terminálban:
openssl rand -hex 32

# Railway-en beállítandó:
SECRET_KEY=<generált-érték>
JWT_SECRET_KEY=<generált-érték>
```

#### 🤖 OpenAI API kulcs (opcionális):

```bash
OPENAI_API_KEY=sk-your-openai-api-key
```

#### 🌐 CORS beállítás:

```bash
# Frissítsd a frontend domain-nel:
CORS_ORIGINS=["https://your-frontend.vercel.app","https://your-backend.railway.app"]
```

### 5. Railway telepítés összefoglalás

✅ **Automatikusan beállítva** (28 változó):
- Összes adatbázis kapcsolat (PostgreSQL, Redis)
- Összes alkalmazás konfiguráció (API, Celery, stb.)
- Összes alapértelmezett érték

❌ **Manuálisan beállítandó** (3-4 változó):
- `SECRET_KEY`
- `JWT_SECRET_KEY`  
- `OPENAI_API_KEY` (opcionális)
- `CORS_ORIGINS` (frontend URL-lel)

---

## 🔷 Vercel Deployment (Frontend)

### 1. Vercel projekt létrehozása

```bash
# Terminálban (vagy Vercel Dashboard-on):
cd frontend
vercel

# Vagy GitHub integration használata
```

### 2. Automatikusan beállított változók

A `vercel.json` már tartalmazza az összes szükséges környezeti változót:

```json
{
  "env": {
    "NEXT_PUBLIC_API_URL": "https://your-backend.railway.app",
    "NEXT_PUBLIC_APP_NAME": "Fizetesi_Info_Platform",
    "NEXT_PUBLIC_APP_ENV": "production",
    "NEXT_PUBLIC_ENABLE_ANALYTICS": "true"
  }
}
```

### 3. Egyetlen módosítás szükséges

**Vercel Dashboard → Settings → Environment Variables:**

```bash
# Frissítsd a Railway backend URL-jét:
NEXT_PUBLIC_API_URL=https://your-backend-name.up.railway.app
```

### 4. Vercel telepítés összefoglalás

✅ **Automatikusan beállítva** (4 változó):
- `NEXT_PUBLIC_APP_NAME`
- `NEXT_PUBLIC_APP_ENV`
- `NEXT_PUBLIC_ENABLE_ANALYTICS`
- `NEXT_PUBLIC_SENTRY_DSN`

❌ **Manuálisan beállítandó** (1 változó):
- `NEXT_PUBLIC_API_URL` (Railway backend URL)

---

## 🔑 Környezeti változók összefoglalója

### Railway Backend - Automatikus változók (railway.json)

| Kategória | Változó | Forrás | Megjegyzés |
|-----------|---------|--------|------------|
| **PostgreSQL** | `DATABASE_URL` | Railway Postgres | ✅ Auto |
| | `POSTGRES_USER` | Railway Postgres | ✅ Auto |
| | `POSTGRES_PASSWORD` | Railway Postgres | ✅ Auto |
| | `POSTGRES_DB` | Railway Postgres | ✅ Auto |
| | `POSTGRES_HOST` | Railway Postgres | ✅ Auto |
| | `POSTGRES_PORT` | Railway Postgres | ✅ Auto |
| **Redis** | `REDIS_URL` | Railway Redis | ✅ Auto |
| | `REDIS_HOST` | Railway Redis | ✅ Auto |
| | `REDIS_PORT` | Railway Redis | ✅ Auto |
| **Celery** | `CELERY_BROKER_URL` | Railway Redis | ✅ Auto |
| | `CELERY_RESULT_BACKEND` | Railway Redis | ✅ Auto |
| **Alkalmazás** | `APP_NAME` | railway.json | ✅ Auto |
| | `APP_ENV` | railway.json | ✅ Auto |
| | `DEBUG` | railway.json | ✅ Auto |
| | `API_HOST` | railway.json | ✅ Auto |
| | `API_PORT` | railway.json | ✅ Auto |
| | `JWT_ALGORITHM` | railway.json | ✅ Auto |
| | `LOG_LEVEL` | railway.json | ✅ Auto |
| | ... (22 további) | railway.json | ✅ Auto |

### Railway Backend - Manuális változók

| Változó | Generálás | Kötelező? |
|---------|-----------|-----------|
| `SECRET_KEY` | `openssl rand -hex 32` | ✅ Igen |
| `JWT_SECRET_KEY` | `openssl rand -hex 32` | ✅ Igen |
| `OPENAI_API_KEY` | OpenAI Dashboard | ❌ Opcionális |
| `CORS_ORIGINS` | Frontend URL | ✅ Igen |

### Vercel Frontend - Automatikus változók (vercel.json)

| Változó | Forrás | Megjegyzés |
|---------|--------|------------|
| `NEXT_PUBLIC_APP_NAME` | vercel.json | ✅ Auto |
| `NEXT_PUBLIC_APP_ENV` | vercel.json | ✅ Auto |
| `NEXT_PUBLIC_ENABLE_ANALYTICS` | vercel.json | ✅ Auto |
| `NEXT_PUBLIC_SENTRY_DSN` | vercel.json | ✅ Auto |

### Vercel Frontend - Manuális változók

| Változó | Érték | Kötelező? |
|---------|-------|-----------|
| `NEXT_PUBLIC_API_URL` | Railway backend URL | ✅ Igen |

---

## 🧪 Tesztelés és ellenőrzés

### Backend ellenőrzés (Railway)

```bash
# Health check
curl https://your-backend.railway.app/health

# Várt válasz:
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production"
}

# API docs
https://your-backend.railway.app/docs
```

### Frontend ellenőrzés (Vercel)

```bash
# Főoldal
https://your-frontend.vercel.app

# Console-ban ellenőrizd:
# - API kapcsolat működik
# - Nincs CORS hiba
# - Environment változók betöltődtek
```

### Környezeti változók ellenőrzése

**Railway-en:**
```bash
# Railway CLI (opcionális)
railway variables

# Vagy Dashboard → Variables
```

**Vercel-en:**
```bash
# Vercel CLI
vercel env ls

# Vagy Dashboard → Settings → Environment Variables
```

---

## 🎯 Gyors telepítési checklist

### Railway Backend
- [ ] PostgreSQL service hozzáadva
- [ ] Redis service hozzáadva
- [ ] `SECRET_KEY` generálva és beállítva
- [ ] `JWT_SECRET_KEY` generálva és beállítva
- [ ] `OPENAI_API_KEY` beállítva (opcionális)
- [ ] `CORS_ORIGINS` frissítve frontend URL-lel
- [ ] Backend deployed és fut
- [ ] Health check működik

### Vercel Frontend
- [ ] Projekt létrehozva
- [ ] `NEXT_PUBLIC_API_URL` beállítva Railway URL-lel
- [ ] Frontend deployed és fut
- [ ] API kapcsolat működik
- [ ] Nincs CORS hiba

---

## 💡 Tippek és trükkök

### 1. Secret kulcsok generálása

```bash
# Biztonságos SECRET_KEY generálás
openssl rand -hex 32

# Vagy Python-nal:
python -c "import secrets; print(secrets.token_hex(32))"

# Vagy Node.js-sel:
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### 2. CORS beállítás több domain-hez

```bash
# Railway Variables-ban:
CORS_ORIGINS=["https://app.vercel.app","https://www.yourdomain.com","https://api.yourdomain.com"]
```

### 3. Railway CLI használata (opcionális)

```bash
# Telepítés
npm i -g @railway/cli

# Login
railway login

# Project link
railway link

# Variables listázása
railway variables

# Deploy
railway up
```

### 4. Environment-specifikus konfigurációk

Railway automatikusan kezeli a `production` environment-et a `railway.json` alapján. További environment-ek:

```json
{
  "environments": {
    "staging": {
      "variables": {
        "APP_ENV": "staging",
        "DEBUG": "True"
      }
    }
  }
}
```

---

## 🆘 Hibaelhárítás

### "Database connection error"

```bash
# Ellenőrizd:
1. PostgreSQL service fut-e Railway-en
2. DATABASE_URL helyesen van-e beállítva (automatikus)
3. Backend service "Networking" beállítások

# Railway logs:
railway logs
```

### "CORS error" a frontend-en

```bash
# Ellenőrizd:
1. CORS_ORIGINS tartalmazza a frontend URL-t
2. Protocol (https://) helyesen van-e
3. Nincs trailing slash (/)

# Helyes formátum:
CORS_ORIGINS=["https://your-app.vercel.app"]
```

### "API connection failed" Vercel-en

```bash
# Ellenőrizd:
1. NEXT_PUBLIC_API_URL helyesen van-e beállítva
2. Railway backend fut és elérhető
3. Network tab-ben látszik-e a request

# Vercel build logs:
vercel logs
```

---

## 📚 További információk

- [Railway dokumentáció](https://docs.railway.app)
- [Vercel dokumentáció](https://vercel.com/docs)
- [FastAPI deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js environment variables](https://nextjs.org/docs/basic-features/environment-variables)

---

## ✅ Sikeres telepítés után

Ha minden működik:
1. ⭐ Mentsd el a SECRET_KEY-eket biztonságosan
2. 📝 Dokumentáld a deployment URL-eket
3. 🔒 Állíts be monitoring-ot (Sentry, stb.)
4. 🚀 Kezdd el használni az alkalmazást!

---

**Problémád van?** Nézd meg a projekt dokumentációját vagy nyiss egy issue-t a GitHub-on.
