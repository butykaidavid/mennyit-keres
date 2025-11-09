"""
Jobs.hu Scraper
Magyar állásportál scraping
"""

import logging
from typing import List, Dict, Optional
from ..base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class JobsHuScraper(BaseScraper):
    """Jobs.hu scraper"""
    
    def __init__(self):
        super().__init__("jobs.hu")
        self.base_url = "https://www.jobs.hu"
        self.search_url = f"{self.base_url}/allasok"
        
    def scrape(self, max_pages: int = 5, category: str = None) -> List[Dict]:
        """Állások scraping"""
        all_jobs = []
        
        for page in range(1, max_pages + 1):
            logger.info(f"Scraping Jobs.hu page {page}/{max_pages}")
            
            # URL építés
            url = f"{self.search_url}?page={page}"
            if category:
                url += f"&category={category}"
            
            # Oldal letöltése
            html = self._get_page(url)
            if not html:
                logger.warning(f"Failed to fetch page {page}")
                continue
            
            # Parsing
            soup = self._parse_html(html)
            
            # Állások kinyerése (példa selectorok)
            job_elements = soup.find_all('article', class_='job-listing')
            
            for job_elem in job_elements:
                job_data = self.parse_job(job_elem)
                if job_data:
                    all_jobs.append(job_data)
            
            logger.info(f"Found {len(job_elements)} jobs on page {page}")
        
        logger.info(f"Total jobs scraped from Jobs.hu: {len(all_jobs)}")
        return all_jobs
    
    def parse_job(self, job_element) -> Optional[Dict]:
        """Egy állás adatainak kinyerése"""
        try:
            # Selectorok (példa - valós scraping előtt ellenőrizni!)
            title_elem = job_element.find('h3', class_='job-title')
            company_elem = job_element.find('div', class_='employer')
            location_elem = job_element.find('span', class_='city')
            salary_elem = job_element.find('div', class_='salary-info')
            link_elem = job_element.find('a', class_='job-link')
            
            if not title_elem:
                return None
            
            # Adatok kinyerése
            title = self.clean_text(title_elem.get_text())
            company = self.clean_text(company_elem.get_text()) if company_elem else None
            location = self.clean_text(location_elem.get_text()) if location_elem else None
            salary_text = self.clean_text(salary_elem.get_text()) if salary_elem else None
            link = link_elem.get('href') if link_elem else None
            
            # URL javítás
            if link and not link.startswith('http'):
                link = f"{self.base_url}{link}"
            
            # Fizetés normalizálás
            salary_data = self.normalize_salary(salary_text) if salary_text else {}
            
            job_data = {
                "title": title,
                "company": company,
                "location": location,
                "salary_min": salary_data.get("min"),
                "salary_max": salary_data.get("max"),
                "salary_currency": salary_data.get("currency", "HUF"),
                "salary_period": salary_data.get("period", "monthly"),
                "source_url": link,
                "source_portal": self.portal_name,
                "description": None,
                "skills": [],
                "verified": False
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing job from Jobs.hu: {e}")
            return None


if __name__ == "__main__":
    # Teszt futtatás
    scraper = JobsHuScraper()
    jobs = scraper.scrape(max_pages=2)
    print(f"Scraped {len(jobs)} jobs from Jobs.hu")
    
    if jobs:
        print("\nExample job:")
        print(jobs[0])
