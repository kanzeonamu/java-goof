"""
LinkedIn job scraper.

WARNING: LinkedIn explicitly prohibits automated scraping in their Terms of Service.
This scraper is provided for educational purposes. For production use, consider:
1. Using LinkedIn's official Job Search API (requires partnership)
2. Manual exports from LinkedIn Recruiter
3. Third-party aggregators with LinkedIn partnerships
"""
import time
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from models import JobPosting
from .base_scraper import BaseScraper
import config


class LinkedInScraper(BaseScraper):
    """Scraper for LinkedIn jobs (use with caution - see module docstring)."""

    def __init__(self, username: str = None, password: str = None, **kwargs):
        """
        Initialize LinkedIn scraper.

        Args:
            username: LinkedIn username/email
            password: LinkedIn password
        """
        super().__init__(**kwargs)
        self.username = username or config.LINKEDIN_USERNAME
        self.password = password or config.LINKEDIN_PASSWORD
        self.base_url = "https://www.linkedin.com"
        self.logged_in = False

    def login(self) -> bool:
        """
        Login to LinkedIn.

        Returns:
            True if successful, False otherwise
        """
        if not self.username or not self.password:
            self.logger.warning("LinkedIn credentials not provided. Scraping will be limited.")
            return False

        try:
            self.driver.get(f"{self.base_url}/login")
            time.sleep(2)

            # Enter username
            username_field = self.driver.find_element(By.ID, "username")
            username_field.send_keys(self.username)

            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)

            time.sleep(5)

            # Check if login successful
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                self.logged_in = True
                self.logger.info("LinkedIn login successful")
                return True
            else:
                self.logger.warning("LinkedIn login may have failed - verify manually")
                return False

        except Exception as e:
            self.logger.error(f"LinkedIn login error: {e}")
            return False

    def build_search_url(self, search_term: str, remote_only: bool = True) -> str:
        """Build LinkedIn job search URL."""
        base = f"{self.base_url}/jobs/search"

        # URL parameters
        params = []
        params.append(f"keywords={search_term.replace(' ', '%20')}")
        params.append("location=United%20States")

        if remote_only:
            params.append("f_WT=2")  # Remote filter

        # Join parameters
        url = f"{base}?{'&'.join(params)}"
        return url

    def scrape(self, search_terms: List[str] = None) -> List[JobPosting]:
        """
        Scrape LinkedIn jobs.

        Args:
            search_terms: List of job titles to search for

        Returns:
            List of JobPosting objects
        """
        if search_terms is None:
            search_terms = config.TARGET_TITLES

        self.init_driver()

        # Attempt login
        if self.username and self.password:
            self.login()

        jobs = []

        for term in search_terms:
            self.logger.info(f"Searching LinkedIn for: {term}")

            try:
                url = self.build_search_url(term)
                self.driver.get(url)
                time.sleep(3)

                # Scroll to load more jobs
                for _ in range(3):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                # Extract job cards
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".job-search-card, .jobs-search-results__list-item")

                self.logger.info(f"Found {len(job_cards)} job cards for '{term}'")

                for card in job_cards[:config.SCRAPER_CONFIG['max_results_per_site']]:
                    job = self._extract_job_from_card(card)
                    if job:
                        jobs.append(job)

                self.rate_limit()

            except Exception as e:
                self.logger.error(f"Error scraping LinkedIn for '{term}': {e}")
                continue

        self.logger.info(f"Total LinkedIn jobs scraped: {len(jobs)}")
        return jobs

    def _extract_job_from_card(self, card) -> Optional[JobPosting]:
        """Extract job details from a job card element."""
        try:
            # Extract basic info
            title_elem = card.find_element(By.CSS_SELECTOR, ".base-search-card__title, h3")
            title = title_elem.text.strip()

            company_elem = card.find_element(By.CSS_SELECTOR, ".base-search-card__subtitle, h4")
            company = company_elem.text.strip()

            location_elem = card.find_element(By.CSS_SELECTOR, ".job-search-card__location, .job-card-container__metadata-item")
            location = location_elem.text.strip()

            # Get job URL
            link_elem = card.find_element(By.CSS_SELECTOR, "a.base-card__full-link, a[href*='/jobs/view/']")
            job_url = link_elem.get_attribute("href")

            # Try to get more details by clicking (if logged in)
            description = ""
            salary_min, salary_max, salary_disclosed = None, None, False

            if self.logged_in:
                try:
                    link_elem.click()
                    time.sleep(2)

                    # Extract description
                    desc_elem = self.driver.find_element(By.CSS_SELECTOR, ".show-more-less-html__markup, .jobs-description")
                    description = desc_elem.text.strip()

                    # Extract salary if available
                    try:
                        salary_elem = self.driver.find_element(By.CSS_SELECTOR, ".salary, .job-details-jobs-unified-top-card__job-insight")
                        salary_text = salary_elem.text
                        salary_min, salary_max, salary_disclosed = self.extract_salary_from_text(salary_text)
                    except NoSuchElementException:
                        pass

                    # Go back to list
                    self.driver.back()
                    time.sleep(1)

                except Exception as e:
                    self.logger.warning(f"Could not extract details for job: {e}")

            # Determine remote policy
            remote_policy = self.extract_remote_policy(f"{location} {description}", location)

            # Create job posting
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
                source="linkedin",
                industry="tech"  # Assume tech based on search
            )

            return job

        except Exception as e:
            self.logger.error(f"Error extracting job card: {e}")
            return None
