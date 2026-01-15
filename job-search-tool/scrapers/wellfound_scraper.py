"""
Wellfound (formerly AngelList Talent) job scraper.
"""
import time
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from models import JobPosting
from .base_scraper import BaseScraper
import config


class WellfoundScraper(BaseScraper):
    """Scraper for Wellfound jobs."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://wellfound.com"

    def build_search_url(self, search_term: str) -> str:
        """Build Wellfound job search URL."""
        # Wellfound uses role slugs
        term_slug = search_term.lower().replace(" ", "-")
        url = f"{self.base_url}/role/r/{term_slug}"
        return url

    def scrape(self, search_terms: List[str] = None) -> List[JobPosting]:
        """
        Scrape Wellfound jobs.

        Args:
            search_terms: List of job titles to search for

        Returns:
            List of JobPosting objects
        """
        if search_terms is None:
            search_terms = config.SEARCH_KEYWORDS

        self.init_driver()
        jobs = []

        for term in search_terms:
            self.logger.info(f"Searching Wellfound for: {term}")

            try:
                # Try direct role search
                url = f"{self.base_url}/jobs?keywords={term.replace(' ', '%20')}"
                self.driver.get(url)
                time.sleep(3)

                # Scroll to load jobs
                for _ in range(3):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                # Find job cards
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-test='StartupResult'], .job-listing")

                self.logger.info(f"Found {len(job_cards)} Wellfound job cards for '{term}'")

                for card in job_cards[:config.SCRAPER_CONFIG['max_results_per_site']]:
                    job = self._extract_job_from_card(card)
                    if job:
                        jobs.append(job)

                self.rate_limit()

            except Exception as e:
                self.logger.error(f"Error scraping Wellfound for '{term}': {e}")
                continue

        self.logger.info(f"Total Wellfound jobs scraped: {len(jobs)}")
        return jobs

    def _extract_job_from_card(self, card) -> Optional[JobPosting]:
        """Extract job details from a job card element."""
        try:
            # Extract title
            title_elem = card.find_element(By.CSS_SELECTOR, "h2, .job-title, [data-test='job-title']")
            title = title_elem.text.strip()

            # Extract company
            company_elem = card.find_element(By.CSS_SELECTOR, ".company-name, [data-test='company-name'], h3")
            company = company_elem.text.strip()

            # Extract URL
            link_elem = card.find_element(By.CSS_SELECTOR, "a[href*='/jobs'], a[href*='/company']")
            job_url = link_elem.get_attribute("href")
            if not job_url.startswith("http"):
                job_url = f"{self.base_url}{job_url}"

            # Extract location/remote info
            location = ""
            remote_policy = "unknown"
            try:
                location_elem = card.find_element(By.CSS_SELECTOR, ".location, [data-test='job-location']")
                location = location_elem.text.strip()
                remote_policy = self.extract_remote_policy(location, location)
            except NoSuchElementException:
                pass

            # Extract salary if available
            salary_min, salary_max, salary_disclosed = None, None, False
            try:
                salary_elem = card.find_element(By.CSS_SELECTOR, ".salary, [data-test='salary']")
                salary_text = salary_elem.text
                salary_min, salary_max, salary_disclosed = self.extract_salary_from_text(salary_text)
            except NoSuchElementException:
                pass

            # Extract company stage
            company_stage = "unknown"
            try:
                stage_elem = card.find_element(By.CSS_SELECTOR, ".stage, [data-test='stage']")
                stage_text = stage_elem.text.lower()
                if "seed" in stage_text:
                    company_stage = "seed"
                elif "series a" in stage_text:
                    company_stage = "series_a"
                elif "series b" in stage_text:
                    company_stage = "series_b"
                elif "series c" in stage_text:
                    company_stage = "series_c"
            except NoSuchElementException:
                pass

            # Get description (requires clicking through)
            description = ""
            # We'll skip full description for initial scrape to avoid too many requests

            job = JobPosting(
                company=company,
                role_title=title,
                job_url=job_url,
                description=description,
                remote_policy=remote_policy,
                location=location,
                salary_min=salary_min,
                salary_max=salary_max,
                salary_disclosed=salary_disclosed,
                company_stage=company_stage,
                source="wellfound",
                industry="tech"
            )

            return job

        except Exception as e:
            self.logger.error(f"Error extracting Wellfound job card: {e}")
            return None
