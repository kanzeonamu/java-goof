# Job Search Automation Tool

Automated job search and application assistant for creative production leadership roles in tech.

## Features

### 1. Job Scraping Module
- **Supported Sites:** LinkedIn, Wellfound, Built In, Otta, Remote.co
- **Target Roles:** Head of Creative Production, VP Creative Operations, Director of Video, Creative Strategy Director, Head of Brand Production
- **Smart Filtering:**
  - Remote-first priority (95% remote or NYC location)
  - Minimum salary: $210K (flags unknown, excludes confirmed lower)
  - Company stage: Prefers seed through Series B
  - Industry: Tech companies only
- **Data Export:** Saves results to JSON with company, role, salary, remote policy, stage, URL, description

### 2. Scoring Engine
Scores each job 1-10 based on:
- **Role Alignment (30%):** Infrastructure/systems building vs execution work
- **Company Stage (20%):** Earlier stage = higher score
- **Remote Policy (25%):** Remote required, dealbreaker if onsite
- **Salary Transparency (10%):** Disclosed and meets minimum
- **Cultural Fit (15%):** Red flags (micromanagement, "wear many hats") vs positive indicators (systems, scalable, budget ownership)

Outputs ranked list with detailed scoring reasoning.

### 3. Resume Tailoring (Coming Soon)
- Extracts 5-7 most relevant bullets matching job description
- Emphasizes: systems design, cross-functional delivery, measurable impact, team building, budget ownership
- Generates tailored 1-page resume in markdown per job

### 4. Cover Letter Generation (Coming Soon)
- Uses your key talking points:
  - Production as infrastructure, not execution
  - Built production functions 3x (Elastic, Snyk, InVision)
  - Revenue attribution: $4M+ at InVision
  - Scale impact: 34% of Elastic lifetime views
  - Budget authority: $25K-7 figures
  - Cross-functional orchestration
- Generates 250-300 word cover letters matched to company stage

### 5. Portfolio Recommendations (Coming Soon)
- Recommends portfolio pieces based on job description:
  - Elastic "Evolving Search" hero video
  - Snyk AR game (experiential)
  - InVision "Squads" documentary
  - InVision Learn platform work

### 6. Output Format
- Daily digest: Top 5-10 opportunities ranked by score
- Per opportunity: Score + reasoning, tailored resume, cover letter, portfolio recs, application link
- Organized folder structure: `/jobs/YYYY-MM-DD/[company-name]/`

## Installation

### Prerequisites
- Python 3.8+
- Chrome browser (for Selenium)

### Setup

1. **Clone and navigate to the tool:**
   ```bash
   cd job-search-tool
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment (optional):**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

## Usage

### Test the Scoring Engine

Run the test script with sample job data:

```bash
python test_scoring.py
```

This will score 6 sample job postings and show you how the scoring engine works without scraping live sites.

### Run Live Job Search

**Single site test:**
```bash
python main.py --sites wellfound --test
```

**Full search across all sites:**
```bash
python main.py
```

**Search specific sites:**
```bash
python main.py --sites wellfound builtin otta
```

**Test mode without saving:**
```bash
python main.py --test --no-save
```

### Daily Automation

Set up a cron job to run daily:

```bash
# Run every weekday at 9 AM
0 9 * * 1-5 cd /path/to/job-search-tool && python main.py
```

## Output Structure

```
jobs/
├── 2026-01-15/
│   ├── raw_jobs.json              # All scraped jobs
│   ├── scored_jobs.json           # Filtered and scored jobs
│   ├── daily_digest.md            # Top opportunities summary
│   ├── acme-ai/
│   │   ├── job_details.json
│   │   ├── tailored_resume.md
│   │   ├── cover_letter.md
│   │   ├── portfolio_recommendations.md
│   │   └── application_link.txt
│   └── scale-studios/
│       └── ...
└── 2026-01-16/
    └── ...
```

## Configuration

Edit `config.py` to customize:
- Target job titles and search keywords
- Company stage preferences
- Scoring weights
- Cultural red flags and positive indicators
- Portfolio pieces
- Resume talking points

## Important Notes

### LinkedIn Scraping
⚠️ **WARNING:** LinkedIn explicitly prohibits automated scraping in their Terms of Service. This tool includes a LinkedIn scraper for educational purposes, but using it may result in account suspension. Consider:
- Using LinkedIn's official Job Search API (requires partnership)
- Manual exports from LinkedIn Recruiter
- Third-party aggregators with LinkedIn partnerships

### Rate Limiting
The tool includes built-in rate limiting (2 seconds between requests by default). Adjust in `config.py` if needed.

### Headless Mode
Scrapers run in headless mode by default. Disable for debugging:
```python
# In config.py
SCRAPER_CONFIG = {
    "headless": False,  # Set to False to see browser
    ...
}
```

## Development Roadmap

- [x] Job scraping module with site-specific scrapers
- [x] Scoring engine with weighted ranking
- [x] Data persistence and JSON storage
- [x] Daily digest generation
- [ ] Resume tailoring with AI
- [ ] Cover letter generation with AI
- [ ] Portfolio recommendation engine
- [ ] Email notifications for high-score jobs
- [ ] Application tracking
- [ ] Interview preparation module

## Sample Output

```
TOP 5 OPPORTUNITIES

1. VP of Creative Operations at Growth Stage Tech
   Score: 9.2/10
   Remote: remote | Location: NYC or Remote
   Salary: $250,000+
   URL: https://example.com/job5

   Score Breakdown:
   Role Alignment (9.0/10): Strong infrastructure/systems focus, leadership role
   Company Stage (8.0/10): Series B (preferred)
   Remote Policy (10.0/10): Fully remote (required)
   Salary Transparency (10.0/10): Salary disclosed and meets minimum: $250,000+
   Cultural Fit (9.0/10): No obvious red flags, strong positive indicators (6 found)

2. Head of Creative Production at Acme AI
   Score: 8.9/10
   ...
```

## Troubleshooting

### ChromeDriver Issues
If you encounter ChromeDriver errors:
```bash
pip install --upgrade webdriver-manager
```

### Import Errors
Make sure you're running from the tool directory:
```bash
cd job-search-tool
python main.py
```

### No Jobs Found
- Check your internet connection
- Verify the sites are accessible
- Try running with `--test` flag first
- Check logs in `logs/` directory

## Contributing

This tool is designed for personal use. Modify and extend as needed for your specific requirements.

## License

MIT License - Use at your own risk. Always comply with website Terms of Service.
