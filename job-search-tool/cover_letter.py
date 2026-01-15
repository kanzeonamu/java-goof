"""
Cover letter generation module.
Generates personalized cover letters based on job postings.
"""
import logging
from typing import Optional
import anthropic

from models import JobPosting
import config


logger = logging.getLogger(__name__)


class CoverLetterGenerator:
    """Generates personalized cover letters for job applications."""

    def __init__(self, api_key: str = None):
        """
        Initialize cover letter generator.

        Args:
            api_key: Anthropic API key (defaults to config)
        """
        self.api_key = api_key or config.ANTHROPIC_API_KEY
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("No Anthropic API key provided. Cover letter generation will use templates.")

    def generate_cover_letter(self, job: JobPosting) -> str:
        """
        Generate personalized cover letter for a job posting.

        Args:
            job: JobPosting object

        Returns:
            Cover letter text (250-300 words)
        """
        if self.client:
            try:
                return self._generate_with_ai(job)
            except Exception as e:
                logger.error(f"Error using AI for cover letter generation: {e}")
                logger.info("Falling back to template-based generation")
                return self._generate_template(job)
        else:
            return self._generate_template(job)

    def _generate_with_ai(self, job: JobPosting) -> str:
        """Use AI to generate cover letter."""
        # Determine tone based on company stage
        tone = self._get_tone_for_stage(job.company_stage)

        prompt = f"""You are writing a cover letter for Daniel Cowen applying for a job.

Job Details:
Company: {job.company}
Role: {job.role_title}
Company Stage: {job.company_stage}
Description: {job.description}

Daniel's Background & Key Talking Points:
1. Production as Infrastructure: Daniel views creative production not as execution work but as infrastructure and systems design. He's built production functions from scratch 3 times (Elastic, Snyk, InVision).

2. Revenue Attribution & Business Impact:
   - Generated $4M+ in attributable revenue at InVision from documentary "Squads"
   - Achieved 6x revenue target overage on InVision Learn platform ($1.8MM pipeline vs $300K target)
   - 34% of Elastic's lifetime YouTube views in <2% of channel lifespan
   - Drove 1,200 MQLs from experiential AR game at Snyk

3. Scale & Operational Authority:
   - Budget authority ranging from $25K to 7 figures
   - Deep partnership with Legal, Procurement, Finance
   - Led teams of 4+ internal + 9+ external agencies/vendors simultaneously
   - Built scalable workflows and production operations

4. Cross-Functional Leadership:
   - Orchestrated initiatives across Product, Engineering, Marketing, Sales, Legal
   - Strategic partner to executive leadership
   - Systems thinker focused on operational excellence

5. Award-Winning Creative:
   - Work featured on HBO, The New York Times, VOX, PBS
   - Screened at Tribeca, SXSW, Cannes, The New York Film Festival
   - Multiple Platinum and Gold awards for creative excellence

Tone Guidance:
{tone}

Requirements:
1. Write a compelling 250-300 word cover letter
2. Match the tone to the company stage (see guidance above)
3. Focus on 2-3 most relevant talking points that align with the job description
4. Include specific metrics and outcomes
5. Show understanding of the role's strategic nature
6. Demonstrate value proposition clearly
7. End with clear call to action
8. Do NOT use overly formal language or clichés
9. Be direct, confident, and substantive
10. Make it personal to this specific role and company

Write the cover letter now. Do not include a subject line, just the body of the letter starting with the greeting."""

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        cover_letter = message.content[0].text.strip()
        return cover_letter

    def _generate_template(self, job: JobPosting) -> str:
        """Generate cover letter from template."""
        # Determine key points based on job description
        description_lower = job.description.lower()

        # Select relevant talking points
        points = []

        if any(word in description_lower for word in ["infrastructure", "systems", "scale", "operations"]):
            points.append(
                "I've built production functions from scratch three times (Elastic, Snyk, InVision), "
                "treating production as infrastructure rather than execution. At Elastic, my work generated "
                "34% of the channel's lifetime views in under 2% of its lifespan."
            )

        if any(word in description_lower for word in ["revenue", "business", "roi", "impact", "metrics"]):
            points.append(
                "My work drives measurable business outcomes. At InVision, a single documentary project "
                "generated $4M+ in attributable revenue, and the Learn platform pilot exceeded revenue "
                "targets by 6x ($1.8MM vs $300K target)."
            )

        if any(word in description_lower for word in ["budget", "vendor", "agency", "procurement"]):
            points.append(
                "I've owned budgets ranging from $25K to 7 figures with deep Legal/Procurement partnerships, "
                "managing teams of 4+ internal and 9+ external agencies simultaneously."
            )

        if any(word in description_lower for word in ["cross-functional", "stakeholder", "leadership", "strategic"]):
            points.append(
                "I orchestrate cross-functional initiatives across Product, Engineering, Marketing, Sales, "
                "and Legal, serving as a strategic partner to executive leadership."
            )

        # If no specific matches, use general points
        if not points:
            points = [
                "I specialize in building creative production infrastructure at scale. Over my career, "
                "I've built production functions from scratch at three high-growth tech companies, "
                "driving measurable business impact through systems thinking and operational excellence.",

                "My work combines strategic leadership with proven results: $4M+ in revenue attribution, "
                "6x revenue target overage, and award-winning creative that's been featured on HBO, "
                "The New York Times, and screened at major festivals including Tribeca and SXSW."
            ]

        # Build cover letter
        tone_prefix = "I'm reaching out about" if self._is_early_stage(job.company_stage) else "I'm writing to express my interest in"

        cover_letter = f"""Dear Hiring Team at {job.company},

{tone_prefix} the {job.role_title} position. {points[0]}

{points[1] if len(points) > 1 else ''}

I'm drawn to {job.company} because of your focus on {"building innovative solutions" if self._is_early_stage(job.company_stage) else "operational excellence"} at this stage. I believe production operations should be strategic infrastructure that enables teams to move faster, measure impact, and scale effectively.

I'd welcome the opportunity to discuss how my experience building production systems could contribute to your team's goals. You can view my work at loffilms.com/videostrategy.

Best regards,
Daniel Cowen
dc@loffilms.com
860-951-5919
"""

        return cover_letter

    def _get_tone_for_stage(self, company_stage: str) -> str:
        """Get tone guidance based on company stage."""
        if not company_stage:
            company_stage = "unknown"

        stage_lower = company_stage.lower()

        if "seed" in stage_lower:
            return """Use a direct, energetic tone. Startups value action and impact over formality.
Be conversational but professional. Show you understand the challenges of building from zero to one."""

        elif "series a" in stage_lower or "series_a" in stage_lower:
            return """Use a confident, strategic tone. Series A companies are scaling and need proven operators.
Balance directness with professionalism. Emphasize systems building and scalability."""

        elif "series b" in stage_lower or "series_b" in stage_lower:
            return """Use a strategic, results-oriented tone. Series B companies are optimizing for growth.
Be professional but not overly formal. Focus on metrics, efficiency, and cross-functional impact."""

        elif "series c" in stage_lower or "series_c" in stage_lower or "series d" in stage_lower:
            return """Use a professional, executive tone. Later stage companies value proven track records.
Be more formal and structured. Emphasize leadership, scale, and organizational impact."""

        elif "public" in stage_lower:
            return """Use a formal, executive tone. Public companies have established processes.
Be professional and structured. Emphasize governance, stakeholder management, and enterprise scale."""

        else:
            return """Use a balanced, professional tone. Focus on concrete achievements and measurable impact.
Be confident but not presumptuous. Show strategic thinking and operational excellence."""

    def _is_early_stage(self, company_stage: str) -> bool:
        """Check if company is early stage."""
        if not company_stage:
            return False

        stage_lower = company_stage.lower()
        return "seed" in stage_lower or "series a" in stage_lower or "series_a" in stage_lower
