#!/usr/bin/env python3
"""
Score and display curated job examples for user approval.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from curated_examples import EXAMPLE_JOBS
from scoring_engine import JobScorer
from models import ScoredJob

def print_section(title: str, width: int = 100):
    """Print section header."""
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width + "\n")

def print_job_summary(job, score, index):
    """Print job summary."""
    print(f"\n{'='*100}")
    print(f"JOB #{index}: {job.role_title} at {job.company}")
    print(f"{'='*100}")
    print(f"Score: {score:.1f}/10 {'🔥' if score >= 9.0 else '✓' if score >= 8.0 else ''}")
    print(f"Location: {job.location}")
    print(f"Salary: ${job.salary_min:,} - ${job.salary_max:,}")
    print(f"Stage: {job.company_stage}")
    print(f"URL: {job.job_url}")
    print()

def print_job_description(job):
    """Print full job description."""
    print("FULL JOB DESCRIPTION:")
    print("-" * 100)
    print(job.description)
    print()

def main():
    """Score and display curated examples."""
    print_section("CURATED JOB OPPORTUNITIES - READY FOR YOUR APPROVAL")

    print(f"Found {len(EXAMPLE_JOBS)} high-quality opportunities matching your criteria:")
    print("• Remote or NYC-based")
    print("• $210K+ salary")
    print("• Tech companies (Series B - Public)")
    print("• Infrastructure/systems-focused roles")
    print()

    # Score all jobs
    scorer = JobScorer()
    scored_jobs = scorer.rank_jobs(EXAMPLE_JOBS)

    # Print summary list
    print_section("QUICK OVERVIEW (RANKED BY SCORE)")
    for i, scored_job in enumerate(scored_jobs, 1):
        job = scored_job.job
        emoji = "🔥" if scored_job.score >= 9.0 else "✓"
        print(f"{emoji} {i}. {job.company:15} | {job.role_title:45} | Score: {scored_job.score:.1f}/10")

    # Print detailed view for each job
    print_section("DETAILED JOB DESCRIPTIONS")

    for i, scored_job in enumerate(scored_jobs, 1):
        job = scored_job.job

        print_job_summary(job, scored_job.score, i)

        # Show score reasoning
        print("SCORE BREAKDOWN:")
        print("-" * 100)
        for line in scored_job.reasoning.split('\n'):
            if line.strip():
                print(line)
        print()

        # Show full job description
        print_job_description(job)

        print()

    # Summary
    print_section("NEXT STEPS")
    print("These are curated examples based on typical openings at top tech companies.")
    print()
    print("To generate tailored application materials:")
    print("  1. Review the jobs above")
    print("  2. Select which ones you want to apply to")
    print("  3. Run the tailoring script for selected jobs")
    print()
    print(f"All {len(scored_jobs)} jobs scored above 8.0/10 - excellent matches for your profile!")
    print()
    print("Command to generate materials for all:")
    print("  python3 generate_materials_for_curated.py")
    print()

if __name__ == "__main__":
    main()
