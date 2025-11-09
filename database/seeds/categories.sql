-- Seed data for categories
-- Magyar kategóriák az állásokhoz

INSERT INTO categories (name, slug, description) VALUES
    ('IT és Telekommunikáció', 'it', 'Szoftverfejlesztés, rendszergazda, IT support, adatbázis szakértő, hálózati mérnök'),
    ('Frontend Fejlesztés', 'frontend', 'React, Vue, Angular, JavaScript, TypeScript fejlesztők'),
    ('Backend Fejlesztés', 'backend', 'Python, Java, .NET, Node.js, PHP fejlesztők'),
    ('DevOps és Infrastruktúra', 'devops', 'DevOps engineer, SRE, CI/CD, Kubernetes, Docker'),
    ('Adattudomány és AI', 'data-science', 'Data scientist, ML engineer, AI specialist'),
    ('Mobilfejlesztés', 'mobile', 'iOS, Android, Flutter, React Native fejlesztők'),
    
    ('Mérnöki', 'engineering', 'Gépész, villamos, építő, autóipari mérnökök'),
    ('Gépészmérnök', 'mechanical', 'Gépészmérnökök, CAD tervezők'),
    ('Villamosmérnök', 'electrical', 'Elektronikai és villamosmérnökök'),
    ('Építőmérnök', 'civil', 'Építészmérnökök, építésvezetők'),
    
    ('Értékesítés', 'sales', 'Sales manager, értékesítési képviselő, key account manager'),
    ('B2B Értékesítés', 'b2b-sales', 'Üzleti értékesítés'),
    ('B2C Értékesítés', 'b2c-sales', 'Fogyasztói értékesítés'),
    
    ('Marketing', 'marketing', 'Marketing manager, content creator, social media specialist'),
    ('Digitális Marketing', 'digital-marketing', 'SEO, SEM, performance marketing'),
    ('Content Marketing', 'content-marketing', 'Tartalomkészítés, copywriting'),
    
    ('Pénzügy', 'finance', 'Könyvelő, controller, pénzügyi elemző, számviteli szakértő'),
    ('Könyvelés', 'accounting', 'Könyvelők, főkönyvelők'),
    ('Kontrolling', 'controlling', 'Controllerek, üzleti elemzők'),
    
    ('HR és Toborzás', 'hr', 'HR manager, recruiter, HR business partner'),
    ('Toborzás', 'recruitment', 'Toborzási szakemberek, headhunterek'),
    ('HR Adminisztráció', 'hr-admin', 'HR adminisztrátorok, bérszámfejtők'),
    
    ('Ügyfélszolgálat', 'customer-service', 'Call center munkatárs, ügyfélszolgálati vezető'),
    ('Call Center', 'call-center', 'Telefonos ügyfélszolgálat'),
    ('Customer Success', 'customer-success', 'Ügyfél-sikeresség szakemberek'),
    
    ('Termelés és Gyártás', 'production', 'Gyártásvezető, műszakvezető, termeléstervező'),
    ('Minőségbiztosítás', 'quality', 'QA engineer, minőségbiztosítási szakemberek'),
    
    ('Logisztika', 'logistics', 'Logisztikai koordinátor, raktárvezető, szállítmányozó'),
    ('Raktározás', 'warehouse', 'Raktári dolgozók, raktárvezetők'),
    ('Szállítmányozás', 'shipping', 'Szállítmányozási szakemberek'),
    
    ('Oktatás', 'education', 'Tanár, oktató, tréner, coach'),
    ('Nyelvoktatás', 'language-teaching', 'Nyelvtanárok'),
    ('IT Oktatás', 'it-training', 'IT trénerek'),
    
    ('Egészségügy', 'healthcare', 'Orvos, ápoló, gyógyszerész, orvosi asszisztens'),
    ('Orvosok', 'doctors', 'Háziorvos, szakorvos'),
    ('Ápolás', 'nursing', 'Ápolók, asszisztensek'),
    
    ('Jogi', 'legal', 'Ügyvéd, jogi tanácsadó, compliance officer'),
    
    ('Művészet és Dizájn', 'design', 'Grafikus, UX/UI designer, kreatív vezető'),
    ('Grafikai Tervezés', 'graphic-design', 'Grafikusok, illusztrátorok'),
    ('UX/UI Design', 'ux-ui', 'UX/UI tervezők'),
    
    ('Vendéglátás', 'hospitality', 'Felszolgáló, szakács, hotel recepciós'),
    ('Turizmus', 'tourism', 'Idegenvezető, utazási tanácsadó'),
    
    ('Kereskedelem', 'retail', 'Eladó, boltvezető, visual merchandiser'),
    
    ('Ingatlan', 'real-estate', 'Ingatlan értékesítő, ingatlanközvetítő'),
    
    ('Egyéb', 'other', 'Egyéb munkakörök')
ON CONFLICT (slug) DO NOTHING;
