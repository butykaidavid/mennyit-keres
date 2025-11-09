# Fizetési Info Platform - Frontend

Modern, responsive frontend React/Next.js használatával.

## 🚀 Kezdés

### Telepítés

```bash
npm install
# vagy
yarn install
```

### Fejlesztői mód

```bash
npm run dev
# vagy
yarn dev
```

Nyisd meg [http://localhost:3000](http://localhost:3000) a böngésződben.

### Build

```bash
npm run build
npm start
```

## 📁 Struktúra

```
frontend/
├── src/
│   ├── app/                 # Next.js 14 App Router
│   │   ├── page.tsx        # Főoldal
│   │   ├── layout.tsx      # Root layout
│   │   ├── kereses/        # Keresési oldal
│   │   ├── pozicio/        # Pozíció részletek
│   │   ├── kategoriak/     # Kategóriák
│   │   └── admin/          # Admin panel
│   │
│   ├── components/         # React komponensek
│   │   ├── layout/        # Layout komponensek
│   │   ├── job/           # Állás komponensek
│   │   ├── stats/         # Statisztika komponensek
│   │   └── common/        # Közös komponensek
│   │
│   ├── services/          # API szolgáltatások
│   │   ├── api.ts        # API kliens
│   │   └── jobs.ts       # Állások API
│   │
│   ├── store/            # Zustand state management
│   │   └── jobStore.ts
│   │
│   ├── types/            # TypeScript típusok
│   │   └── job.ts
│   │
│   └── utils/            # Segédfüggvények
│       └── formatters.ts
│
├── public/               # Statikus fájlok
│   ├── images/
│   └── icons/
│
├── tailwind.config.js   # TailwindCSS konfig
├── next.config.js       # Next.js konfig
└── tsconfig.json        # TypeScript konfig
```

## 🎨 Dizájn

- **TailwindCSS** - Utility-first CSS framework
- **Headless UI** - Accessible komponensek
- **Hero Icons** - Modern ikonok
- **Responsive** - Mobile-first megközelítés

## 📊 Grafikonok

- **Recharts** - Fizetési trendek vizualizációja
- Interaktív grafikonok
- Összehasonlító táblázatok

## 🔐 Authentikáció

- JWT alapú
- Védett route-ok
- Admin panel hozzáférés

## 🧪 Tesztelés

```bash
npm test
npm run test:watch
```

## 📝 Környezeti változók

`.env.local` fájlban:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

## 🚢 Deployment

Vercel, Netlify vagy Docker használatával.

```bash
npm run build
```

## 📄 License

MIT
