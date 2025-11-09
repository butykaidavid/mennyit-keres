"""
Profession.hu Scraper
Magyar állásportál scraping
"""

import logging
from typing import List, Dict, Optional
from ..base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class ProfessionScraper(BaseScraper):
    """Profession.hu scraper"""
    
    def __init__(self):
        super().__init__("profession.hu")
        self.base_url = "https://www.profession.hu"
        self.search_url = f"{self.base_url}/allasok"
        
    def scrape(self, max_pages: int = 5, category: str = None) -> List[Dict]:
        """Állások scraping"""
        all_jobs = []
        
        for page in range(1, max_pages + 1):
            logger.info(f"Scraping page {page}/{max_pages}")
            
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
            
            # Állások kinyerése
            job_elements = soup.find_all('div', class_='job-card')  # Példa selector
            
            for job_elem in job_elements:
                job_data = self.parse_job(job_elem)
                if job_data:
                    all_jobs.append(job_data)
            
            logger.info(f"Found {len(job_elements)} jobs on page {page}")
        
        logger.info(f"Total jobs scraped: {len(all_jobs)}")
        return all_jobs
    
    def parse_job(self, job_element) -> Optional[Dict]:
        """Egy állás adatainak kinyerése"""
        try:
            # Címke keresése (példa selectorok - valós scraping előtt ellenőrizni kell)
            title_elem = job_element.find('h2', class_='job-title')
            company_elem = job_element.find('div', class_='company-name')
            location_elem = job_element.find('span', class_='location')
            salary_elem = job_element.find('span', class_='salary')
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
                "description": None,  # Részletes oldalról lenne
                "skills": [],
                "verified": False
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing job: {e}")
            return None
    
    def scrape_job_details(self, job_url: str) -> Optional[Dict]:
        """Állás részletes adatainak scraping"""
        html = self._get_page(job_url)
        if not html:
            return None
        
        soup = self._parse_html(html)
        
        # Részletes adatok kinyerése
        description_elem = soup.find('div', class_='job-description')
        requirements_elem = soup.find('div', class_='requirements')
        
        return {
            "description": self.clean_text(description_elem.get_text()) if description_elem else None,
            "requirements": self.clean_text(requirements_elem.get_text()) if requirements_elem else None
        }


if __name__ == "__main__":
    # Teszt futtatás
    scraper = ProfessionScraper()
    jobs = scraper.scrape(max_pages=2)
    print(f"Scraped {len(jobs)} jobs")
    
    if jobs:
        print("\nExample job:")
        print(jobs[0])
