-- Sample job data for testing
-- Magyar teszt állások

-- Get IT category ID
DO $$
DECLARE
    it_cat_id UUID;
    sales_cat_id UUID;
    marketing_cat_id UUID;
BEGIN
    SELECT id INTO it_cat_id FROM categories WHERE slug = 'it' LIMIT 1;
    SELECT id INTO sales_cat_id FROM categories WHERE slug = 'sales' LIMIT 1;
    SELECT id INTO marketing_cat_id FROM categories WHERE slug = 'marketing' LIMIT 1;

    -- IT Jobs
    INSERT INTO jobs (title, company, location, salary_min, salary_max, salary_currency, salary_period, 
                      experience_level, employment_type, skills, description, source_portal, verified, category_id) 
    VALUES 
        ('Senior Python Developer', 'TechCorp Kft.', 'Budapest', 800000, 1200000, 'HUF', 'monthly', 
         'senior', 'full-time', '["Python", "Django", "PostgreSQL", "Docker", "AWS"]'::jsonb, 
         'Tapasztalt Python fejlesztőt keresünk Django projektekhez.', 'test_data', true, it_cat_id),
        
        ('Junior Frontend Developer', 'StartUp Ltd.', 'Budapest', 400000, 600000, 'HUF', 'monthly',
         'junior', 'full-time', '["JavaScript", "React", "HTML", "CSS", "Git"]'::jsonb,
         'Kezdő frontend fejlesztő pozíció React stack-kel.', 'test_data', true, it_cat_id),
        
        ('Full Stack Developer', 'Digital Agency', 'Debrecen', 600000, 900000, 'HUF', 'monthly',
         'medior', 'full-time', '["JavaScript", "Node.js", "React", "MongoDB", "Express"]'::jsonb,
         'Full stack fejlesztő MERN stack-kel.', 'test_data', true, it_cat_id),
        
        ('DevOps Engineer', 'CloudTech', 'Budapest', 900000, 1400000, 'HUF', 'monthly',
         'senior', 'full-time', '["Kubernetes", "Docker", "AWS", "Terraform", "CI/CD"]'::jsonb,
         'DevOps mérnök felhő infrastruktúra kezelésére.', 'test_data', true, it_cat_id),
        
        ('Data Scientist', 'AI Solutions', 'Szeged', 750000, 1100000, 'HUF', 'monthly',
         'medior', 'full-time', '["Python", "Machine Learning", "Pandas", "TensorFlow", "SQL"]'::jsonb,
         'Adattudós pozíció ML projektekhez.', 'test_data', true, it_cat_id),

    -- Sales Jobs
        ('Sales Manager', 'BigCorp Hungary', 'Budapest', 500000, 800000, 'HUF', 'monthly',
         'senior', 'full-time', '["B2B Sales", "Negotiation", "CRM", "Communication"]'::jsonb,
         'Értékesítési vezető B2B környezetben.', 'test_data', true, sales_cat_id),
        
        ('Junior Sales Representative', 'SalesTeam Kft.', 'Győr', 350000, 500000, 'HUF', 'monthly',
         'junior', 'full-time', '["Communication", "Customer Service", "Sales"]'::jsonb,
         'Kezdő értékesítő pozíció.', 'test_data', true, sales_cat_id),

    -- Marketing Jobs
        ('Digital Marketing Specialist', 'MarketingPro', 'Budapest', 500000, 750000, 'HUF', 'monthly',
         'medior', 'full-time', '["SEO", "Google Ads", "Facebook Ads", "Analytics", "Content Marketing"]'::jsonb,
         'Digitális marketing szakember keresése.', 'test_data', true, marketing_cat_id),
        
        ('Social Media Manager', 'Creative Agency', 'Budapest', 450000, 650000, 'HUF', 'monthly',
         'medior', 'full-time', '["Social Media", "Content Creation", "Copywriting", "Analytics"]'::jsonb,
         'Social media menedzser pozíció.', 'test_data', true, marketing_cat_id);
END $$;
