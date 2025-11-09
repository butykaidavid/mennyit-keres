# Hozzájárulási Útmutató

Köszönjük, hogy érdekel a projekt fejlesztése! Ez az útmutató segít eligazodni a hozzájárulási folyamatban.

## 🚀 Gyors Start

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/fizetesek.git
   cd fizetesek
   ```
3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**
5. **Test your changes**
6. **Commit and push**
7. **Create a Pull Request**

## 📝 Kódolási Szabályok

### Python (Backend)
- **PEP 8** követése
- **Type hints** használata
- **Docstrings** minden függvényhez
- **Black** formatter (line length: 88)
- **Flake8** linter

```python
def calculate_salary_average(jobs: List[Job]) -> float:
    """
    Fizetések átlagának kiszámítása.
    
    Args:
        jobs: Állások listája
        
    Returns:
        Átlagfizetés float-ként
    """
    if not jobs:
        return 0.0
    
    salaries = [job.salary_min for job in jobs if job.salary_min]
    return sum(salaries) / len(salaries) if salaries else 0.0
```

### TypeScript (Frontend)
- **ESLint** követése
- **TypeScript strict mode**
- **Functional components** használata
- **Hooks** használata osztályok helyett

```typescript
interface JobCardProps {
  job: Job;
  onSelect: (id: string) => void;
}

export const JobCard: React.FC<JobCardProps> = ({ job, onSelect }) => {
  return (
    <div onClick={() => onSelect(job.id)}>
      <h3>{job.title}</h3>
      <p>{job.company}</p>
    </div>
  );
};
```

## 🧪 Tesztelés

### Backend Tests
```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## 🔀 Git Workflow

### Branch Naming
- `feature/` - Új funkció
- `bugfix/` - Hibajavítás
- `hotfix/` - Sürgős javítás
- `refactor/` - Kód refaktorálás
- `docs/` - Dokumentáció

**Példák:**
- `feature/add-linkedin-scraper`
- `bugfix/fix-salary-parsing`
- `docs/update-api-documentation`

### Commit Messages

Használd a [Conventional Commits](https://www.conventionalcommits.org/) formátumot:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` - Új funkció
- `fix` - Hibajavítás
- `docs` - Dokumentáció
- `style` - Formázás
- `refactor` - Refaktorálás
- `test` - Tesztek
- `chore` - Build/tool változások

**Példák:**
```bash
feat(scraper): add CVOnline.hu scraper

Implemented new scraper for CVOnline.hu with salary parsing.

Closes #42

---

fix(api): correct salary statistics calculation

Fixed bug where median salary was calculated incorrectly.

Fixes #35

---

docs(readme): update installation instructions

Updated Docker installation steps with latest version.
```

## 📦 Pull Request Process

1. **Frissítsd a dokumentációt** ha szükséges
2. **Adj hozzá teszteket** új funkcióhoz
3. **Ellenőrizd a linter-t** (`flake8`, `eslint`)
4. **Futtasd a teszteket** (`pytest`, `npm test`)
5. **Írj részletes PR description-t**
6. **Link-eld a kapcsolódó issue-kat**

### PR Template

```markdown
## Változások leírása
[Rövid leírás a változásokról]

## Issue referencia
Closes #[issue number]

## Tesztelés
- [ ] Unit tesztek hozzáadva
- [ ] Integration tesztek átmentek
- [ ] Manuálisan tesztelve

## Checklist
- [ ] Kódom követi a projekt stílusát
- [ ] Self-review elvégezve
- [ ] Dokumentáció frissítve
- [ ] Nincsenek új warnings
- [ ] Tesztek átmennek
```

## 🐛 Bug Reports

Használd a GitHub Issues-t bugok jelentésére.

### Bug Report Template

```markdown
**Bug leírása**
Rövid és pontos leírás a bugról.

**Reprodukálási lépések**
1. Menj a '...'
2. Kattints a '...'
3. Scroll le '...'
4. Lásd a hibát

**Várt viselkedés**
Mit vártál, hogy történjen.

**Képernyőképek**
Ha van, add hozzá.

**Környezet:**
 - OS: [pl. Ubuntu 20.04]
 - Browser: [pl. Chrome 96]
 - Version: [pl. 1.0.0]

**További kontextus**
Bármilyen más információ a problémáról.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**A funkció leírása**
Világos és tömör leírás arról, mit szeretnél.

**Probléma amit megold**
Mit oldana meg ez a funkció? Mi a use case?

**Lehetséges megvalósítás**
Ha van ötleted, hogyan lehetne implementálni.

**Alternatívák**
Milyen alternatív megoldásokat vagy funkciókat fontoltál meg?

**További kontextus**
Bármilyen más információ vagy képernyőkép.
```

## 📚 Dokumentáció

- **README.md** - Főoldal, áttekintés
- **API.md** - API dokumentáció
- **DEPLOYMENT.md** - Deploy útmutató
- **Code comments** - Inline dokumentáció
- **Docstrings** - Függvény dokumentáció

## 🔐 Biztonsági Problémák

**Ne** nyiss publikus issue-t biztonsági problémákhoz!

Küldj email-t: security@fizetesek.hu

## 📞 Segítség

- **GitHub Discussions** - Kérdések, ötletek
- **Slack** - Real-time kommunikáció
- **Email** - dev@fizetesek.hu

## 📜 Code of Conduct

Légy tiszteletteljes és professzionális minden közreműködővel szemben.

## 🙏 Elismerés

Minden hozzájáruló neve szerepelni fog a CONTRIBUTORS.md fájlban.

---

**Köszönjük a hozzájárulásodat! 🎉**
