"""
Web scrapers for different job sites.
"""
from .base_scraper import BaseScraper
from .linkedin_scraper import LinkedInScraper
from .wellfound_scraper import WellfoundScraper
from .builtin_scraper import BuiltInScraper
from .otta_scraper import OttaScraper
from .remote_co_scraper import RemoteCoScraper

__all__ = [
    'BaseScraper',
    'LinkedInScraper',
    'WellfoundScraper',
    'BuiltInScraper',
    'OttaScraper',
    'RemoteCoScraper'
]
