# Magyar Fizetési Információs Platform

## 📋 Projekt Leírás

Ez a platform automatikusan gyűjti és elemzi a magyar munkaerőpiacon elérhető fizetési információkat különböző szakmákhoz. AI és scraping technológiák kombinálásával valós idejű és pontos kereseti adatokat szolgáltat.

## 🎯 Célok

- **Magyar munkaerőpiac** fizetési adatainak központosítása
- **Valós idejű adatok** gyűjtése állásportálokról
- **AI-alapú elemzés** és adatfeldolgozás
- **Felhasználóbarát keresés** szakmák és készségek szerint
- **Statisztikai elemzések** és trendek megjelenítése

## 🏗️ Architektúra

### Backend (FastAPI)
- RESTful API
- Adatbázis kezelés
- Authentikáció és jogosultságkezelés
- Scraping feladatok ütemezése

### Scraping Modul
- Célpontok: profession.hu, jobs.hu, cvonline.hu, linkedin.com/jobs
- BeautifulSoup és Scrapy alapú
- Selenium dinamikus tartalmakhoz
- Rate limiting és rotating proxies

### AI Modul
- Adatok tisztítása és normalizálása
- Munkakörök kategorizálása
- Fizetési tartományok becslése
- Kereseti trendek előrejelzése

### Frontend (React/Next.js)
- Modern, responsive UI
- Keresési és szűrési lehetőségek
- Interaktív grafikonok és statisztikák
- Admin dashboard

### Adatbázis (PostgreSQL)
- Strukturált adattárolás
- Indexelt keresés
- Historikus adatok követése

## 📁 Projekt Struktúra

```
.
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/         # Adatbázis modellek
│   │   ├── routers/        # API végpontok
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Segédfüggvények
│   │   └── config/         # Konfigurációk
│   ├── requirements.txt
│   └── main.py
│
├── scraper/                # Scraping modul
│   ├── spiders/           # Scraper osztályok
│   ├── utils/             # Scraping segédeszközök
│   ├── models/            # Adat modellek
│   └── requirements.txt
│
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/   # React komponensek
│   │   ├── pages/        # Oldalak
│   │   ├── services/     # API kliens
│   │   └── utils/        # Frontend utils
│   └── package.json
│
├── database/              # Adatbázis
│   ├── migrations/       # DB migrációk
│   └── seeds/            # Kezdő adatok
│
├── docs/                  # Dokumentáció
│   ├── api.md            # API dokumentáció
│   ├── scraping.md       # Scraping útmutató
│   └── deployment.md     # Deployment útmutató
│
├── docker-compose.yml     # Docker orchestration
└── README.md
```

## 🚀 Telepítés és Futtatás

### Előfeltételek
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Docker (opcionális)

### Backend indítása
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend indítása
```bash
cd frontend
npm install
npm run dev
```

### Docker indítás
```bash
docker-compose up -d
```

## 🔧 Konfiguráció

Környezeti változók `.env` fájlban:

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/fizetesek

# API Keys
OPENAI_API_KEY=your_openai_key
SCRAPING_API_KEY=your_proxy_key

# Security
SECRET_KEY=your_secret_key
CORS_ORIGINS=http://localhost:3000

# Scraping
SCRAPE_INTERVAL=3600  # másodpercek
USER_AGENT=Mozilla/5.0...
```

## 📊 Funkcionalitás

### Fő Funkciók
1. **Munkakör keresés** - Fizetési információk megjelenítése szakmánként
2. **Szűrés** - Tapasztalat, helyszín, iparág szerint
3. **Összehasonlítás** - Több munkakör összehasonlítása
4. **Trendek** - Historikus fizetési trendek
5. **Exportálás** - Adatok letöltése CSV/PDF formátumban

### Admin Funkciók
1. Scraping feladatok kezelése
2. Adatok validálása és szerkesztése
3. Statisztikák és jelentések
4. Felhasználók kezelése

## 🔐 Biztonság

- JWT alapú authentikáció
- Rate limiting az API-n
- CORS védelem
- SQL injection védelem (ORM használat)
- XSS védelem
- Érzékeny adatok titkosítása

## 📈 Roadmap

### Phase 1 (Alapok) - 4 hét
- ✅ Projekt struktúra
- ⏳ Backend API alapok
- ⏳ Alapvető scraping
- ⏳ Egyszerű frontend

### Phase 2 (AI Integráció) - 3 hét
- ⏳ OpenAI integráció
- ⏳ Adatok normalizálása
- ⏳ Kategorizálás

### Phase 3 (Finomítás) - 3 hét
- ⏳ Fejlett szűrők
- ⏳ Grafikonok és vizualizációk
- ⏳ Admin panel

### Phase 4 (Production) - 2 hét
- ⏳ Tesztelés
- ⏳ Deployment
- ⏳ Monitoring

## 🛠️ Technológiai Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **Celery** - Aszinkron feladatok
- **Redis** - Cache és queue

### Scraping
- **Scrapy** - Web scraping framework
- **BeautifulSoup4** - HTML parsing
- **Selenium** - Dinamikus tartalmak
- **Playwright** - Modern web automation

### AI/ML
- **OpenAI API** - GPT modellek
- **LangChain** - LLM orchestration
- **Pandas** - Adatelemzés
- **scikit-learn** - Gépi tanulás

### Frontend
- **React/Next.js** - Frontend framework
- **TailwindCSS** - Styling
- **Chart.js / Recharts** - Grafikonok
- **Axios** - HTTP kliens

### DevOps
- **Docker** - Konténerizáció
- **GitHub Actions** - CI/CD
- **Nginx** - Reverse proxy
- **PostgreSQL** - Adatbázis

## 🤝 Közreműködés

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## 📝 Licensz

MIT License

## 👥 Csapat

- Backend Developer
- Frontend Developer
- Data Engineer
- DevOps Engineer

## 📞 Kapcsolat

- Email: info@fizetesek.hu
- Website: https://fizetesek.hu
- GitHub: https://github.com/your-org/fizetesek

---

**Utolsó frissítés:** 2025-11-09
