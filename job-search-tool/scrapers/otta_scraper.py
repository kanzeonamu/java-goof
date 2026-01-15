"""
Otta job scraper.
"""
import time
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from models import JobPosting
from .base_scraper import BaseScraper
import config


class OttaScraper(BaseScraper):
    """Scraper for Otta jobs."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://otta.com"

    def scrape(self, search_terms: List[str] = None) -> List[JobPosting]:
        """
        Scrape Otta jobs.

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
            self.logger.info(f"Searching Otta for: {term}")

            try:
                # Otta search URL
                url = f"{self.base_url}/jobs?q={term.replace(' ', '+')}"
                self.driver.get(url)
                time.sleep(3)

                # Scroll to load more jobs
                for _ in range(3):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                # Find job cards
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='job-card'], .job-card")

                self.logger.info(f"Found {len(job_cards)} Otta job cards for '{term}'")

                for card in job_cards[:config.SCRAPER_CONFIG['max_results_per_site']]:
                    job = self._extract_job_from_card(card)
                    if job:
                        jobs.append(job)

                self.rate_limit()

            except Exception as e:
                self.logger.error(f"Error scraping Otta for '{term}': {e}")
                continue

        self.logger.info(f"Total Otta jobs scraped: {len(jobs)}")
        return jobs

    def _extract_job_from_card(self, card) -> Optional[JobPosting]:
        """Extract job details from a job card element."""
        try:
            # Extract title
            title_elem = card.find_element(By.CSS_SELECTOR, "h2, h3, .job-title")
            title = title_elem.text.strip()

            # Extract company
            company_elem = card.find_element(By.CSS_SELECTOR, ".company-name, [data-testid='company-name']")
            company = company_elem.text.strip()

            # Extract URL
            link_elem = card.find_element(By.CSS_SELECTOR, "a")
            job_url = link_elem.get_attribute("href")
            if not job_url.startswith("http"):
                job_url = f"{self.base_url}{job_url}"

            # Extract location
            location = ""
            try:
                location_elem = card.find_element(By.CSS_SELECTOR, ".location, [data-testid='location']")
                location = location_elem.text.strip()
            except NoSuchElementException:
                pass

            # Determine remote policy
            remote_policy = self.extract_remote_policy(card.text, location)

            # Extract salary if available
            salary_min, salary_max, salary_disclosed = None, None, False
            try:
                salary_elem = card.find_element(By.CSS_SELECTOR, ".salary, [data-testid='salary']")
                salary_text = salary_elem.text
                salary_min, salary_max, salary_disclosed = self.extract_salary_from_text(salary_text)
            except NoSuchElementException:
                pass

            # Extract company stage
            company_stage = "unknown"
            try:
                stage_elem = card.find_element(By.CSS_SELECTOR, ".stage, [data-testid='stage']")
                stage_text = stage_elem.text.lower()
                if "seed" in stage_text:
                    company_stage = "seed"
                elif "series a" in stage_text:
                    company_stage = "series_a"
                elif "series b" in stage_text:
                    company_stage = "series_b"
            except NoSuchElementException:
                pass

            job = JobPosting(
                company=company,
                role_title=title,
                job_url=job_url,
                description="",
                remote_policy=remote_policy,
                location=location,
                salary_min=salary_min,
                salary_max=salary_max,
                salary_disclosed=salary_disclosed,
                company_stage=company_stage,
                source="otta",
                industry="tech"
            )

            return job

        except Exception as e:
            self.logger.error(f"Error extracting Otta job card: {e}")
            return None
