#!/usr/bin/env python3
"""
Main script for job search automation tool.
"""
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from models import JobPosting
from scoring_engine import JobScorer
from data_manager import DataManager
from resume_tailor import ResumeTailor
from cover_letter import CoverLetterGenerator
from portfolio_recommender import PortfolioRecommender
from scrapers import (
    LinkedInScraper,
    WellfoundScraper,
    BuiltInScraper,
    OttaScraper,
    RemoteCoScraper
)
import config


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOGS_DIR / f"job_search_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class JobSearchAutomation:
    """Main orchestrator for job search automation."""

    def __init__(self, enable_ai: bool = True):
        self.scorer = JobScorer()
        self.data_manager = DataManager()
        self.enable_ai = enable_ai

        # Initialize AI-powered modules
        if enable_ai:
            self.resume_tailor = ResumeTailor()
            self.cover_letter_gen = CoverLetterGenerator()
        else:
            self.resume_tailor = None
            self.cover_letter_gen = None

        self.portfolio_recommender = PortfolioRecommender()

        self.scrapers = {
            'linkedin': LinkedInScraper,
            'wellfound': WellfoundScraper,
            'builtin': BuiltInScraper,
            'otta': OttaScraper,
            'remote.co': RemoteCoScraper
        }

    def scrape_all_sites(self, search_terms: List[str] = None,
                         sites: List[str] = None) -> List[JobPosting]:
        """
        Scrape jobs from all configured sites.

        Args:
            search_terms: List of job titles to search for
            sites: List of site names to scrape (default: all)

        Returns:
            List of JobPosting objects
        """
        if search_terms is None:
            search_terms = config.TARGET_TITLES

        if sites is None:
            sites = list(self.scrapers.keys())

        all_jobs = []

        for site_name in sites:
            logger.info(f"Starting scrape of {site_name}...")

            try:
                scraper_class = self.scrapers[site_name]
                scraper = scraper_class(
                    headless=config.SCRAPER_CONFIG['headless'],
                    rate_limit_delay=config.SCRAPER_CONFIG['rate_limit_delay']
                )

                with scraper:
                    jobs = scraper.scrape(search_terms)
                    all_jobs.extend(jobs)
                    logger.info(f"Scraped {len(jobs)} jobs from {site_name}")

            except Exception as e:
                logger.error(f"Error scraping {site_name}: {e}", exc_info=True)
                continue

        logger.info(f"Total jobs scraped from all sites: {len(all_jobs)}")
        return all_jobs

    def filter_jobs(self, jobs: List[JobPosting]) -> List[JobPosting]:
        """
        Filter jobs based on basic criteria.

        Args:
            jobs: List of JobPosting objects

        Returns:
            Filtered list of JobPosting objects
        """
        filtered = []
        filtered_out = []

        for job in jobs:
            passes, failures = job.meets_basic_criteria()
            if passes:
                filtered.append(job)
            else:
                filtered_out.append((job, failures))
                logger.debug(f"Filtered out {job.company} - {job.role_title}: {', '.join(failures)}")

        logger.info(f"Filtered: {len(filtered)} jobs passed, {len(filtered_out)} jobs filtered out")
        return filtered

    def score_and_rank_jobs(self, jobs: List[JobPosting]):
        """
        Score and rank jobs.

        Args:
            jobs: List of JobPosting objects

        Returns:
            Sorted list of ScoredJob objects
        """
        logger.info(f"Scoring {len(jobs)} jobs...")
        scored_jobs = self.scorer.rank_jobs(jobs)

        # Filter by minimum score
        high_quality = self.scorer.filter_by_minimum_score(scored_jobs)
        logger.info(f"{len(high_quality)} jobs scored above threshold ({config.MIN_SCORE_THRESHOLD})")

        return scored_jobs, high_quality

    def generate_tailored_materials(self, scored_jobs):
        """
        Generate tailored materials (resume, cover letter, portfolio) for scored jobs.

        Args:
            scored_jobs: List of ScoredJob objects

        Returns:
            List of ScoredJob objects with tailored materials
        """
        logger.info(f"Generating tailored materials for {len(scored_jobs)} jobs...")

        for i, scored_job in enumerate(scored_jobs, 1):
            job = scored_job.job
            logger.info(f"  [{i}/{len(scored_jobs)}] Tailoring materials for {job.company} - {job.role_title}")

            try:
                # Generate resume bullets
                if self.resume_tailor:
                    resume_bullets = self.resume_tailor.tailor_resume(job)
                    scored_job.resume_bullets = resume_bullets
                    logger.debug(f"    Generated {len(resume_bullets)} resume bullets")

                # Generate cover letter
                if self.cover_letter_gen:
                    cover_letter = self.cover_letter_gen.generate_cover_letter(job)
                    scored_job.cover_letter = cover_letter
                    logger.debug(f"    Generated cover letter ({len(cover_letter)} chars)")

                # Generate portfolio recommendations
                portfolio_recs = self.portfolio_recommender.recommend_portfolio(job)
                scored_job.portfolio_recommendations = portfolio_recs
                logger.debug(f"    Generated {len(portfolio_recs)} portfolio recommendations")

            except Exception as e:
                logger.error(f"    Error generating materials for {job.company}: {e}")
                continue

        logger.info("Tailored materials generation complete")
        return scored_jobs

    def run_daily_search(self, search_terms: List[str] = None,
                        sites: List[str] = None,
                        save_results: bool = True):
        """
        Run complete daily job search.

        Args:
            search_terms: List of job titles to search for
            sites: List of site names to scrape
            save_results: Whether to save results to disk
        """
        logger.info("=" * 80)
        logger.info("Starting daily job search automation")
        logger.info("=" * 80)

        # 1. Scrape jobs
        logger.info("STEP 1: Scraping job sites...")
        all_jobs = self.scrape_all_sites(search_terms, sites)

        if save_results:
            self.data_manager.save_jobs(all_jobs)

        # 2. Filter jobs
        logger.info("STEP 2: Filtering jobs by basic criteria...")
        filtered_jobs = self.filter_jobs(all_jobs)

        # 3. Score and rank
        logger.info("STEP 3: Scoring and ranking jobs...")
        all_scored, high_quality = self.score_and_rank_jobs(filtered_jobs)

        if save_results:
            self.data_manager.save_scored_jobs(high_quality)

        # 4. Generate tailored materials
        if high_quality and self.enable_ai:
            logger.info("STEP 4: Generating tailored materials (resume, cover letter, portfolio)...")
            high_quality = self.generate_tailored_materials(high_quality)

            # Save individual job folders with materials
            if save_results:
                logger.info("Saving individual job folders...")
                for scored_job in high_quality:
                    self.data_manager.save_job_folder(scored_job)

        # 5. Generate digest
        logger.info(f"STEP {5 if self.enable_ai else 4}: Generating daily digest...")
        if high_quality:
            digest_path = self.data_manager.generate_daily_digest(high_quality[:10])
            logger.info(f"Daily digest saved to: {digest_path}")

            # Print top 5 to console
            print("\n" + "=" * 80)
            print("TOP 5 OPPORTUNITIES")
            print("=" * 80)
            for i, scored_job in enumerate(high_quality[:5], 1):
                job = scored_job.job
                print(f"\n{i}. {job.role_title} at {job.company}")
                print(f"   Score: {scored_job.score:.1f}/10")
                print(f"   Remote: {job.remote_policy} | Location: {job.location}")
                if job.salary_min:
                    print(f"   Salary: ${job.salary_min:,}+")
                print(f"   URL: {job.job_url}")
        else:
            logger.warning("No high-quality jobs found")

        logger.info("=" * 80)
        logger.info("Daily job search completed successfully")
        logger.info("=" * 80)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Job Search Automation Tool')
    parser.add_argument('--sites', nargs='+',
                       choices=['linkedin', 'wellfound', 'builtin', 'otta', 'remote.co'],
                       help='Specific sites to scrape')
    parser.add_argument('--test', action='store_true',
                       help='Run in test mode (single search term)')
    parser.add_argument('--no-save', action='store_true',
                       help='Do not save results to disk')
    parser.add_argument('--no-ai', action='store_true',
                       help='Disable AI-powered resume and cover letter generation')

    args = parser.parse_args()

    automation = JobSearchAutomation(enable_ai=not args.no_ai)

    if args.test:
        # Test mode - single search term
        search_terms = ["Director of Video"]
        sites = args.sites or ['wellfound']
    else:
        search_terms = None  # Use defaults from config
        sites = args.sites

    automation.run_daily_search(
        search_terms=search_terms,
        sites=sites,
        save_results=not args.no_save
    )


if __name__ == "__main__":
    main()
