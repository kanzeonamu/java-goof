#!/usr/bin/env python3
"""
Test script with sample job data to demonstrate scoring engine.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from models import JobPosting
from scoring_engine import JobScorer
from data_manager import DataManager


# Sample job postings for testing
SAMPLE_JOBS = [
    JobPosting(
        company="Acme AI",
        role_title="Head of Creative Production",
        job_url="https://example.com/job1",
        description="""
        We're seeking a Head of Creative Production to build and scale our production infrastructure
        from the ground up. You'll design workflows, establish processes, and create systems that
        enable our creative team to deliver high-impact content at scale. This role requires strategic
        thinking, cross-functional leadership, and experience building production operations.

        Responsibilities:
        - Design and implement production infrastructure and workflows
        - Build and manage a team of producers and coordinators
        - Own budget and vendor management ($500K+ annual)
        - Partner with Product, Marketing, and Sales on strategic initiatives
        - Establish measurement frameworks for content impact
        - Scale operations to support 3x growth

        Requirements:
        - 8+ years production experience
        - Track record of building production functions
        - Experience with cross-functional stakeholder management
        - Budget ownership and P&L experience
        - Systems thinking and process design expertise
        """,
        remote_policy="remote",
        location="Remote (US)",
        salary_min=220000,
        salary_max=280000,
        salary_disclosed=True,
        company_stage="series_b",
        industry="tech",
        source="test"
    ),
    JobPosting(
        company="VideoTech Inc",
        role_title="Video Producer",
        job_url="https://example.com/job2",
        description="""
        Fast-paced startup seeking a hands-on video producer who can wear many hats!
        You'll be shooting, editing, and producing content daily. Must thrive in chaos
        and be willing to do whatever it takes to get the job done. No task is too small!

        Requirements:
        - Expert in Adobe Premiere, After Effects, Final Cut Pro
        - Able to operate cameras and lighting equipment
        - Experience shooting interviews and events
        - Self-starter who can hit the ground running
        - Comfortable working nights and weekends as needed
        """,
        remote_policy="onsite",
        location="San Francisco, CA",
        salary_min=85000,
        salary_max=110000,
        salary_disclosed=True,
        company_stage="seed",
        industry="tech",
        source="test"
    ),
    JobPosting(
        company="Scale Studios",
        role_title="Director of Content Operations",
        job_url="https://example.com/job3",
        description="""
        Join our growing team as Director of Content Operations. You'll oversee our production
        pipeline, manage agency relationships, and optimize workflows for efficiency. This role
        combines strategic planning with operational execution.

        Key responsibilities:
        - Manage production operations and workflows
        - Oversee 5-person internal team plus 3 agency partners
        - Own production budget (~$2M annually)
        - Partner with Marketing and Product teams
        - Implement scalable processes and automation
        - Track and report on content performance metrics

        Requirements:
        - 6+ years in production operations or similar role
        - Experience managing teams and vendors
        - Strong project management and systems thinking
        - Budget management experience
        """,
        remote_policy="remote",
        location="Remote",
        salary_min=None,  # Not disclosed
        salary_max=None,
        salary_disclosed=False,
        company_stage="series_a",
        industry="tech",
        source="test"
    ),
    JobPosting(
        company="Enterprise Corp",
        role_title="Senior Creative Producer",
        job_url="https://example.com/job4",
        description="""
        Enterprise Corp is looking for a Senior Creative Producer to execute on our
        content strategy. You'll produce video content, manage freelancers, and
        coordinate with stakeholders across the organization.

        This role requires:
        - Producing 10-15 videos per quarter
        - Managing freelance talent and vendors
        - Coordinating with internal teams
        - Some strategy and planning work
        """,
        remote_policy="hybrid",
        location="Boston, MA",
        salary_min=140000,
        salary_max=170000,
        salary_disclosed=True,
        company_stage="public",
        industry="tech",
        source="test"
    ),
    JobPosting(
        company="Growth Stage Tech",
        role_title="VP of Creative Operations",
        job_url="https://example.com/job5",
        description="""
        We're seeking a VP of Creative Operations to lead our creative production function.
        This is a high-impact role building the infrastructure, team, and processes to scale
        our content operations globally.

        What you'll do:
        - Build production infrastructure and operational excellence
        - Hire and lead team of 8-10 across production, design, and content
        - Own $3M+ budget with full P&L responsibility
        - Design scalable workflows and automation
        - Partner with executive team on strategic initiatives
        - Establish measurement frameworks for content ROI
        - Vendor and agency management at scale

        What we're looking for:
        - 10+ years in creative production leadership
        - Proven track record building production functions 0-to-1
        - Experience scaling teams and operations through hypergrowth
        - Deep expertise in production infrastructure and systems design
        - Cross-functional leadership with exec stakeholders
        - Revenue impact and business outcome orientation
        """,
        remote_policy="remote",
        location="NYC or Remote",
        salary_min=250000,
        salary_max=320000,
        salary_disclosed=True,
        company_stage="series_b",
        industry="tech",
        source="test"
    ),
    JobPosting(
        company="Startup XYZ",
        role_title="Creative Strategy Director",
        job_url="https://example.com/job6",
        description="""
        Startup XYZ needs a Creative Strategy Director to lead creative strategy and
        production for our demand generation campaigns. You'll develop concepts, manage
        agency partners, and ensure creative excellence.

        This role involves:
        - Developing creative strategies for campaigns
        - Managing creative agency relationships
        - Producing brand and product content
        - Some hands-on editing and production work
        - Fast-paced environment, self-starter mentality
        """,
        remote_policy="remote",
        location="Remote",
        salary_min=None,
        salary_max=None,
        salary_disclosed=False,
        company_stage="seed",
        industry="tech",
        source="test"
    ),
]


def main():
    """Run test scoring."""
    print("=" * 80)
    print("JOB SEARCH AUTOMATION - SCORING ENGINE TEST")
    print("=" * 80)
    print()

    # Initialize scorer
    scorer = JobScorer()
    data_manager = DataManager()

    # Score all jobs
    print(f"Scoring {len(SAMPLE_JOBS)} sample jobs...\n")
    scored_jobs = scorer.rank_jobs(SAMPLE_JOBS)

    # Display results
    print("=" * 80)
    print("SCORED AND RANKED RESULTS")
    print("=" * 80)
    print()

    for i, scored_job in enumerate(scored_jobs, 1):
        job = scored_job.job
        print(f"{i}. {job.role_title} at {job.company}")
        print(f"   Score: {scored_job.score:.1f}/10")
        print(f"   Remote: {job.remote_policy} | Location: {job.location}")

        if job.salary_min:
            print(f"   Salary: ${job.salary_min:,}", end="")
            if job.salary_max:
                print(f" - ${job.salary_max:,}", end="")
            print()
        else:
            print(f"   Salary: Not disclosed")

        print(f"   Stage: {job.company_stage}")
        print()
        print("   Score Breakdown:")
        for line in scored_job.reasoning.split('\n'):
            if line.strip():
                print(f"   {line}")
        print()
        print("-" * 80)
        print()

    # Filter by threshold
    high_quality = scorer.filter_by_minimum_score(scored_jobs)
    print(f"\n{len(high_quality)} jobs scored above threshold (6.0/10)")

    # Save results
    save_choice = input("\nSave results to disk? (y/n): ").strip().lower()
    if save_choice == 'y':
        date = "test-" + Path(__file__).stem
        data_manager.save_jobs(SAMPLE_JOBS, date=date)
        data_manager.save_scored_jobs(scored_jobs, date=date)
        digest_path = data_manager.generate_daily_digest(high_quality, date=date)
        print(f"\nResults saved to: {digest_path}")


if __name__ == "__main__":
    main()
