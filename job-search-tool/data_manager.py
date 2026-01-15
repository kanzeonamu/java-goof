"""
Data persistence and management for job postings.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import logging

from models import JobPosting, ScoredJob
import config


class DataManager:
    """Manages storage and retrieval of job data."""

    def __init__(self, base_dir: Path = None):
        """
        Initialize data manager.

        Args:
            base_dir: Base directory for storing job data
        """
        self.base_dir = base_dir or config.JOBS_DIR
        self.logger = logging.getLogger(__name__)

    def save_jobs(self, jobs: List[JobPosting], date: str = None) -> str:
        """
        Save jobs to JSON file.

        Args:
            jobs: List of JobPosting objects
            date: Date string (YYYY-MM-DD), defaults to today

        Returns:
            Path to saved file
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        # Create date directory
        date_dir = self.base_dir / date
        date_dir.mkdir(parents=True, exist_ok=True)

        # Save to JSON
        filename = date_dir / "raw_jobs.json"
        jobs_data = [job.to_dict() for job in jobs]

        with open(filename, 'w') as f:
            json.dump(jobs_data, f, indent=2)

        self.logger.info(f"Saved {len(jobs)} jobs to {filename}")
        return str(filename)

    def save_scored_jobs(self, scored_jobs: List[ScoredJob], date: str = None) -> str:
        """
        Save scored jobs to JSON file.

        Args:
            scored_jobs: List of ScoredJob objects
            date: Date string (YYYY-MM-DD), defaults to today

        Returns:
            Path to saved file
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        # Create date directory
        date_dir = self.base_dir / date
        date_dir.mkdir(parents=True, exist_ok=True)

        # Save to JSON
        filename = date_dir / "scored_jobs.json"
        scored_data = [job.to_dict() for job in scored_jobs]

        with open(filename, 'w') as f:
            json.dump(scored_data, f, indent=2)

        self.logger.info(f"Saved {len(scored_jobs)} scored jobs to {filename}")
        return str(filename)

    def load_jobs(self, date: str = None) -> List[JobPosting]:
        """
        Load jobs from JSON file.

        Args:
            date: Date string (YYYY-MM-DD), defaults to today

        Returns:
            List of JobPosting objects
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        filename = self.base_dir / date / "raw_jobs.json"

        if not filename.exists():
            self.logger.warning(f"No jobs file found for {date}")
            return []

        with open(filename, 'r') as f:
            jobs_data = json.load(f)

        jobs = [JobPosting.from_dict(data) for data in jobs_data]
        self.logger.info(f"Loaded {len(jobs)} jobs from {filename}")
        return jobs

    def save_job_folder(self, scored_job: ScoredJob, date: str = None) -> str:
        """
        Save individual job to its own folder with all materials.

        Args:
            scored_job: ScoredJob object with tailored materials
            date: Date string (YYYY-MM-DD), defaults to today

        Returns:
            Path to job folder
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        # Create job folder
        company_slug = scored_job.job.company.lower().replace(' ', '-').replace('/', '-')
        job_dir = self.base_dir / date / company_slug
        job_dir.mkdir(parents=True, exist_ok=True)

        # Save job details
        with open(job_dir / "job_details.json", 'w') as f:
            json.dump(scored_job.to_dict(), f, indent=2)

        # Save tailored resume if available
        if scored_job.resume_bullets:
            with open(job_dir / "tailored_resume.md", 'w') as f:
                f.write("# Tailored Resume Bullets\n\n")
                for bullet in scored_job.resume_bullets:
                    f.write(f"- {bullet}\n")

        # Save cover letter if available
        if scored_job.cover_letter:
            with open(job_dir / "cover_letter.md", 'w') as f:
                f.write(scored_job.cover_letter)

        # Save portfolio recommendations if available
        if scored_job.portfolio_recommendations:
            with open(job_dir / "portfolio_recommendations.md", 'w') as f:
                f.write("# Recommended Portfolio Pieces\n\n")
                for rec in scored_job.portfolio_recommendations:
                    f.write(f"- {rec}\n")

        # Save application link
        with open(job_dir / "application_link.txt", 'w') as f:
            f.write(scored_job.job.job_url)

        self.logger.info(f"Saved job folder to {job_dir}")
        return str(job_dir)

    def generate_daily_digest(self, scored_jobs: List[ScoredJob], date: str = None) -> str:
        """
        Generate daily digest markdown file.

        Args:
            scored_jobs: List of ScoredJob objects (already ranked)
            date: Date string (YYYY-MM-DD), defaults to today

        Returns:
            Path to digest file
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        date_dir = self.base_dir / date
        date_dir.mkdir(parents=True, exist_ok=True)

        filename = date_dir / "daily_digest.md"

        with open(filename, 'w') as f:
            f.write(f"# Job Search Digest - {date}\n\n")
            f.write(f"**Total Opportunities:** {len(scored_jobs)}\n\n")
            f.write("---\n\n")

            for i, scored_job in enumerate(scored_jobs, 1):
                job = scored_job.job
                f.write(f"## {i}. {job.role_title} at {job.company}\n\n")
                f.write(f"**Score:** {scored_job.score:.1f}/10\n\n")
                f.write(f"**Location:** {job.location or 'Not specified'}\n\n")
                f.write(f"**Remote Policy:** {job.remote_policy}\n\n")

                if job.salary_min:
                    f.write(f"**Salary:** ${job.salary_min:,}")
                    if job.salary_max:
                        f.write(f" - ${job.salary_max:,}")
                    f.write("\n\n")

                if job.company_stage:
                    f.write(f"**Company Stage:** {job.company_stage}\n\n")

                f.write(f"**Source:** {job.source}\n\n")
                f.write(f"**Application Link:** [{job.job_url}]({job.job_url})\n\n")

                f.write("### Score Breakdown\n\n")
                f.write("```\n")
                f.write(scored_job.reasoning)
                f.write("\n```\n\n")

                if scored_job.portfolio_recommendations:
                    f.write("### Recommended Portfolio Pieces\n\n")
                    for rec in scored_job.portfolio_recommendations:
                        f.write(f"- {rec}\n")
                    f.write("\n")

                f.write("---\n\n")

        self.logger.info(f"Generated daily digest at {filename}")
        return str(filename)
