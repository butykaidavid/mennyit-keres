# Deployment Útmutató

## 🚀 Telepítési Módok

### 1. Docker Compose (Ajánlott)

A legegyszerűbb módja a teljes stack futtatásának.

#### Lépések:

1. **Környezeti változók beállítása**
```bash
cp .env.example .env
# Szerkeszd a .env fájlt a megfelelő értékekkel
```

2. **Docker konténerek indítása**
```bash
docker-compose up -d
```

3. **Adatbázis inicializálás**
```bash
docker-compose exec backend alembic upgrade head
```

4. **Ellenőrzés**
```bash
# API health check
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000
```

#### Szolgáltatások:
- **Backend API:** http://localhost:8000
- **Frontend:** http://localhost:3000
- **PostgreSQL:** localhost:5432
- **Redis:** localhost:6379
- **API Docs:** http://localhost:8000/docs

---

### 2. Manuális Telepítés

#### Backend

```bash
cd backend

# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# Environment
cp ../.env.example .env
# Szerkeszd a .env fájlt

# Database migrations
alembic upgrade head

# Run server
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Scraper

```bash
cd scraper

# Virtual environment
python -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt

# Run scraper
python main.py
```

#### Frontend

```bash
cd frontend

# Dependencies
npm install

# Environment
cp .env.local.example .env.local
# Szerkeszd a .env.local fájlt

# Development
npm run dev

# Production build
npm run build
npm start
```

---

### 3. Production Deployment

#### 3.1 VPS / Dedicated Server

**Előfeltételek:**
- Ubuntu 20.04+ / Debian 11+
- Docker és Docker Compose telepítve
- Domain név (opcionális)
- SSL certificate (Let's Encrypt)

**Lépések:**

1. **Repository klónozása**
```bash
git clone https://github.com/your-org/fizetesek.git
cd fizetesek
```

2. **Környezeti változók**
```bash
cp .env.example .env
nano .env  # Szerkesztés
```

3. **SSL Certificate (Let's Encrypt)**
```bash
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com
```

4. **Nginx konfiguráció**
```bash
# Másolás
sudo cp nginx/nginx.conf /etc/nginx/sites-available/fizetesek
sudo ln -s /etc/nginx/sites-available/fizetesek /etc/nginx/sites-enabled/

# SSL paths frissítése
sudo nano /etc/nginx/sites-available/fizetesek

# Nginx restart
sudo systemctl restart nginx
```

5. **Docker Compose production mode**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

6. **Monitoring beállítása**
```bash
# Sentry DSN
# Prometheus
# Grafana
```

#### 3.2 Cloud Platformok

##### AWS ECS

1. **ECR-be push**
```bash
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.eu-central-1.amazonaws.com

docker build -t fizetesek-backend ./backend
docker tag fizetesek-backend:latest your-account.dkr.ecr.eu-central-1.amazonaws.com/fizetesek-backend:latest
docker push your-account.dkr.ecr.eu-central-1.amazonaws.com/fizetesek-backend:latest
```

2. **ECS Task Definition**
```json
{
  "family": "fizetesek-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "your-account.dkr.ecr.eu-central-1.amazonaws.com/fizetesek-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "DATABASE_URL", "value": "..."},
        {"name": "REDIS_URL", "value": "..."}
      ]
    }
  ]
}
```

##### Google Cloud Run

```bash
# Build és deploy
gcloud builds submit --tag gcr.io/your-project/fizetesek-backend ./backend
gcloud run deploy fizetesek-backend --image gcr.io/your-project/fizetesek-backend --platform managed --region europe-west1
```

##### Heroku

```bash
# Backend
heroku create fizetesek-backend
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set OPENAI_API_KEY=your-key
git subtree push --prefix backend heroku main

# Frontend (Vercel ajánlott)
```

##### Vercel (Frontend)

```bash
# Vercel CLI
npm i -g vercel
cd frontend
vercel

# Vagy GitHub integration
# Push to GitHub -> Automatic deployment
```

---

## 🔒 Biztonság

### SSL/TLS

**Let's Encrypt automatikus megújítás:**
```bash
sudo crontab -e
# Add:
0 0 1 * * certbot renew --quiet
```

### Firewall

```bash
# UFW
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

### Environment Variables

**SOHA ne commitolj .env fájlt!**

Használj secrets management-et:
- AWS Secrets Manager
- Google Secret Manager
- HashiCorp Vault
- Docker Secrets

### Database Backups

**Automatikus backup script:**
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_NAME="fizetesek"

pg_dump -U admin $DB_NAME | gzip > $BACKUP_DIR/backup_$TIMESTAMP.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
```

**Cron job:**
```bash
0 2 * * * /path/to/backup.sh
```

---

## 📊 Monitoring

### Sentry (Error Tracking)

```python
# backend/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[FastApiIntegration()],
    environment=settings.APP_ENV
)
```

### Prometheus + Grafana

```yaml
# docker-compose.monitoring.yml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Logging

**Centralized logging (ELK Stack):**
- Elasticsearch
- Logstash
- Kibana

---

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run Backend Tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest
      
      - name: Run Frontend Tests
        run: |
          cd frontend
          npm install
          npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker Images
        run: |
          docker build -t fizetesek-backend:${{ github.sha }} ./backend
          docker build -t fizetesek-scraper:${{ github.sha }} ./scraper
      
      - name: Push to Registry
        run: |
          docker push your-registry/fizetesek-backend:${{ github.sha }}
          docker push your-registry/fizetesek-scraper:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Production
        run: |
          ssh user@server "cd /app && docker-compose pull && docker-compose up -d"
```

---

## 📝 Checklist

### Pre-Deployment
- [ ] Environment variables beállítva
- [ ] Database migrations futtatva
- [ ] SSL certificate telepítve
- [ ] Firewall konfigurálva
- [ ] Backup script beállítva
- [ ] Monitoring eszközök konfigurálva
- [ ] Domain DNS beállítva

### Post-Deployment
- [ ] Health check végpontok működnek
- [ ] API dokumentáció elérhető
- [ ] Frontend betölt
- [ ] Scraping működik
- [ ] Logs elérhetők
- [ ] Monitoring dashboardok aktívak
- [ ] Backup tesztelve

### Performance
- [ ] Database indexek
- [ ] Redis caching
- [ ] CDN statikus fájlokhoz
- [ ] Gzip compression
- [ ] Image optimization

---

## 🐛 Troubleshooting

### Backend nem indul

```bash
# Logs ellenőrzése
docker-compose logs backend

# Database kapcsolat
docker-compose exec backend python -c "from app.config.database import engine; print(engine.url)"
```

### Scraping hibák

```bash
# Scraper logs
docker-compose logs scraper

# Manuális futtatás
docker-compose exec scraper python main.py profession 1
```

### Frontend build fail

```bash
# Logs
npm run build --verbose

# Node_modules tisztítás
rm -rf node_modules package-lock.json
npm install
```

---

## 📞 Support

- **Email:** devops@fizetesek.hu
- **Slack:** #deployment
- **Documentation:** https://docs.fizetesek.hu

---

**Utolsó frissítés:** 2025-11-09
