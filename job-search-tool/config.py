"""
Configuration for job search automation tool.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent
JOBS_DIR = BASE_DIR / "jobs"
LOGS_DIR = BASE_DIR / "logs"
CONFIG_DIR = BASE_DIR / "config"

# Ensure directories exist
JOBS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
CONFIG_DIR.mkdir(exist_ok=True)

# Credentials (load from environment variables)
LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Target job titles
TARGET_TITLES = [
    "Head of Creative Production",
    "VP Creative Operations",
    "Director of Video",
    "Creative Strategy Director",
    "Head of Brand Production",
    "Director of Content Production",
    "VP of Creative",
    "Head of Video Production",
    "Creative Operations Director"
]

# Search keywords for broader matching
SEARCH_KEYWORDS = [
    "creative production",
    "video production",
    "content production",
    "brand production",
    "creative operations",
    "video strategy",
    "creative director production"
]

# Company stage preferences (higher score = more preferred)
STAGE_SCORES = {
    "seed": 10,
    "series_a": 9,
    "series_b": 8,
    "series_c": 6,
    "series_d": 5,
    "series_d+": 4,
    "public": 3,
    "unknown": 5
}

# Remote policy scores
REMOTE_SCORES = {
    "remote": 10,
    "hybrid_nyc": 7,
    "nyc": 5,
    "hybrid": 3,
    "onsite": 0,
    "unknown": 6
}

# Cultural red flags (presence decreases score)
RED_FLAGS = [
    "wear many hats",
    "fast-paced environment",
    "startup mentality",
    "entrepreneurial spirit",
    "self-starter",
    "hit the ground running",
    "thrive in chaos",
    "no task too small",
    "do whatever it takes"
]

# Positive indicators (presence increases score)
POSITIVE_INDICATORS = [
    "infrastructure",
    "systems",
    "platform",
    "process",
    "workflow",
    "pipeline",
    "automation",
    "scalable",
    "scale",
    "team building",
    "cross-functional",
    "strategic",
    "operational",
    "budget",
    "p&l",
    "revenue",
    "impact",
    "measurement",
    "analytics",
    "vendor management",
    "agency management"
]

# Role alignment keywords (strategic vs execution)
STRATEGIC_KEYWORDS = [
    "strategy",
    "infrastructure",
    "systems design",
    "operational excellence",
    "process design",
    "workflow optimization",
    "team building",
    "organizational design",
    "cross-functional leadership",
    "stakeholder management",
    "budget ownership",
    "vendor management",
    "scalability",
    "production operations"
]

EXECUTION_KEYWORDS = [
    "hands-on",
    "execute",
    "shoot",
    "edit",
    "adobe premiere",
    "after effects",
    "final cut",
    "camera operator",
    "produce content",
    "create videos",
    "individual contributor"
]

# Scraper settings
SCRAPER_CONFIG = {
    "headless": True,
    "timeout": 30,
    "max_results_per_site": 50,
    "rate_limit_delay": 2,
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

# Scoring weights
SCORING_WEIGHTS = {
    "role_alignment": 0.30,
    "company_stage": 0.20,
    "remote_policy": 0.25,
    "salary_transparency": 0.10,
    "cultural_fit": 0.15
}

# Minimum score threshold for inclusion in daily digest
MIN_SCORE_THRESHOLD = 6.0

# Resume talking points
RESUME_TALKING_POINTS = {
    "production_infrastructure": [
        "Built production functions from scratch 3x (Elastic, Snyk, InVision)",
        "Production as infrastructure, not execution",
        "Systems design and operational excellence"
    ],
    "revenue_impact": [
        "Revenue attribution: $4M+ at InVision",
        "6x revenue target overage",
        "Measurable business impact and ROI tracking"
    ],
    "scale": [
        "34% of Elastic lifetime views in <2% of channel lifespan",
        "350k+ impressions, 5k+ views, 200 clicks in under a month (organic)",
        "Scaled production operations across global teams"
    ],
    "budget_operations": [
        "Budget/operational authority: $25K-7 figures",
        "Deep Legal/Procurement partnership",
        "Vendor and agency management at scale"
    ],
    "cross_functional": [
        "Cross-functional orchestration across Product, Brand, Sales, Legal",
        "Led teams of 9+ agencies/vendors simultaneously",
        "Strategic alignment with executive leadership"
    ]
}

# Portfolio pieces
PORTFOLIO_PIECES = {
    "elastic_evolving_search": {
        "title": "Elastic 'Evolving Search' Hero Video",
        "description": "High-level narrative featuring CEO, demonstrating strategic storytelling",
        "url": "https://loffilms.com/videostrategy",
        "best_for": ["strategic", "executive", "narrative", "brand", "product marketing"]
    },
    "snyk_ar_game": {
        "title": "Snyk AR Game (Experiential)",
        "description": "Interactive experience generating 1,200 MQLs",
        "url": "https://loffilms.com/videostrategy",
        "best_for": ["experiential", "demand generation", "events", "innovative", "measurable impact"]
    },
    "invision_squads": {
        "title": "InVision 'Squads' Documentary",
        "description": "$4M+ revenue attribution, customer-centric storytelling",
        "url": "https://loffilms.com/videostrategy",
        "best_for": ["documentary", "customer stories", "revenue impact", "saas"]
    },
    "invision_learn": {
        "title": "InVision Learn Platform",
        "description": "Educational content platform, 6x revenue target overage",
        "url": "https://loffilms.com/videostrategy",
        "best_for": ["educational", "platform", "scalable content", "revenue impact"]
    }
}
