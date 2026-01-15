"""
Scoring engine for job postings.
Scores jobs 1-10 based on multiple criteria.
"""
from typing import Tuple
from models import JobPosting, ScoredJob
import config


class JobScorer:
    """Scores job postings based on defined criteria."""

    def __init__(self):
        self.weights = config.SCORING_WEIGHTS

    def score_job(self, job: JobPosting) -> ScoredJob:
        """
        Score a job posting from 1-10 based on multiple criteria.
        Returns ScoredJob with score and reasoning.
        """
        scores = {}
        reasoning_parts = []

        # 1. Role Alignment (30% weight)
        role_score, role_reasoning = self._score_role_alignment(job)
        scores['role_alignment'] = role_score
        reasoning_parts.append(f"Role Alignment ({role_score:.1f}/10): {role_reasoning}")

        # 2. Company Stage (20% weight)
        stage_score, stage_reasoning = self._score_company_stage(job)
        scores['company_stage'] = stage_score
        reasoning_parts.append(f"Company Stage ({stage_score:.1f}/10): {stage_reasoning}")

        # 3. Remote Policy (25% weight)
        remote_score, remote_reasoning = self._score_remote_policy(job)
        scores['remote_policy'] = remote_score
        reasoning_parts.append(f"Remote Policy ({remote_score:.1f}/10): {remote_reasoning}")

        # 4. Salary Transparency (10% weight)
        salary_score, salary_reasoning = self._score_salary_transparency(job)
        scores['salary_transparency'] = salary_score
        reasoning_parts.append(f"Salary Transparency ({salary_score:.1f}/10): {salary_reasoning}")

        # 5. Cultural Fit (15% weight)
        culture_score, culture_reasoning = self._score_cultural_fit(job)
        scores['cultural_fit'] = culture_score
        reasoning_parts.append(f"Cultural Fit ({culture_score:.1f}/10): {culture_reasoning}")

        # Calculate weighted final score
        final_score = sum(scores[key] * self.weights[key] for key in scores)
        final_score = round(final_score, 1)

        # Compile reasoning
        reasoning = "\n".join(reasoning_parts)
        reasoning += f"\n\nFinal Score: {final_score}/10"

        return ScoredJob(
            job=job,
            score=final_score,
            reasoning=reasoning
        )

    def _score_role_alignment(self, job: JobPosting) -> Tuple[float, str]:
        """
        Score how well the role aligns with production infrastructure vs execution.
        10 = Pure infrastructure/systems/strategic
        1 = Pure execution/IC work
        """
        description_lower = job.description.lower()
        title_lower = job.role_title.lower()
        combined_text = f"{title_lower} {description_lower}"

        # Count strategic vs execution keywords
        strategic_count = sum(1 for keyword in config.STRATEGIC_KEYWORDS if keyword in combined_text)
        execution_count = sum(1 for keyword in config.EXECUTION_KEYWORDS if keyword in combined_text)

        # Check for leadership indicators
        leadership_indicators = ["lead", "director", "head", "vp", "chief", "manage team"]
        has_leadership = any(indicator in title_lower for indicator in leadership_indicators)

        # Check for team building / hiring mentions
        has_team_building = any(phrase in description_lower for phrase in [
            "build team", "hire", "grow team", "scale team", "team of"
        ])

        # Base score calculation
        if strategic_count == 0 and execution_count > 3:
            score = 2.0
            reason = "Heavy execution focus, minimal strategic/infrastructure elements"
        elif strategic_count > execution_count * 2:
            score = 9.0
            reason = f"Strong infrastructure/systems focus ({strategic_count} strategic indicators)"
        elif strategic_count > execution_count:
            score = 7.0
            reason = f"Good strategic alignment ({strategic_count} strategic vs {execution_count} execution keywords)"
        elif strategic_count == execution_count:
            score = 5.0
            reason = "Mixed strategic and execution responsibilities"
        else:
            score = 3.0
            reason = f"More execution-focused ({execution_count} execution vs {strategic_count} strategic keywords)"

        # Boost for leadership role
        if has_leadership:
            score = min(10.0, score + 1.0)
            reason += ", leadership role"

        # Boost for team building
        if has_team_building:
            score = min(10.0, score + 0.5)
            reason += ", includes team building"

        return (score, reason)

    def _score_company_stage(self, job: JobPosting) -> Tuple[float, str]:
        """
        Score company stage (earlier = better).
        """
        if not job.company_stage or job.company_stage == "unknown":
            return (5.0, "Stage unknown, neutral score")

        stage_lower = job.company_stage.lower()

        # Map to config scores
        if "seed" in stage_lower:
            return (10.0, "Seed stage (preferred)")
        elif "series a" in stage_lower or "series_a" in stage_lower:
            return (9.0, "Series A (highly preferred)")
        elif "series b" in stage_lower or "series_b" in stage_lower:
            return (8.0, "Series B (preferred)")
        elif "series c" in stage_lower or "series_c" in stage_lower:
            return (6.0, "Series C (acceptable)")
        elif "series d" in stage_lower or "series_d" in stage_lower:
            return (5.0, "Series D (late stage)")
        elif "public" in stage_lower or "ipo" in stage_lower:
            return (3.0, "Public company (less preferred)")
        else:
            return (5.0, f"Stage '{job.company_stage}' unclear")

    def _score_remote_policy(self, job: JobPosting) -> Tuple[float, str]:
        """
        Score remote policy. Remote is required.
        """
        policy_lower = job.remote_policy.lower()
        location_lower = (job.location or "").lower()

        if "remote" in policy_lower or "remote" in location_lower:
            # Check if it's remote first or remote optional
            if "remote first" in policy_lower or "fully remote" in policy_lower:
                return (10.0, "Fully remote (required)")
            else:
                return (9.0, "Remote (required)")

        # Check for NYC location
        if "nyc" in location_lower or "new york" in location_lower:
            if "hybrid" in policy_lower:
                return (7.0, "Hybrid in NYC (acceptable)")
            else:
                return (5.0, "NYC-based (acceptable)")

        # Unknown - give benefit of doubt
        if policy_lower == "unknown" or not policy_lower:
            return (6.0, "Remote policy unclear (needs verification)")

        # Hybrid outside NYC
        if "hybrid" in policy_lower:
            return (3.0, "Hybrid outside NYC (not ideal)")

        # Onsite
        return (0.0, "Not remote (dealbreaker)")

    def _score_salary_transparency(self, job: JobPosting) -> Tuple[float, str]:
        """
        Score salary transparency and adequacy.
        """
        if job.salary_min and job.salary_min >= 210000:
            return (10.0, f"Salary disclosed and meets minimum: ${job.salary_min:,}+")
        elif job.salary_min and job.salary_min < 210000:
            return (1.0, f"Salary too low: ${job.salary_min:,} (below $210k minimum)")
        elif job.salary_disclosed:
            return (5.0, "Salary disclosed but amount unclear")
        else:
            return (6.0, "Salary not disclosed (common for senior roles)")

    def _score_cultural_fit(self, job: JobPosting) -> Tuple[float, str]:
        """
        Score cultural fit based on red flags and positive indicators.
        """
        description_lower = job.description.lower()

        # Count red flags
        red_flags_found = [flag for flag in config.RED_FLAGS if flag.lower() in description_lower]

        # Count positive indicators
        positive_found = [indicator for indicator in config.POSITIVE_INDICATORS
                         if indicator.lower() in description_lower]

        # Base score
        score = 7.0

        # Penalize for red flags
        if len(red_flags_found) >= 3:
            score -= 3.0
            reason = f"Multiple red flags detected: {', '.join(red_flags_found[:3])}"
        elif len(red_flags_found) == 2:
            score -= 2.0
            reason = f"Some red flags: {', '.join(red_flags_found)}"
        elif len(red_flags_found) == 1:
            score -= 1.0
            reason = f"Minor red flag: {red_flags_found[0]}"
        else:
            reason = "No obvious red flags"

        # Boost for positive indicators
        if len(positive_found) >= 5:
            score += 2.0
            reason += f", strong positive indicators ({len(positive_found)} found)"
        elif len(positive_found) >= 3:
            score += 1.0
            reason += f", good positive indicators ({len(positive_found)} found)"

        score = max(0.0, min(10.0, score))

        return (score, reason)

    def rank_jobs(self, jobs: list[JobPosting]) -> list[ScoredJob]:
        """
        Score and rank multiple jobs.
        Returns list of ScoredJob objects sorted by score (highest first).
        """
        scored_jobs = [self.score_job(job) for job in jobs]
        scored_jobs.sort(key=lambda x: x.score, reverse=True)
        return scored_jobs

    def filter_by_minimum_score(self, scored_jobs: list[ScoredJob],
                                 min_score: float = None) -> list[ScoredJob]:
        """
        Filter jobs by minimum score threshold.
        """
        if min_score is None:
            min_score = config.MIN_SCORE_THRESHOLD

        return [job for job in scored_jobs if job.score >= min_score]
