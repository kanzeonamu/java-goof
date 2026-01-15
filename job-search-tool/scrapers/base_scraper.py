"""
Base scraper class with common functionality.
"""
import time
import logging
from abc import ABC, abstractmethod
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup

from models import JobPosting
import config


class BaseScraper(ABC):
    """Base class for job site scrapers."""

    def __init__(self, headless: bool = True, rate_limit_delay: int = 2):
        """
        Initialize scraper.

        Args:
            headless: Run browser in headless mode
            rate_limit_delay: Delay between requests in seconds
        """
        self.headless = headless
        self.rate_limit_delay = rate_limit_delay
        self.logger = logging.getLogger(self.__class__.__name__)
        self.driver: Optional[webdriver.Chrome] = None

    def init_driver(self):
        """Initialize Selenium WebDriver."""
        if self.driver is not None:
            return

        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'user-agent={config.SCRAPER_CONFIG["user_agent"]}')
        options.add_argument('--disable-blink-features=AutomationControlled')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)

    def close_driver(self):
        """Close WebDriver."""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def wait_and_find(self, by: By, value: str, timeout: int = 10):
        """Wait for element and return it."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def rate_limit(self):
        """Apply rate limiting between requests."""
        time.sleep(self.rate_limit_delay)

    def get_page_with_requests(self, url: str, headers: Optional[dict] = None) -> Optional[BeautifulSoup]:
        """
        Fetch page using requests library (for sites that don't need JS rendering).

        Args:
            url: URL to fetch
            headers: Optional HTTP headers

        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            if headers is None:
                headers = {
                    'User-Agent': config.SCRAPER_CONFIG["user_agent"]
                }

            response = requests.get(url, headers=headers, timeout=config.SCRAPER_CONFIG["timeout"])
            response.raise_for_status()

            self.rate_limit()
            return BeautifulSoup(response.content, 'lxml')

        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    @abstractmethod
    def scrape(self, search_terms: List[str]) -> List[JobPosting]:
        """
        Scrape jobs from the site.

        Args:
            search_terms: List of search terms/job titles to search for

        Returns:
            List of JobPosting objects
        """
        pass

    def extract_salary_from_text(self, text: str) -> tuple[Optional[int], Optional[int], bool]:
        """
        Extract salary range from text.

        Returns:
            (min_salary, max_salary, is_disclosed)
        """
        import re

        if not text:
            return (None, None, False)

        text_lower = text.lower()

        # Look for salary patterns
        # Pattern 1: $200k - $250k
        pattern1 = r'\$(\d{1,3})[kK][\s-]+\$?(\d{1,3})[kK]'
        # Pattern 2: $200,000 - $250,000
        pattern2 = r'\$(\d{1,3}),?(\d{3}),?(\d{3})[\s-]+\$?(\d{1,3}),?(\d{3}),?(\d{3})'
        # Pattern 3: 200k-250k
        pattern3 = r'(\d{1,3})[kK][\s-]+(\d{1,3})[kK]'

        match = re.search(pattern1, text)
        if match:
            min_sal = int(match.group(1)) * 1000
            max_sal = int(match.group(2)) * 1000
            return (min_sal, max_sal, True)

        match = re.search(pattern2, text)
        if match:
            min_sal = int(match.group(1) + match.group(2) + match.group(3))
            max_sal = int(match.group(4) + match.group(5) + match.group(6))
            return (min_sal, max_sal, True)

        match = re.search(pattern3, text)
        if match:
            min_sal = int(match.group(1)) * 1000
            max_sal = int(match.group(2)) * 1000
            return (min_sal, max_sal, True)

        return (None, None, False)

    def extract_remote_policy(self, text: str, location: str = "") -> str:
        """
        Extract remote policy from text and location.

        Returns:
            "remote", "hybrid", "onsite", or "unknown"
        """
        if not text:
            text = ""

        combined = f"{text} {location}".lower()

        if any(keyword in combined for keyword in ["remote first", "fully remote", "100% remote"]):
            return "remote"
        elif "remote" in combined:
            return "remote"
        elif "hybrid" in combined:
            return "hybrid"
        elif any(keyword in combined for keyword in ["on-site", "onsite", "in-office"]):
            return "onsite"
        else:
            return "unknown"

    def __enter__(self):
        """Context manager entry."""
        self.init_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_driver()
