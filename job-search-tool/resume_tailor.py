"""
Resume tailoring module.
Extracts and tailors resume content to match job descriptions.
"""
import logging
from typing import List, Optional
import anthropic

from models import JobPosting
import config


logger = logging.getLogger(__name__)


class ResumeTailor:
    """Tailors resume content to specific job postings."""

    def __init__(self, api_key: str = None):
        """
        Initialize resume tailor.

        Args:
            api_key: Anthropic API key (defaults to config)
        """
        self.api_key = api_key or config.ANTHROPIC_API_KEY
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("No Anthropic API key provided. Resume tailoring will use rule-based fallback.")

    def tailor_resume(self, job: JobPosting, resume_text: str = None) -> List[str]:
        """
        Generate tailored resume bullets for a specific job.

        Args:
            job: JobPosting object
            resume_text: Full resume text (optional, uses default profile if not provided)

        Returns:
            List of 5-7 tailored resume bullets
        """
        if resume_text is None:
            resume_text = self._get_default_resume_content()

        if self.client:
            try:
                return self._tailor_with_ai(job, resume_text)
            except Exception as e:
                logger.error(f"Error using AI for resume tailoring: {e}")
                logger.info("Falling back to rule-based tailoring")
                return self._tailor_rule_based(job, resume_text)
        else:
            return self._tailor_rule_based(job, resume_text)

    def _tailor_with_ai(self, job: JobPosting, resume_text: str) -> List[str]:
        """Use AI to tailor resume content."""
        prompt = f"""You are helping tailor a resume for a specific job application.

Job Details:
Company: {job.company}
Role: {job.role_title}
Description: {job.description}

Full Resume/Experience:
{resume_text}

Task: Extract and select 5-7 most relevant bullets from the resume that best match this job description.

Requirements:
1. Choose bullets that emphasize:
   - Systems design and infrastructure building (not just execution)
   - Cross-functional delivery and leadership
   - Measurable business impact (revenue, growth metrics)
   - Team building and organizational development
   - Budget ownership and operational authority

2. Prioritize bullets that match keywords in the job description
3. Focus on strategic accomplishments over tactical execution
4. Include specific metrics and outcomes where possible
5. Return ONLY the selected bullets, one per line
6. Each bullet should start with a strong action verb
7. Keep each bullet concise but impactful (1-2 lines max)

Return the bullets as a numbered list."""

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Parse response
        response_text = message.content[0].text
        bullets = self._parse_bullets_from_response(response_text)

        return bullets

    def _tailor_rule_based(self, job: JobPosting, resume_text: str) -> List[str]:
        """Rule-based resume tailoring as fallback."""
        # Get default bullets
        all_bullets = self._get_all_resume_bullets()

        # Score each bullet based on job description
        job_text = f"{job.role_title} {job.description}".lower()
        scored_bullets = []

        for bullet in all_bullets:
            bullet_lower = bullet.lower()
            score = 0

            # Check for keyword matches
            keywords = self._extract_keywords(job_text)
            for keyword in keywords:
                if keyword in bullet_lower:
                    score += 2

            # Boost for strategic keywords
            strategic_words = ["infrastructure", "systems", "scale", "built", "led",
                             "revenue", "budget", "cross-functional", "strategic"]
            for word in strategic_words:
                if word in bullet_lower:
                    score += 1

            # Boost for metrics
            if any(char.isdigit() for char in bullet):
                score += 1

            scored_bullets.append((score, bullet))

        # Sort by score and take top 5-7
        scored_bullets.sort(reverse=True, key=lambda x: x[0])
        selected = [bullet for score, bullet in scored_bullets[:7]]

        return selected

    def _get_default_resume_content(self) -> str:
        """Get default resume content from config."""
        content = """
EXPERIENCE

ELASTIC - Video Lead, Creative & Strategy (June 2024 - Present)
• Directing internal team of 4 and dozen agencies/vendors to produce strategic content for global company and audience
• Directed and produced Elastic's new hero video featuring CEO, achieving 350k impressions, 5k+ views, 200 clicks in under a month (all organic)
• Video achieved 34% of channel's lifetime views in under 2% of channel lifespan
• Led cross-functional initiatives across Product, Engineering, Marketing, and Legal teams
• Established production infrastructure and workflow systems for scale

SNYK - Creative Video Director (November 2021 - November 2022)
• Directed team of 9 agencies/vendors to produce video collateral across Product Design, Product Marketing, Demand Generation, Customer Advocacy, Sales, Social, Web, Developer Relations, Talent Brand, and Events
• Produced and directed Snyk's platform story animation, generating 40k+ views across multiple channels
• Led discovery for Snyk's IPO Roadshow Trailer, establishing creative strategy and production approach
• Created experiential AR game for SnykCon 2022 generating 1,200 MQLs
• Built production operations from scratch including vendor management and budget oversight

INVISION - Video Strategy Director (June 2018 - November 2021)
• Grew InVision Films unit into strategic business asset responsible for over $100M in sales opportunities
• Directed documentary film "Squads" which generated over $4MM in attributable revenue
• Directed and produced 10 Masterclass-style courses for new learning platform, selling $1MM in seats and generating $1.8MM in pipeline as pilot (exceeding revenue targets by 6x)
• Built and managed production infrastructure supporting 100+ videos annually
• Owned budget ranging from $25K to 7 figures with deep Legal/Procurement partnership
• Led cross-functional collaboration across Product, Brand, Sales, Legal, and Customer Success

LINE OF FLIGHT FILMS - Owner (October 2012 - Present)
• Award-winning director, producer, and cinematographer
• Work featured on HBO, The New York Times Op-Docs, VOX.com, PBS
• Screened at Tribeca Film Festival, SXSW, Cannes, The New York Film Festival, Clermont Ferrand, and Torino Film Festival
• Platinum Award Best Documentary (Marcom Awards)
• Gold Winner Marketing Material (Marcom Awards)
• Platinum Award Integrated Campaign (Summit International)

KEY ACHIEVEMENTS
• Built production functions from scratch 3x (Elastic, Snyk, InVision)
• Revenue attribution: $4MM+ at InVision from single documentary project
• 6x revenue target overage on InVision Learn platform ($1.8MM pipeline vs $300K target)
• 34% of Elastic lifetime YouTube views achieved in <2% of channel lifespan
• Budget/operational authority: $25K-7 figures across organizations
• Team leadership: Managed internal teams up to 4 people and external vendor networks of 9+ agencies
• Cross-functional orchestration across Product, Engineering, Marketing, Sales, Legal, Procurement
• Production as infrastructure: Systems design, workflow optimization, scalable operations
"""
        return content

    def _get_all_resume_bullets(self) -> List[str]:
        """Extract all bullets from resume content."""
        content = self._get_default_resume_content()
        bullets = []

        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('•'):
                bullets.append(line[1:].strip())

        return bullets

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from job description."""
        # Remove common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                       'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'will',
                       'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'this', 'that',
                       'you', 'your', 'we', 'our', 'their'}

        words = text.lower().split()
        keywords = [w for w in words if w not in common_words and len(w) > 3]

        # Return unique keywords
        return list(set(keywords))

    def _parse_bullets_from_response(self, response: str) -> List[str]:
        """Parse bullet points from AI response."""
        bullets = []
        lines = response.strip().split('\n')

        for line in lines:
            line = line.strip()
            # Remove numbering, bullets, etc.
            if line:
                # Remove leading numbers (1., 2., etc.) or bullets (•, -, *)
                cleaned = line.lstrip('0123456789.•-* ').strip()
                if cleaned:
                    # Ensure bullet starts with action verb
                    if not cleaned.startswith('•'):
                        cleaned = '• ' + cleaned
                    bullets.append(cleaned)

        return bullets

    def format_tailored_resume(self, job: JobPosting, bullets: List[str]) -> str:
        """
        Format tailored resume bullets into markdown.

        Args:
            job: JobPosting object
            bullets: List of tailored bullets

        Returns:
            Formatted markdown resume
        """
        md = f"""# Daniel Cowen
**Creative direction at enterprise scale**

## Contact
- Email: dc@loffilms.com
- Phone: 860-951-5919
- Portfolio: [loffilms.com/videostrategy](https://loffilms.com/videostrategy)

## Tailored for: {job.role_title} at {job.company}

## Key Achievements & Relevant Experience

"""
        for bullet in bullets:
            if not bullet.startswith('•'):
                bullet = '• ' + bullet
            md += f"{bullet}\n"

        md += """
## Notable Skills
Creative team lead, creative development, brand, narrative and content strategy, project management, media and video production, cross-functional collaboration, soft skills, online learning, event content and conversation design, animation, AR, virtual production, agency/vendor management, forecasting/budgeting, interviewing.

## Awards
- Platinum Award Best Documentary (Marcom Awards)
- Gold Winner Marketing Material (Marcom Awards)
- Platinum Award Integrated Campaign (Summit International)
"""

        return md
