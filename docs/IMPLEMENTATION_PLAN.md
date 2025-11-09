# Implementációs Terv

## 📋 Részletes Lépések

### 1. PROJEKT INICIALIZÁLÁS (1-2 nap)

#### 1.1 Alapinfrastruktúra
- [x] Git repository létrehozása
- [x] Mappa struktúra kialakítása
- [ ] `.gitignore` beállítása
- [ ] `.env.example` fájlok létrehozása
- [ ] Docker környezet előkészítése

#### 1.2 Dokumentáció
- [x] README.md
- [x] Implementációs terv
- [ ] API dokumentáció sablon
- [ ] Adatbázis séma dokumentáció

---

### 2. BACKEND FEJLESZTÉS (1-2 hét)

#### 2.1 Alapbeállítások
```python
# Backend tech stack:
- FastAPI 0.104+
- Python 3.10+
- PostgreSQL 14+
- SQLAlchemy 2.0
- Pydantic V2
- JWT authentication
```

#### 2.2 Szükséges fájlok
- [ ] `backend/requirements.txt` - Függőségek
- [ ] `backend/main.py` - FastAPI app
- [ ] `backend/app/config/settings.py` - Beállítások
- [ ] `backend/app/models/` - SQLAlchemy modellek
- [ ] `backend/app/routers/` - API végpontok
- [ ] `backend/app/services/` - Business logic

#### 2.3 Adatbázis Modellek

**Job Model:**
```python
class Job(Base):
    id: UUID
    title: str
    company: str
    location: str
    salary_min: int
    salary_max: int
    salary_currency: str
    experience_level: str
    employment_type: str
    skills: List[str]
    description: str
    source_url: str
    scraped_at: datetime
    verified: bool
    category: str
```

**Salary Statistics Model:**
```python
class SalaryStats(Base):
    id: UUID
    job_title: str
    avg_salary: float
    median_salary: float
    min_salary: float
    max_salary: float
    sample_size: int
    last_updated: datetime
```

**Category Model:**
```python
class Category(Base):
    id: UUID
    name: str
    slug: str
    parent_id: UUID (optional)
    description: str
```

#### 2.4 API Végpontok

**Keresési API:**
- `GET /api/jobs` - Összes állás
- `GET /api/jobs/{id}` - Egy állás részletei
- `GET /api/jobs/search` - Keresés query paraméterekkel
- `GET /api/jobs/statistics` - Statisztikák

**Munkakör API:**
- `GET /api/positions` - Pozíciók listája
- `GET /api/positions/{slug}` - Pozíció adatok
- `GET /api/positions/{slug}/salary-trends` - Fizetési trendek

**Kategória API:**
- `GET /api/categories` - Kategóriák
- `GET /api/categories/{slug}` - Kategória részletek

**Admin API:**
- `POST /api/admin/scrape` - Scraping indítása
- `GET /api/admin/jobs/pending` - Jóváhagyásra váró állások
- `PUT /api/admin/jobs/{id}/verify` - Állás megerősítése

---

### 3. SCRAPING MODUL (1-2 hét)

#### 3.1 Célportálok

**Prioritás 1 (Magyar állásportálok):**
1. **profession.hu**
   - URL pattern: `https://www.profession.hu/allasok/`
   - Keresési paraméterek: kategória, fizetés, helyszín
   - Anti-scraping: reCAPTCHA, rate limiting

2. **jobs.hu**
   - URL pattern: `https://www.jobs.hu/allasok/`
   - API endpoint (ha elérhető)
   - Részletes fizetési adatok

3. **cvonline.hu**
   - URL pattern: `https://www.cvonline.hu/allasok/`
   - Szűrők: tapasztalat, iparág

**Prioritás 2:**
4. **LinkedIn Jobs** (magyar állások)
5. **karrierstart.hu**
6. **workania.hu**

#### 3.2 Scraper Architektúra

```python
# scraper/base_scraper.py
class BaseScraper:
    def __init__(self):
        self.session = requests.Session()
        self.user_agent = random.choice(USER_AGENTS)
    
    def scrape(self) -> List[JobData]:
        pass
    
    def parse(self, html: str) -> List[JobData]:
        pass
    
    def save_to_db(self, jobs: List[JobData]):
        pass
```

#### 3.3 Anti-Scraping Megoldások
- **Rotating User Agents** - Változó böngésző azonosítók
- **Proxy rotation** - Különböző IP címek használata
- **Rate limiting** - Kérések korlátozása
- **Request delays** - Véletlenszerű várakozások
- **Session management** - Cookie és session kezelés
- **Headless browser** - Selenium/Playwright JavaScripthez

#### 3.4 Adatgyűjtési Stratégia
```python
# Scraping ütemezés
SCRAPING_SCHEDULE = {
    'profession.hu': {
        'interval': 3600,  # 1 óra
        'categories': ['IT', 'Engineering', 'Sales', ...],
        'max_pages': 10
    },
    'jobs.hu': {
        'interval': 3600,
        'categories': [...],
        'max_pages': 10
    }
}
```

---

### 4. AI INTEGRÁCIÓ (1 hét)

#### 4.1 AI Feladatok

**Adatok tisztítása:**
```python
# OpenAI prompt példa
prompt = f"""
Normalize this job salary information:
- Input: "{raw_salary_text}"
- Output format: min_salary, max_salary, currency, period

Example:
- Input: "450-650 ezer Ft/hó"
- Output: {{"min": 450000, "max": 650000, "currency": "HUF", "period": "monthly"}}
"""
```

**Kategorizálás:**
```python
def categorize_job(title: str, description: str) -> str:
    """AI-based job categorization"""
    prompt = f"""
    Categorize this Hungarian job posting:
    Title: {title}
    Description: {description}
    
    Categories: IT, Engineering, Sales, Marketing, HR, Finance, ...
    Output: Primary category
    """
    return openai.complete(prompt)
```

**Készség kivonatolás:**
```python
def extract_skills(description: str) -> List[str]:
    """Extract required skills from job description"""
    prompt = f"""
    Extract technical and soft skills from this Hungarian job description:
    {description}
    
    Output format: ["Python", "SQL", "Communication", ...]
    """
    return openai.complete(prompt)
```

#### 4.2 LangChain Integráció
```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Salary normalization chain
salary_chain = LLMChain(
    llm=openai_llm,
    prompt=salary_prompt_template
)

# Job categorization chain
categorization_chain = LLMChain(
    llm=openai_llm,
    prompt=categorization_prompt_template
)
```

#### 4.3 Költség optimalizálás
- **Batch processing** - Több adat egyszerre
- **Caching** - Ismétlődő eredmények tárolása
- **Local LLM** - Kisebb feladatokhoz (pl. Llama 2)
- **GPT-3.5-turbo** - Egyszerűbb feladatokhoz
- **GPT-4** - Komplex elemzésekhez

---

### 5. FRONTEND FEJLESZTÉS (2 hét)

#### 5.1 Technológiai Stack
```json
{
  "framework": "Next.js 14",
  "styling": "TailwindCSS",
  "charts": "Recharts",
  "state": "Zustand",
  "api": "Axios",
  "forms": "React Hook Form"
}
```

#### 5.2 Oldalak

**1. Főoldal (`/`)**
- Hero section keresővel
- Népszerű munkakörök
- Statisztikák (átlagfizetések)
- Friss állások

**2. Keresési eredmények (`/kereses`)**
- Szűrők (helyszín, tapasztalat, fizetés)
- Álláslistázás
- Rendezési opciók
- Paginálás

**3. Munkakör részletek (`/pozicio/[slug]`)**
- Pozíció leírás
- Fizetési statisztikák
- Trend grafikonok
- Hasonló pozíciók
- Kapcsolódó állások

**4. Kategóriák (`/kategoriak/[slug]`)**
- Kategória áttekintés
- Átlagfizetések
- Népszerű pozíciók
- Piaci trendek

**5. Statisztikák (`/statisztikak`)**
- Iparági összehasonlítás
- Fizetési trendek
- Helyszín szerinti bontás
- Interaktív grafikonok

**6. Admin (`/admin`)**
- Dashboard
- Állások kezelése
- Scraping irányítópult
- Felhasználók

#### 5.3 Komponensek
```
components/
├── layout/
│   ├── Header.tsx
│   ├── Footer.tsx
│   └── Sidebar.tsx
├── job/
│   ├── JobCard.tsx
│   ├── JobList.tsx
│   ├── JobFilters.tsx
│   └── JobDetails.tsx
├── stats/
│   ├── SalaryChart.tsx
│   ├── TrendChart.tsx
│   └── ComparisonTable.tsx
└── common/
    ├── SearchBar.tsx
    ├── Button.tsx
    └── Card.tsx
```

---

### 6. ADATBÁZIS TERVEZÉS (2-3 nap)

#### 6.1 PostgreSQL Schema

```sql
-- Jobs table
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    location VARCHAR(255),
    salary_min INTEGER,
    salary_max INTEGER,
    salary_currency VARCHAR(10) DEFAULT 'HUF',
    salary_period VARCHAR(20) DEFAULT 'monthly',
    experience_level VARCHAR(50),
    employment_type VARCHAR(50),
    skills JSONB,
    description TEXT,
    source_url TEXT,
    source_portal VARCHAR(100),
    scraped_at TIMESTAMP DEFAULT NOW(),
    verified BOOLEAN DEFAULT FALSE,
    category_id UUID REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Categories table
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    parent_id UUID REFERENCES categories(id),
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Salary statistics table
CREATE TABLE salary_statistics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_title VARCHAR(255) NOT NULL,
    category_id UUID REFERENCES categories(id),
    avg_salary FLOAT,
    median_salary FLOAT,
    min_salary FLOAT,
    max_salary FLOAT,
    percentile_25 FLOAT,
    percentile_75 FLOAT,
    sample_size INTEGER,
    location VARCHAR(255),
    experience_level VARCHAR(50),
    last_updated TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_jobs_title ON jobs(title);
CREATE INDEX idx_jobs_category ON jobs(category_id);
CREATE INDEX idx_jobs_location ON jobs(location);
CREATE INDEX idx_jobs_scraped_at ON jobs(scraped_at);
CREATE INDEX idx_salary_stats_title ON salary_statistics(job_title);
```

#### 6.2 Seed Data
```python
# Initial categories
categories = [
    {"name": "IT és Telekommunikáció", "slug": "it"},
    {"name": "Mérnöki", "slug": "engineering"},
    {"name": "Értékesítés", "slug": "sales"},
    {"name": "Marketing", "slug": "marketing"},
    {"name": "Pénzügy", "slug": "finance"},
    {"name": "HR", "slug": "hr"},
    {"name": "Ügyfélszolgálat", "slug": "customer-service"},
    # ...
]
```

---

### 7. DEPLOYMENT (3-5 nap)

#### 7.1 Docker Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://...
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000

  db:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=fizetesek
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=secret

  redis:
    image: redis:7-alpine

  scraper:
    build: ./scraper
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

#### 7.2 CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd backend && pytest
          cd frontend && npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Deploy commands
```

#### 7.3 Production Checklist
- [ ] SSL certificate (Let's Encrypt)
- [ ] Environment variables configured
- [ ] Database backups automated
- [ ] Monitoring setup (Sentry, LogRocket)
- [ ] Performance optimization
- [ ] CDN setup for static files
- [ ] Rate limiting configured
- [ ] Security headers configured

---

### 8. TESZTELÉS (Folyamatos)

#### 8.1 Backend Tests
```python
# tests/test_jobs_api.py
def test_get_jobs():
    response = client.get("/api/jobs")
    assert response.status_code == 200
    assert "jobs" in response.json()

def test_search_jobs():
    response = client.get("/api/jobs/search?q=python")
    assert response.status_code == 200
```

#### 8.2 Scraping Tests
```python
# tests/test_scrapers.py
def test_profession_scraper():
    scraper = ProfessionScraper()
    jobs = scraper.scrape(max_pages=1)
    assert len(jobs) > 0
    assert jobs[0].title is not None
```

#### 8.3 Frontend Tests
```typescript
// tests/JobCard.test.tsx
describe('JobCard', () => {
  it('renders job information', () => {
    render(<JobCard job={mockJob} />);
    expect(screen.getByText(mockJob.title)).toBeInTheDocument();
  });
});
```

---

## 🎯 Mérföldkövek

### Week 1-2: Foundation
- ✅ Projekt struktúra
- 🔄 Backend alapok
- 🔄 Database setup
- ⏳ Basic scraping

### Week 3-4: Core Features
- ⏳ API endpoints
- ⏳ Scraping automation
- ⏳ AI integration
- ⏳ Frontend basics

### Week 5-6: Polish
- ⏳ Admin panel
- ⏳ Advanced filters
- ⏳ Charts and stats
- ⏳ Testing

### Week 7-8: Launch
- ⏳ Performance optimization
- ⏳ Security hardening
- ⏳ Documentation
- ⏳ Deployment

---

## 📝 Napi Feladatok Példa

### Day 1
- [x] Initialize repository
- [x] Create folder structure
- [ ] Setup FastAPI project
- [ ] Configure database

### Day 2
- [ ] Create database models
- [ ] Setup migrations
- [ ] Create basic API endpoints
- [ ] Test endpoints

### Day 3
- [ ] Build first scraper (profession.hu)
- [ ] Test scraping
- [ ] Store data in database
- [ ] Handle errors

---

## 🔗 Hasznos Linkek

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Scrapy Documentation](https://docs.scrapy.org/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [OpenAI API](https://platform.openai.com/docs/)

---

**Utolsó frissítés:** 2025-11-09
