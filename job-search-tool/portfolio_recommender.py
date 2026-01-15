"""
Portfolio recommendation engine.
Recommends which portfolio pieces to highlight based on job description.
"""
import logging
from typing import List, Dict

from models import JobPosting
import config


logger = logging.getLogger(__name__)


class PortfolioRecommender:
    """Recommends portfolio pieces based on job requirements."""

    def __init__(self):
        """Initialize portfolio recommender."""
        self.portfolio_pieces = config.PORTFOLIO_PIECES

    def recommend_portfolio(self, job: JobPosting, max_recommendations: int = 3) -> List[str]:
        """
        Recommend portfolio pieces for a job posting.

        Args:
            job: JobPosting object
            max_recommendations: Maximum number of pieces to recommend

        Returns:
            List of recommendation strings with descriptions
        """
        # Score each portfolio piece
        scored_pieces = []

        for piece_id, piece_info in self.portfolio_pieces.items():
            score = self._score_portfolio_piece(piece_info, job)
            scored_pieces.append((score, piece_info))

        # Sort by score and take top N
        scored_pieces.sort(reverse=True, key=lambda x: x[0])

        # Format recommendations
        recommendations = []
        for score, piece_info in scored_pieces[:max_recommendations]:
            rec = self._format_recommendation(piece_info, score)
            recommendations.append(rec)

        return recommendations

    def _score_portfolio_piece(self, piece_info: Dict, job: JobPosting) -> float:
        """Score how well a portfolio piece matches a job."""
        score = 0.0
        job_text = f"{job.role_title} {job.description}".lower()

        # Check if any of the piece's keywords match the job
        for keyword in piece_info.get("best_for", []):
            if keyword.lower() in job_text:
                score += 2.0

        # Bonus scoring based on specific job characteristics
        description_lower = job.description.lower()

        # Elastic video - good for strategic/executive/brand roles
        if piece_info["title"] == "Elastic 'Evolving Search' Hero Video":
            if any(word in job_text for word in ["strategic", "executive", "ceo", "leadership", "brand", "narrative"]):
                score += 3.0
            if "product marketing" in job_text or "brand marketing" in job_text:
                score += 2.0

        # Snyk AR game - good for experiential/demand gen roles
        elif piece_info["title"] == "Snyk AR Game (Experiential)":
            if any(word in job_text for word in ["experiential", "event", "demand gen", "lead gen", "mql", "innovative"]):
                score += 3.0
            if "creative" in job_text and "campaign" in job_text:
                score += 2.0

        # InVision Squads - good for customer story/revenue roles
        elif piece_info["title"] == "InVision 'Squads' Documentary":
            if any(word in job_text for word in ["customer", "case study", "revenue", "sales enablement", "documentary"]):
                score += 3.0
            if "saas" in job_text or "b2b" in job_text:
                score += 2.0

        # InVision Learn - good for educational/platform roles
        elif piece_info["title"] == "InVision Learn Platform":
            if any(word in job_text for word in ["education", "learning", "training", "platform", "course", "scalable"]):
                score += 3.0
            if "content" in job_text and ("scale" in job_text or "system" in job_text):
                score += 2.0

        # Boost for revenue-focused roles
        if "revenue" in description_lower or "roi" in description_lower or "business impact" in description_lower:
            if "revenue" in piece_info["description"].lower():
                score += 1.5

        # Boost for scale/systems roles
        if "scale" in description_lower or "infrastructure" in description_lower or "systems" in description_lower:
            if piece_info["title"] in ["Elastic 'Evolving Search' Hero Video", "InVision Learn Platform"]:
                score += 1.0

        return score

    def _format_recommendation(self, piece_info: Dict, score: float) -> str:
        """Format portfolio piece recommendation."""
        title = piece_info["title"]
        description = piece_info["description"]
        url = piece_info["url"]

        return f"**{title}** - {description}\n   View: {url}"

    def get_all_portfolio_pieces(self) -> str:
        """Get formatted string of all portfolio pieces."""
        output = "## Portfolio Highlights\n\n"

        for piece_info in self.portfolio_pieces.values():
            output += f"### {piece_info['title']}\n"
            output += f"{piece_info['description']}\n"
            output += f"[View Work]({piece_info['url']})\n\n"

        return output

    def get_portfolio_summary_for_job(self, job: JobPosting) -> str:
        """
        Get formatted portfolio summary tailored to a specific job.

        Args:
            job: JobPosting object

        Returns:
            Formatted markdown string
        """
        recommendations = self.recommend_portfolio(job, max_recommendations=3)

        output = f"## Recommended Portfolio Pieces for {job.company}\n\n"
        output += "Based on the job description, here are the most relevant portfolio pieces:\n\n"

        for i, rec in enumerate(recommendations, 1):
            output += f"{i}. {rec}\n\n"

        output += "\n### Additional Portfolio\n\n"
        output += "Full portfolio and case studies available at: https://loffilms.com/videostrategy\n\n"
        output += "Notable work includes:\n"
        output += "- Featured on HBO, The New York Times Op-Docs, VOX.com, PBS\n"
        output += "- Screened at Tribeca, SXSW, Cannes, The New York Film Festival\n"
        output += "- Platinum Award Best Documentary (Marcom Awards)\n"
        output += "- Gold Winner Marketing Material (Marcom Awards)\n"

        return output
