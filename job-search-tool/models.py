"""
Data models for job search automation tool.
"""
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict
from datetime import datetime
import json


@dataclass
class JobPosting:
    """Represents a job posting."""
    company: str
    role_title: str
    job_url: str
    description: str
    remote_policy: str  # "remote", "hybrid", "onsite", "unknown"
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_disclosed: bool = False
    company_stage: Optional[str] = None  # "seed", "series_a", "series_b", "series_c+", "public", "unknown"
    industry: Optional[str] = None
    source: str = ""  # "linkedin", "wellfound", "builtin", "otta", "remote.co"
    posted_date: Optional[str] = None
    scraped_date: str = datetime.now().isoformat()

    # Scoring fields
    score: Optional[float] = None
    score_reasoning: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: Dict) -> 'JobPosting':
        """Create from dictionary."""
        return cls(**data)

    def meets_basic_criteria(self) -> tuple[bool, List[str]]:
        """
        Check if job meets basic filtering criteria.
        Returns (passes, reasons_for_failure).
        """
        failures = []

        # Remote requirement
        if self.remote_policy not in ["remote", "unknown"]:
            if not (self.location and "nyc" in self.location.lower()):
                failures.append(f"Not remote (policy: {self.remote_policy}, location: {self.location})")

        # Salary minimum (only exclude if known to be lower)
        if self.salary_min is not None and self.salary_min < 210000:
            failures.append(f"Salary too low: ${self.salary_min:,}")

        # Industry check (basic tech keywords)
        if self.industry and self.industry.lower() not in ["tech", "technology", "software", "saas", "unknown"]:
            if not any(keyword in self.description.lower() for keyword in ["software", "saas", "platform", "tech", "startup"]):
                failures.append(f"Non-tech company: {self.industry}")

        return (len(failures) == 0, failures)


@dataclass
class ScoredJob:
    """Represents a scored job with tailored materials."""
    job: JobPosting
    score: float
    reasoning: str
    resume_bullets: Optional[List[str]] = None
    cover_letter: Optional[str] = None
    portfolio_recommendations: Optional[List[str]] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "job": self.job.to_dict(),
            "score": self.score,
            "reasoning": self.reasoning,
            "resume_bullets": self.resume_bullets,
            "cover_letter": self.cover_letter,
            "portfolio_recommendations": self.portfolio_recommendations
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class ScraperConfig:
    """Configuration for web scrapers."""
    linkedin_username: Optional[str] = None
    linkedin_password: Optional[str] = None
    headless: bool = True
    timeout: int = 30
    max_results_per_site: int = 50
    rate_limit_delay: int = 2  # seconds between requests
