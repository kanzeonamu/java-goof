"""
Remote.co job scraper.
"""
import time
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from models import JobPosting
from .base_scraper import BaseScraper
import config


class RemoteCoScraper(BaseScraper):
    """Scraper for Remote.co jobs."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://remote.co"

    def scrape(self, search_terms: List[str] = None) -> List[JobPosting]:
        """
        Scrape Remote.co jobs.

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
            self.logger.info(f"Searching Remote.co for: {term}")

            try:
                # Remote.co search URL
                url = f"{self.base_url}/remote-jobs/search/?search_keywords={term.replace(' ', '+')}"
                self.driver.get(url)
                time.sleep(3)

                # Scroll to load more jobs
                for _ in range(3):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                # Find job cards
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".job_listing, [data-title]")

                self.logger.info(f"Found {len(job_cards)} Remote.co job cards for '{term}'")

                for card in job_cards[:config.SCRAPER_CONFIG['max_results_per_site']]:
                    job = self._extract_job_from_card(card)
                    if job:
                        jobs.append(job)

                self.rate_limit()

            except Exception as e:
                self.logger.error(f"Error scraping Remote.co for '{term}': {e}")
                continue

        self.logger.info(f"Total Remote.co jobs scraped: {len(jobs)}")
        return jobs

    def _extract_job_from_card(self, card) -> Optional[JobPosting]:
        """Extract job details from a job card element."""
        try:
            # Extract title
            title_elem = card.find_element(By.CSS_SELECTOR, "h3, .job-title, [data-title]")
            title = title_elem.text.strip()

            # Extract company
            company_elem = card.find_element(By.CSS_SELECTOR, ".company, .company-name")
            company = company_elem.text.strip()

            # Extract URL
            link_elem = card.find_element(By.CSS_SELECTOR, "a")
            job_url = link_elem.get_attribute("href")
            if not job_url.startswith("http"):
                job_url = f"{self.base_url}{job_url}"

            # Extract location (usually "Anywhere" for remote.co)
            location = "Remote"
            try:
                location_elem = card.find_element(By.CSS_SELECTOR, ".location")
                location = location_elem.text.strip()
            except NoSuchElementException:
                pass

            # Remote.co is all remote jobs
            remote_policy = "remote"

            # Extract salary if available
            salary_min, salary_max, salary_disclosed = None, None, False
            try:
                salary_elem = card.find_element(By.CSS_SELECTOR, ".salary")
                salary_text = salary_elem.text
                salary_min, salary_max, salary_disclosed = self.extract_salary_from_text(salary_text)
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
                source="remote.co",
                industry="tech"
            )

            return job

        except Exception as e:
            self.logger.error(f"Error extracting Remote.co job card: {e}")
            return None
