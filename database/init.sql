-- Database Initialization Script
-- Magyar Fizetési Információs Platform

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    parent_id UUID REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Jobs table
CREATE TABLE IF NOT EXISTS jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
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
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified BOOLEAN DEFAULT FALSE,
    active BOOLEAN DEFAULT TRUE,
    category_id UUID REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Salary statistics table
CREATE TABLE IF NOT EXISTS salary_statistics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
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
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title);
CREATE INDEX IF NOT EXISTS idx_jobs_category ON jobs(category_id);
CREATE INDEX IF NOT EXISTS idx_jobs_location ON jobs(location);
CREATE INDEX IF NOT EXISTS idx_jobs_scraped_at ON jobs(scraped_at DESC);
CREATE INDEX IF NOT EXISTS idx_jobs_verified ON jobs(verified);
CREATE INDEX IF NOT EXISTS idx_jobs_active ON jobs(active);
CREATE INDEX IF NOT EXISTS idx_salary_stats_title ON salary_statistics(job_title);
CREATE INDEX IF NOT EXISTS idx_categories_slug ON categories(slug);

-- Insert initial categories
INSERT INTO categories (name, slug, description) VALUES
    ('IT és Telekommunikáció', 'it', 'Informatika, szoftverfejlesztés, IT infrastruktúra'),
    ('Mérnöki', 'engineering', 'Gépészmérnök, villamosmérnök, építőmérnök'),
    ('Értékesítés', 'sales', 'Értékesítési képviselő, sales manager'),
    ('Marketing', 'marketing', 'Digitális marketing, tartalommarketing, SEO'),
    ('Pénzügy', 'finance', 'Könyvelés, pénzügyi elemzés, banki szakértő'),
    ('HR és Toborzás', 'hr', 'Humán erőforrás, toborzás, HR menedzsment'),
    ('Ügyfélszolgálat', 'customer-service', 'Ügyfélkapcsolat, call center, support'),
    ('Termelés és Gyártás', 'production', 'Gyártási folyamatok, minőségbiztosítás'),
    ('Logisztika', 'logistics', 'Szállítás, raktározás, ellátási lánc'),
    ('Oktatás', 'education', 'Tanár, oktató, tréner'),
    ('Egészségügy', 'healthcare', 'Orvos, ápoló, egészségügyi szakember'),
    ('Jogi', 'legal', 'Ügyvéd, jogi tanácsadó'),
    ('Művészet és Dizájn', 'design', 'Grafikus, UX/UI designer, kreatív'),
    ('Egyéb', 'other', 'Egyéb munkakörök')
ON CONFLICT (slug) DO NOTHING;

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_salary_statistics_updated_at BEFORE UPDATE ON salary_statistics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions (if needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_user;
