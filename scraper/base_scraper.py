"""
Base Scraper
Alap scraper osztály, amiből az összes konkrét scraper származik
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from typing import List, Dict, Optional
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper:
    """Alap scraper osztály"""
    
    def __init__(self, portal_name: str):
        self.portal_name = portal_name
        self.session = requests.Session()
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'hu-HU,hu;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
    def _get_page(self, url: str, retries: int = 3) -> Optional[str]:
        """HTTP GET kérés rate limiting-gel"""
        for attempt in range(retries):
            try:
                # Véletlenszerű delay
                time.sleep(random.uniform(1, 3))
                
                # Új User-Agent minden kérésnél
                self.headers['User-Agent'] = self.ua.random
                
                response = self.session.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                logger.info(f"Successfully fetched: {url}")
                return response.text
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching {url} (attempt {attempt + 1}/{retries}): {e}")
                if attempt == retries - 1:
                    return None
                time.sleep(random.uniform(3, 5))
        
        return None
    
    def _parse_html(self, html: str) -> BeautifulSoup:
        """HTML parsing BeautifulSoup-pal"""
        return BeautifulSoup(html, 'lxml')
    
    def scrape(self, max_pages: int = 5) -> List[Dict]:
        """
        Főbb scraping logika
        Felülírva az alosztályokban
        """
        raise NotImplementedError("Scrape method must be implemented in subclass")
    
    def parse_job(self, job_element) -> Optional[Dict]:
        """
        Egy állás adatainak kinyerése
        Felülírva az alosztályokban
        """
        raise NotImplementedError("Parse job method must be implemented in subclass")
    
    def save_to_db(self, jobs: List[Dict]):
        """Állások mentése adatbázisba"""
        # TODO: Database connection és mentés
        logger.info(f"Saving {len(jobs)} jobs to database")
        
    def normalize_salary(self, salary_text: str) -> Dict:
        """
        Fizetés normalizálása
        Példa: "450-650 ezer Ft/hó" -> {"min": 450000, "max": 650000}
        """
        import re
        
        if not salary_text:
            return {"min": None, "max": None, "currency": "HUF", "period": "monthly"}
        
        # Regex mintázatok
        salary_text = salary_text.lower().strip()
        
        # Ezer -> 1000
        if "ezer" in salary_text:
            numbers = re.findall(r'\d+', salary_text)
            if len(numbers) >= 2:
                return {
                    "min": int(numbers[0]) * 1000,
                    "max": int(numbers[1]) * 1000,
                    "currency": "HUF",
                    "period": "monthly" if "hó" in salary_text else "yearly"
                }
            elif len(numbers) == 1:
                return {
                    "min": int(numbers[0]) * 1000,
                    "max": int(numbers[0]) * 1000,
                    "currency": "HUF",
                    "period": "monthly" if "hó" in salary_text else "yearly"
                }
        
        return {"min": None, "max": None, "currency": "HUF", "period": "monthly"}
    
    def clean_text(self, text: str) -> str:
        """Szöveg tisztítása (whitespace, stb.)"""
        if not text:
            return ""
        return " ".join(text.strip().split())
