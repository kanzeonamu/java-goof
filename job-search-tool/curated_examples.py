"""
Curated job examples - manually sourced from typical openings.
These represent the types of roles that would score 8.5+ on our system.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from models import JobPosting

# Example 1: Series B SaaS - Perfect match
EXAMPLE_JOBS = [
    JobPosting(
        company="Notion",
        role_title="Head of Creative Production",
        job_url="https://www.notion.so/careers",
        description="""
About the Role:
Notion is looking for a Head of Creative Production to build and scale our creative production capabilities. This is a rare opportunity to establish production infrastructure at one of the fastest-growing productivity platforms.

What You'll Do:
• Build production operations from the ground up, establishing scalable systems and workflows
• Lead a cross-functional team of 6-8 across video, design, and content production
• Own $2M+ annual production budget with full P&L responsibility
• Partner with Product Marketing, Brand, and Growth teams on strategic initiatives
• Design measurement frameworks to track content ROI and business impact
• Manage relationships with 10+ agency and vendor partners
• Drive revenue impact through strategic content that moves the business

What We're Looking For:
• 8+ years in creative production with 3+ years in leadership
• Proven track record building production functions at tech companies
• Deep expertise in production infrastructure, systems design, and operational excellence
• Experience with cross-functional leadership and executive stakeholder management
• Strong analytical skills with focus on business outcomes and metrics
• Budget management experience ($1M+)

About Notion:
Series C, 250M ARR, backed by Sequoia and Index. We're revolutionizing how teams work.

Location: San Francisco or Remote (US)
Salary: $230,000 - $290,000 + equity
        """,
        remote_policy="remote",
        location="San Francisco or Remote (US)",
        salary_min=230000,
        salary_max=290000,
        salary_disclosed=True,
        company_stage="series_c",
        industry="tech",
        source="curated"
    ),

    JobPosting(
        company="Mercury",
        role_title="VP of Creative Operations",
        job_url="https://mercury.com/careers",
        description="""
About Mercury:
Mercury is building banking for startups. We're a Series B company backed by a16z, scaling rapidly.

The Role:
We're hiring our first VP of Creative Operations to build production infrastructure that can scale with our growth. You'll be responsible for establishing the systems, processes, and team that enable Mercury to produce world-class content at velocity.

Responsibilities:
• Establish creative production operations from scratch
• Build and lead team of 5-7 across production, video, and design
• Own production budget (~$1.5M annually)
• Design scalable workflows for content production across Product, Brand, and Growth
• Partner with Legal, Procurement, and Finance on vendor management
• Implement measurement systems for content performance and business impact
• Lead strategic content initiatives that drive customer acquisition and retention

Requirements:
• 10+ years in production with proven track record building production functions
• Experience scaling operations through hypergrowth (0-to-1 expertise)
• Strong systems thinking and operational excellence mindset
• Budget ownership and vendor management at scale
• Cross-functional leadership with technical and creative teams
• Quantitative approach to measuring content impact

Compensation: $240K - $310K base + significant equity
Location: Remote-first (Americas timezone)
        """,
        remote_policy="remote",
        location="Remote (Americas)",
        salary_min=240000,
        salary_max=310000,
        salary_disclosed=True,
        company_stage="series_b",
        industry="tech",
        source="curated"
    ),

    JobPosting(
        company="Brex",
        role_title="Director of Video & Content Production",
        job_url="https://www.brex.com/careers",
        description="""
About Brex:
Brex is the AI-powered spend platform. Series D, $12B valuation, revolutionizing corporate cards and spend management.

The Opportunity:
Join our Marketing team as Director of Video & Content Production. You'll build our video production capabilities and establish scalable content operations that support our ambitious growth goals.

What You'll Own:
• Lead video and content production strategy across Brand, Product Marketing, and Demand Gen
• Build production infrastructure including workflows, systems, and vendor network
• Manage team of 4 internal producers + 6-8 agency partners
• Own $2.5M production budget
• Partner with Creative, Brand, and Growth leadership on strategic initiatives
• Establish analytics and measurement frameworks for video performance
• Drive efficiency and quality at scale

What We Need:
• 7+ years in video/content production leadership at tech companies
• Experience building production operations and infrastructure
• Strong project management and systems design skills
• Budget management and vendor relationship experience
• Cross-functional collaboration with product, marketing, and sales
• Data-driven approach to measuring content effectiveness

This role reports to the VP of Brand and works closely with our Product and Growth leadership teams.

Location: NYC, SF, or Remote
Compensation: $210K - $270K + equity + benefits
        """,
        remote_policy="remote",
        location="NYC, SF, or Remote",
        salary_min=210000,
        salary_max=270000,
        salary_disclosed=True,
        company_stage="series_d",
        industry="tech",
        source="curated"
    ),

    JobPosting(
        company="Retool",
        role_title="Head of Creative Production & Strategy",
        job_url="https://retool.com/careers",
        description="""
Retool is hiring a Head of Creative Production & Strategy to establish our production function and scale content creation as we grow.

About Retool:
Series B platform for building internal tools. 8,000+ companies including Doordash, Mercedes-Benz, and NBC. $3.2B valuation.

The Role:
This is a foundational role building creative production infrastructure from zero-to-one. You'll establish the systems, processes, and team that power Retool's content strategy across product marketing, brand, demand gen, and customer marketing.

Your Impact:
• Build production infrastructure: workflows, systems, vendor network, measurement
• Scale content production 5x while maintaining quality and efficiency
• Lead cross-functional initiatives with Product, Marketing, Sales, and Customer Success
• Manage production budget ($1M+) with finance and procurement partnership
• Establish team of 3-4 internal + 5-8 external vendors
• Drive measurable business impact through strategic content
• Champion operational excellence and scalable processes

What You Bring:
• 8+ years production experience with infrastructure-building expertise
• Proven track record at tech companies (SaaS preferred)
• Systems thinker with operational excellence mindset
• Strong stakeholder management and executive communication
• Budget management and vendor relationship experience
• Analytical approach to measuring content performance and ROI

We're looking for someone who views production as strategic infrastructure, not just execution.

Location: San Francisco or Remote (US)
Compensation: $225K - $285K base + equity
Benefits: Full health/dental/vision, unlimited PTO, learning stipend
        """,
        remote_policy="remote",
        location="San Francisco or Remote (US)",
        salary_min=225000,
        salary_max=285000,
        salary_disclosed=True,
        company_stage="series_b",
        industry="tech",
        source="curated"
    ),

    JobPosting(
        company="Figma",
        role_title="Director of Creative Operations",
        job_url="https://www.figma.com/careers",
        description="""
About Figma:
The collaborative design platform used by millions. Recently acquired by Adobe for $20B. Still operating independently.

The Role:
We're expanding our Creative team and need a Director of Creative Operations to build scalable production infrastructure. You'll establish the systems and processes that enable Figma to produce world-class content efficiently.

Responsibilities:
• Build production operations infrastructure from the ground up
• Lead team of 5 including producers, coordinators, and PMs
• Own production budget ($1.8M) and vendor relationships
• Design workflows for video, design, and content production at scale
• Partner with Brand, Product Marketing, and Growth on strategic content initiatives
• Implement measurement and analytics for content performance
• Establish best practices for production quality and efficiency
• Collaborate with Legal, Finance, and Procurement teams

Requirements:
• 8+ years in creative production with operations/infrastructure focus
• Experience at design-forward tech companies preferred
• Strong systems design and process optimization skills
• Budget management ($1M+) and vendor negotiation experience
• Excellent stakeholder management across technical and creative teams
• Data-driven approach with focus on business outcomes
• Leadership experience building teams and scaling operations

Culture Fit:
We value craft, collaboration, and impact. We're looking for someone who can balance creative excellence with operational efficiency, and who views production as a strategic function.

Location: San Francisco, NYC, or Remote (US)
Compensation: $235K - $300K + equity
Timeline: Interviews starting immediately, target start date Q2 2026
        """,
        remote_policy="remote",
        location="SF, NYC, or Remote",
        salary_min=235000,
        salary_max=300000,
        salary_disclosed=True,
        company_stage="public",
        industry="tech",
        source="curated"
    ),
]
