# API Dokumentáció

## Áttekintés

A Fizetési Info Platform RESTful API-t biztosít az állásadatok és fizetési statisztikák eléréséhez.

**Base URL:** `http://localhost:8000/api`

**API Dokumentáció:** `http://localhost:8000/docs` (Swagger UI)

## Authentikáció

Egyes végpontok JWT token-t igényelnek.

```http
Authorization: Bearer <your_jwt_token>
```

## Végpontok

### Jobs (Állások)

#### GET /api/jobs
Állások listázása paginálással és szűrőkkel.

**Query paraméterek:**
- `skip` (int): Kihagyott rekordok száma (default: 0)
- `limit` (int): Lekért rekordok száma (default: 10, max: 100)
- `location` (string): Helyszín szerinti szűrés
- `category_id` (UUID): Kategória szerinti szűrés
- `min_salary` (int): Minimum fizetés szerinti szűrés
- `verified_only` (bool): Csak ellenőrzött állások (default: false)

**Példa kérés:**
```bash
GET /api/jobs?limit=20&location=Budapest&min_salary=500000
```

**Példa válasz:**
```json
{
  "total": 145,
  "skip": 0,
  "limit": 20,
  "jobs": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Senior Python Developer",
      "company": "Tech Kft.",
      "location": "Budapest",
      "salary_min": 800000,
      "salary_max": 1200000,
      "salary_currency": "HUF",
      "salary_period": "monthly",
      "experience_level": "senior",
      "employment_type": "full-time",
      "skills": ["Python", "Django", "PostgreSQL"],
      "description": "...",
      "source_url": "https://...",
      "source_portal": "profession.hu",
      "verified": true,
      "created_at": "2025-11-01T10:00:00Z"
    }
  ]
}
```

#### GET /api/jobs/{job_id}
Egy állás részletes adatai.

**Path paraméter:**
- `job_id` (UUID): Állás azonosító

**Példa kérés:**
```bash
GET /api/jobs/123e4567-e89b-12d3-a456-426614174000
```

#### GET /api/jobs/search
Állások keresése kulcsszavak alapján.

**Query paraméterek:**
- `q` (string, required): Keresési kulcsszó (min 2 karakter)
- `skip` (int): Paginálás
- `limit` (int): Paginálás

**Példa kérés:**
```bash
GET /api/jobs/search?q=python&limit=10
```

#### POST /api/jobs
Új állás létrehozása (Admin).

**Request body:**
```json
{
  "title": "Junior Developer",
  "company": "StartUp Kft.",
  "location": "Budapest",
  "salary_min": 400000,
  "salary_max": 600000,
  "description": "...",
  "category_id": "..."
}
```

---

### Categories (Kategóriák)

#### GET /api/categories
Összes kategória listázása.

**Példa válasz:**
```json
{
  "total": 14,
  "categories": [
    {
      "id": "...",
      "name": "IT és Telekommunikáció",
      "slug": "it",
      "description": "...",
      "created_at": "..."
    }
  ]
}
```

#### GET /api/categories/{slug}
Egy kategória részletei.

**Path paraméter:**
- `slug` (string): Kategória slug (pl: "it", "marketing")

**Példa kérés:**
```bash
GET /api/categories/it
```

#### GET /api/categories/{slug}/jobs
Egy kategória állásai.

**Query paraméterek:**
- `skip`, `limit`: Paginálás

**Példa kérés:**
```bash
GET /api/categories/it/jobs?limit=20
```

---

### Statistics (Statisztikák)

#### GET /api/statistics/salary
Fizetési statisztikák.

**Query paraméterek:**
- `job_title` (string): Munkakör
- `location` (string): Helyszín
- `experience_level` (string): Tapasztalati szint

**Példa kérés:**
```bash
GET /api/statistics/salary?job_title=developer&location=Budapest
```

**Példa válasz:**
```json
{
  "filters": {
    "job_title": "developer",
    "location": "Budapest"
  },
  "statistics": [
    {
      "job_title": "Python Developer",
      "avg_salary": 750000,
      "median_salary": 700000,
      "min_salary": 400000,
      "max_salary": 1500000,
      "percentile_25": 550000,
      "percentile_75": 950000,
      "sample_size": 84
    }
  ]
}
```

#### GET /api/statistics/trending
Legkeresettebb munkakörök.

**Query paraméterek:**
- `limit` (int): Találatok száma (max: 50)

**Példa válasz:**
```json
{
  "count": 10,
  "trending_jobs": [
    {
      "title": "Python Developer",
      "count": 156,
      "avg_salary": 750000
    }
  ]
}
```

#### GET /api/statistics/locations
Helyszín szerinti statisztikák.

**Példa válasz:**
```json
{
  "locations": [
    {
      "location": "Budapest",
      "job_count": 1234,
      "avg_salary": 650000
    }
  ]
}
```

#### GET /api/statistics/salary-distribution
Fizetési eloszlás.

**Query paraméterek:**
- `job_title` (string): Munkakör (opcionális)

**Példa válasz:**
```json
{
  "job_title": "Developer",
  "distribution": {
    "avg": 700000,
    "min": 300000,
    "max": 2000000,
    "sample_size": 450
  }
}
```

---

### Admin

#### POST /api/admin/scrape/trigger
Scraping feladat indítása.

**Request body:**
```json
{
  "portal": "profession"  // vagy "jobs", "all"
}
```

**Authentikáció:** JWT token szükséges

#### GET /api/admin/jobs/pending
Ellenőrzésre váró állások.

**Query paraméterek:**
- `skip`, `limit`: Paginálás

**Authentikáció:** JWT token szükséges

#### PUT /api/admin/jobs/{job_id}/verify
Állás megerősítése.

**Path paraméter:**
- `job_id` (UUID): Állás azonosító

**Request body:**
```json
{
  "verified": true
}
```

**Authentikáció:** JWT token szükséges

#### DELETE /api/admin/jobs/{job_id}
Állás törlése (soft delete).

**Authentikáció:** JWT token szükséges

#### GET /api/admin/dashboard/stats
Dashboard statisztikák.

**Példa válasz:**
```json
{
  "total_jobs": 5432,
  "verified_jobs": 4821,
  "pending_jobs": 611,
  "verification_rate": 88.75,
  "portals": [
    {
      "portal": "profession.hu",
      "count": 2156
    }
  ]
}
```

---

## Hibakezelés

**HTTP státuszkódok:**
- `200 OK` - Sikeres kérés
- `201 Created` - Sikeres létrehozás
- `400 Bad Request` - Hibás kérés
- `401 Unauthorized` - Nincs authentikáció
- `403 Forbidden` - Nincs jogosultság
- `404 Not Found` - Nem található
- `500 Internal Server Error` - Szerverhiba

**Hibaformátum:**
```json
{
  "detail": "Hibaüzenet"
}
```

## Rate Limiting

- **60 kérés / perc** per IP cím
- **1000 kérés / óra** per IP cím

## CORS

Engedélyezett origin-ek:
- `http://localhost:3000`
- `http://localhost:8000`
- (Production URL-ek)

## Verziókezelés

Jelenlegi verzió: **v1.0**

Jövőbeli verziók: `/api/v2/...`

---

**Utolsó frissítés:** 2025-11-09
