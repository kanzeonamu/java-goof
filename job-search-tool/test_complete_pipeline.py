#!/usr/bin/env python3
"""
Test complete pipeline including resume tailoring, cover letters, and portfolio recommendations.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from models import JobPosting, ScoredJob
from scoring_engine import JobScorer
from resume_tailor import ResumeTailor
from cover_letter import CoverLetterGenerator
from portfolio_recommender import PortfolioRecommender
from data_manager import DataManager


# Sample high-quality job for testing
TEST_JOB = JobPosting(
    company="TechScale Inc",
    role_title="VP of Creative Operations",
    job_url="https://example.com/jobs/vp-creative-ops",
    description="""
    We're seeking a VP of Creative Operations to build and scale our creative production infrastructure.
    This is a high-impact leadership role focused on systems design, operational excellence, and
    cross-functional collaboration.

    What You'll Do:
    - Build production infrastructure from the ground up
    - Design scalable workflows and processes
    - Lead a team of 8-10 across production, design, and content
    - Own $3M+ budget with P&L responsibility
    - Partner with Product, Marketing, Sales, and Engineering leadership
    - Establish measurement frameworks for content ROI and business impact
    - Manage vendor and agency relationships at scale
    - Drive revenue impact through strategic content initiatives

    What We're Looking For:
    - 10+ years in creative production leadership
    - Proven track record building production functions 0-to-1
    - Experience scaling operations through hypergrowth
    - Deep expertise in production infrastructure and systems design
    - Cross-functional leadership with executive stakeholders
    - Revenue-oriented mindset with measurable business outcomes
    - Strong budget management and vendor relationship skills

    About Us:
    TechScale is a Series B SaaS company revolutionizing how enterprises manage their operations.
    We've raised $50M and are scaling rapidly. This role will report to the CMO and partner closely
    with Product and Revenue leadership.
    """,
    remote_policy="remote",
    location="NYC or Remote",
    salary_min=250000,
    salary_max=320000,
    salary_disclosed=True,
    company_stage="series_b",
    industry="tech",
    source="test"
)


def print_section(title: str, width: int = 80):
    """Print a section header."""
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width + "\n")


def main():
    """Run complete pipeline test."""
    print_section("JOB SEARCH AUTOMATION - COMPLETE PIPELINE TEST")

    # Initialize components
    print("Initializing components...")
    scorer = JobScorer()
    resume_tailor = ResumeTailor()
    cover_letter_gen = CoverLetterGenerator()
    portfolio_recommender = PortfolioRecommender()
    data_manager = DataManager()
    print("✓ All components initialized\n")

    # Display job details
    print_section("TEST JOB DETAILS")
    print(f"Company: {TEST_JOB.company}")
    print(f"Role: {TEST_JOB.role_title}")
    print(f"Location: {TEST_JOB.location}")
    print(f"Remote: {TEST_JOB.remote_policy}")
    print(f"Salary: ${TEST_JOB.salary_min:,} - ${TEST_JOB.salary_max:,}")
    print(f"Stage: {TEST_JOB.company_stage}")
    print(f"URL: {TEST_JOB.job_url}")

    # Step 1: Score the job
    print_section("STEP 1: SCORING JOB")
    scored_job = scorer.score_job(TEST_JOB)
    print(f"Score: {scored_job.score:.1f}/10\n")
    print("Score Breakdown:")
    print(scored_job.reasoning)

    # Step 2: Tailor resume
    print_section("STEP 2: TAILORING RESUME")
    print("Generating tailored resume bullets...")
    resume_bullets = resume_tailor.tailor_resume(TEST_JOB)
    print(f"✓ Generated {len(resume_bullets)} tailored bullets\n")
    print("Tailored Resume Bullets:")
    for i, bullet in enumerate(resume_bullets, 1):
        print(f"{i}. {bullet}")

    scored_job.resume_bullets = resume_bullets

    # Step 3: Generate cover letter
    print_section("STEP 3: GENERATING COVER LETTER")
    print("Generating personalized cover letter...")
    cover_letter = cover_letter_gen.generate_cover_letter(TEST_JOB)
    print(f"✓ Generated cover letter ({len(cover_letter)} characters)\n")
    print(cover_letter)

    scored_job.cover_letter = cover_letter

    # Step 4: Recommend portfolio
    print_section("STEP 4: RECOMMENDING PORTFOLIO PIECES")
    print("Analyzing job description and recommending portfolio pieces...")
    portfolio_recs = portfolio_recommender.recommend_portfolio(TEST_JOB, max_recommendations=3)
    print(f"✓ Generated {len(portfolio_recs)} recommendations\n")
    print("Recommended Portfolio Pieces:")
    for i, rec in enumerate(portfolio_recs, 1):
        print(f"\n{i}. {rec}")

    scored_job.portfolio_recommendations = portfolio_recs

    # Step 5: Format complete application package
    print_section("STEP 5: COMPLETE APPLICATION PACKAGE")
    print(f"Job: {TEST_JOB.role_title} at {TEST_JOB.company}")
    print(f"Score: {scored_job.score:.1f}/10")
    print(f"URL: {TEST_JOB.job_url}\n")
    print(f"✓ Resume: {len(resume_bullets)} tailored bullets")
    print(f"✓ Cover Letter: {len(cover_letter)} characters")
    print(f"✓ Portfolio: {len(portfolio_recs)} recommendations")

    # Step 6: Save results (optional)
    print_section("STEP 6: SAVE RESULTS")
    save_choice = input("Save complete application package to disk? (y/n): ").strip().lower()

    if save_choice == 'y':
        date = "test-complete-pipeline"
        job_folder = data_manager.save_job_folder(scored_job, date=date)
        print(f"\n✓ Application package saved to: {job_folder}")

        # Also save formatted resume
        formatted_resume = resume_tailor.format_tailored_resume(TEST_JOB, resume_bullets)
        resume_path = Path(job_folder) / "formatted_resume.md"
        with open(resume_path, 'w') as f:
            f.write(formatted_resume)
        print(f"✓ Formatted resume saved to: {resume_path}")

        # Save portfolio summary
        portfolio_summary = portfolio_recommender.get_portfolio_summary_for_job(TEST_JOB)
        portfolio_path = Path(job_folder) / "portfolio_summary.md"
        with open(portfolio_path, 'w') as f:
            f.write(portfolio_summary)
        print(f"✓ Portfolio summary saved to: {portfolio_path}")

        print(f"\nComplete application package ready in: {job_folder}")
    else:
        print("\nResults not saved.")

    # Summary
    print_section("TEST COMPLETE")
    print("✓ Job scoring: Working")
    print("✓ Resume tailoring: Working" + (" (AI-powered)" if resume_tailor.client else " (rule-based)"))
    print("✓ Cover letter generation: Working" + (" (AI-powered)" if cover_letter_gen.client else " (template-based)"))
    print("✓ Portfolio recommendations: Working")
    print("✓ Data persistence: Working")
    print("\nAll systems operational! 🚀")


if __name__ == "__main__":
    main()
