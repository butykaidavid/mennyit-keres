"""
Main Scraper
Scraperek futtatása és koordinálása
"""

import logging
import sys
from typing import List, Dict

from spiders.profession_scraper import ProfessionScraper
from spiders.jobs_hu_scraper import JobsHuScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ScraperManager:
    """Scraperek kezelése"""
    
    def __init__(self):
        self.scrapers = {
            'profession': ProfessionScraper(),
            'jobs': JobsHuScraper(),
        }
    
    def run_all(self, max_pages: int = 5) -> Dict[str, List[Dict]]:
        """Összes scraper futtatása"""
        results = {}
        
        for name, scraper in self.scrapers.items():
            logger.info(f"Starting scraper: {name}")
            try:
                jobs = scraper.scrape(max_pages=max_pages)
                results[name] = jobs
                logger.info(f"Scraper {name} finished: {len(jobs)} jobs")
            except Exception as e:
                logger.error(f"Error in scraper {name}: {e}")
                results[name] = []
        
        return results
    
    def run_single(self, portal: str, max_pages: int = 5) -> List[Dict]:
        """Egy scraper futtatása"""
        if portal not in self.scrapers:
            logger.error(f"Unknown portal: {portal}")
            return []
        
        logger.info(f"Starting scraper: {portal}")
        try:
            jobs = self.scrapers[portal].scrape(max_pages=max_pages)
            logger.info(f"Scraper {portal} finished: {len(jobs)} jobs")
            return jobs
        except Exception as e:
            logger.error(f"Error in scraper {portal}: {e}")
            return []


def main():
    """Main entry point"""
    manager = ScraperManager()
    
    # Argumentumok kezelése
    if len(sys.argv) > 1:
        portal = sys.argv[1]
        max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        jobs = manager.run_single(portal, max_pages)
    else:
        # Összes scraper futtatása
        results = manager.run_all(max_pages=3)
        
        # Összesítés
        total_jobs = sum(len(jobs) for jobs in results.values())
        logger.info(f"\n{'='*50}")
        logger.info(f"Total jobs scraped: {total_jobs}")
        for portal, jobs in results.items():
            logger.info(f"  - {portal}: {len(jobs)} jobs")
        logger.info(f"{'='*50}\n")


if __name__ == "__main__":
    main()
