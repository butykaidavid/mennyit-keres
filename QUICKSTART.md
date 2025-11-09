# 🚀 Gyors Kezdés - Fizetési Információs Platform

Ez a útmutató segít 10 perc alatt elindítani a projektet.

## ⚡ Gyors indítás Docker-rel (Ajánlott)

### 1. Előfeltételek
- [Docker](https://docs.docker.com/get-docker/) telepítve
- [Docker Compose](https://docs.docker.com/compose/install/) telepítve
- Git telepítve

### 2. Projekt letöltése
```bash
git clone https://github.com/your-org/fizetesek.git
cd fizetesek
```

### 3. Környezeti változók
```bash
cp .env.example .env
```

**Szerkeszd a `.env` fájlt és add meg:**
- `OPENAI_API_KEY` - OpenAI API kulcs (https://platform.openai.com/)
- `SECRET_KEY` - Véletlenszerű string (pl: `openssl rand -hex 32`)

### 4. Indítás
```bash
docker-compose up -d
```

### 5. Adatbázis inicializálás
```bash
docker-compose exec backend alembic upgrade head
```

### 6. Ellenőrzés

**Backend API:**
```bash
curl http://localhost:8000/health
```
Vagy nyisd meg böngészőben: http://localhost:8000/docs

**Frontend:**
http://localhost:3000

**Adatbázis:**
```bash
docker-compose exec db psql -U admin -d fizetesek
```

---

## 🔧 Manuális indítás (Fejlesztéshez)

### Backend

```bash
cd backend

# Python környezet
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Függőségek
pip install -r requirements.txt

# Environment
cp ../.env.example .env
# Szerkeszd a .env fájlt!

# PostgreSQL és Redis indítása külön
# Vagy használj Docker-t csak ezekhez:
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:14
docker run -d -p 6379:6379 redis:7-alpine

# Adatbázis setup
alembic upgrade head

# Backend indítás
uvicorn main:app --reload
```

Backend elérhető: http://localhost:8000

### Scraper

```bash
cd scraper

# Virtual environment
python -m venv venv
source venv/bin/activate

# Függőségek
pip install -r requirements.txt

# Teszt futtatás (1 oldal profession.hu-ról)
python main.py profession 1
```

### Frontend

```bash
cd frontend

# Node packages
npm install

# Environment
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Development mode
npm run dev
```

Frontend elérhető: http://localhost:3000

---

## 📝 Első lépések

### 1. Scraping indítása

**API-n keresztül:**
```bash
curl -X POST http://localhost:8000/api/admin/scrape/trigger \
  -H "Content-Type: application/json" \
  -d '{"portal": "profession"}'
```

**Közvetlenül:**
```bash
cd scraper
python main.py profession 2  # 2 oldal scraping
```

### 2. API tesztelés

**Swagger UI:** http://localhost:8000/docs

**Példa API hívások:**

```bash
# Összes állás
curl http://localhost:8000/api/jobs

# Keresés
curl http://localhost:8000/api/jobs/search?q=python

# Kategóriák
curl http://localhost:8000/api/categories

# Statisztikák
curl http://localhost:8000/api/statistics/trending
```

### 3. Adatok feltöltése (Teszt adatok)

```bash
cd database
docker-compose exec db psql -U admin -d fizetesek < seeds/test_data.sql
```

---

## 🎯 Következő lépések

1. **Dokumentáció áttekintése:**
   - [README.md](README.md) - Teljes áttekintés
   - [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) - Részletes terv
   - [docs/API.md](docs/API.md) - API dokumentáció

2. **Fejlesztés:**
   - Backend: `backend/app/` mappában
   - Frontend: `frontend/src/` mappában
   - Scraper: `scraper/spiders/` mappában

3. **Tesztelés:**
   ```bash
   # Backend tesztek
   cd backend && pytest
   
   # Frontend tesztek
   cd frontend && npm test
   ```

4. **Production deployment:**
   - [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 🐛 Gyakori problémák

### Backend nem indul

**Probléma:** `ModuleNotFoundError`
```bash
# Függőségek újratelepítése
pip install -r requirements.txt --upgrade
```

**Probléma:** Database connection error
```bash
# Ellenőrzd a DATABASE_URL-t a .env-ben
# PostgreSQL fut?
docker-compose ps db
```

### Scraper hibák

**Probléma:** `No module named 'fake_useragent'`
```bash
cd scraper
pip install -r requirements.txt
```

**Probléma:** Rate limiting / Blocked
- Csökkentsd a `max_pages` értéket
- Növeld a delay-t (`REQUEST_DELAY_MIN` a .env-ben)

### Frontend build hiba

**Probléma:** `Cannot find module`
```bash
rm -rf node_modules package-lock.json
npm install
```

---

## 📊 Projekt áttekintés

```
Projekt Struktúra:
.
├── backend/          → FastAPI backend (Port 8000)
├── frontend/         → Next.js frontend (Port 3000)
├── scraper/          → Web scraping modul
├── database/         → DB migrations & seeds
├── docs/             → Dokumentáció
└── docker-compose.yml → Docker orchestration
```

**Technológiák:**
- **Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL
- **Scraper:** BeautifulSoup, Selenium, Scrapy
- **AI:** OpenAI API, LangChain
- **Frontend:** React, Next.js, TailwindCSS
- **Cache:** Redis
- **Queue:** Celery

---

## 🤝 Segítség

**Dokumentáció:** [README.md](README.md)

**Issues:** GitHub Issues

**Email:** dev@fizetesek.hu

---

## ✅ Checklist

- [ ] Docker és Docker Compose telepítve
- [ ] Git repo klónozva
- [ ] `.env` fájl létrehozva és kitöltve
- [ ] `docker-compose up -d` futtatva
- [ ] Backend health check OK (http://localhost:8000/health)
- [ ] Frontend betölt (http://localhost:3000)
- [ ] API docs elérhető (http://localhost:8000/docs)
- [ ] Teszt scraping futtatva

---

**Készen állsz a fejlesztésre! 🎉**

Utolsó frissítés: 2025-11-09
