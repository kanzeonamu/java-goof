# Standing One

Free public resource for people searching for help with sacroiliac joint pain (SI pain).

**Domain:** standing.one
**Stack:** Astro, TypeScript, Pagefind search, Cloudflare Pages
**Author attribution:** Daniel Cowen (Tiger Walk page)

## Features

- **Educational content:** Plain-language guides on SI pain, systems thinking, and practical interventions
- **Static site search:** Full-text search powered by Pagefind
- **Feedback form:** Private email submissions via Formspree
- **SEO optimized:** Meta tags, OpenGraph, sitemap, JSON-LD schema, semantic HTML
- **Accessible & fast:** Minimal CSS, system fonts, dark mode support, Lighthouse-optimized
- **Privacy-friendly:** Cloudflare Web Analytics (no cookies)

## Local Development

### Prerequisites

- Node.js 18+ and npm
- Git

### Setup

1. **Clone the repository**

```bash
git clone <repository-url>
cd standing-one
```

2. **Install dependencies**

```bash
npm install
```

3. **Set up environment variables** (optional for local dev)

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Add your Formspree endpoint (see [Feedback Form Setup](#feedback-form-setup) below):

```
PUBLIC_FORMSPREE_ENDPOINT=https://formspree.io/f/YOUR_FORM_ID
```

If not set, the feedback form will show a "not configured" message.

4. **Start development server**

```bash
npm run dev
```

Open http://localhost:4321 in your browser.

### Development commands

- `npm run dev` — Start dev server with hot reload
- `npm run build` — Build for production (includes Astro build + Pagefind indexing)
- `npm run preview` — Preview production build locally
- `npm run astro` — Run Astro CLI commands

## Content Editing

### Adding or editing pages

All page content is in:
- `src/pages/` — Astro pages (`.astro` files)
- `src/content/conditions/` — Condition guides (Markdown)
- `src/content/topics/` — Topic explainers (Markdown)

#### Editing existing markdown content

1. Navigate to the relevant `.md` file in `src/content/`
2. Edit the frontmatter (title, description, lastUpdated, tags)
3. Edit the markdown content
4. Update `lastUpdated` to current date
5. Save and rebuild

Example frontmatter:

```yaml
---
title: 'Page Title'
description: 'Short description for SEO'
lastUpdated: '2026-01-15'
tags: ['tag1', 'tag2']
---
```

#### Adding a new condition page

1. Create a new `.md` file in `src/content/conditions/`
2. Add frontmatter with title, description, lastUpdated, tags
3. Write content in Markdown
4. The page will be available at `/conditions/[filename]`
5. Add link to `/src/pages/conditions/index.astro` if desired

#### Adding a new topic page

Same as conditions, but in `src/content/topics/` and accessible at `/topics/[filename]`.

### Updating navigation

Edit `src/layouts/BaseLayout.astro` to change header or footer navigation links.

## Search Indexing

Search is powered by **Pagefind**, which indexes the built site.

### How it works

1. `npm run build` runs:
   - `astro check` (TypeScript check)
   - `astro build` (builds static site to `dist/`)
   - `npm run search:index` (runs `pagefind --site dist` to index content)

2. Pagefind creates `/pagefind/` directory in `dist/` with search index and UI

3. The `/search` page loads Pagefind UI and searches the index

### Rebuilding search index

Search is automatically indexed on every production build. No manual steps needed.

If you want to re-index after editing content locally:

```bash
npm run build
```

## Feedback Form Setup

The feedback form uses **Formspree** to email submissions privately without exposing the destination email publicly.

### Steps to set up Formspree

1. **Create a free Formspree account** at https://formspree.io

2. **Create a new form** in the Formspree dashboard

3. **Configure form settings:**
   - Set email destination to Daniel Cowen's email (configured in Formspree dashboard, not in code)
   - Enable spam protection (Formspree provides this)
   - Optionally enable reCAPTCHA if spam becomes an issue

4. **Copy the form endpoint URL**

   It will look like: `https://formspree.io/f/YOUR_FORM_ID`

5. **Add endpoint to environment variables**

   **For local development:**
   - Add to `.env` (not committed to repo):
     ```
     PUBLIC_FORMSPREE_ENDPOINT=https://formspree.io/f/YOUR_FORM_ID
     ```

   **For Cloudflare Pages (production):**
   - Go to Cloudflare Dashboard → Workers & Pages → Your Site → Settings → Environment Variables
   - Add variable:
     - Name: `PUBLIC_FORMSPREE_ENDPOINT`
     - Value: `https://formspree.io/f/YOUR_FORM_ID`
   - Save and redeploy

6. **Test the form**

   - Submit a test message via `/feedback`
   - Verify email is received at the configured destination
   - Verify redirect to `/thanks` works

### Form field mapping

The form fields are mapped as follows:
- `name` → Submitter name (optional)
- `_replyto` → Submitter email for replies (optional)
- `dealing-with` → Brief description of issue
- `what-helped` → What helped
- `what-worse` → What made it worse
- `anything-else` → Additional comments
- `share-consent` → Consent to share anonymously (checkbox)
- `_gotcha` → Honeypot field for spam prevention (hidden)

### Security notes

- The destination email is **never exposed** in the code or client-side
- Formspree provides spam protection and rate limiting
- Honeypot field (`_gotcha`) provides basic bot protection
- No email addresses are published anywhere on the site

## Deployment to Cloudflare Pages

### Prerequisites

- Cloudflare account (free tier works)
- Git repository (GitHub, GitLab, or Bitbucket)

### Initial deployment steps

1. **Push code to Git repository**

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Create Cloudflare Pages project**

   - Log in to Cloudflare Dashboard
   - Go to **Workers & Pages**
   - Click **Create** → **Pages** → **Connect to Git**
   - Select your Git provider and repository
   - Configure build settings:
     - **Build command:** `npm run build`
     - **Build output directory:** `dist`
   - Click **Save and Deploy**

3. **Set environment variables**

   - Go to your Pages project → **Settings** → **Environment Variables**
   - Add variable:
     - Name: `PUBLIC_FORMSPREE_ENDPOINT`
     - Value: `https://formspree.io/f/YOUR_FORM_ID` (from Formspree setup)
   - Select **Production** and **Preview** (or just Production if preferred)
   - Click **Save**
   - **Redeploy** to apply the new variable

4. **Wait for deployment**

   First deployment takes 2–5 minutes. Cloudflare will:
   - Clone the repo
   - Install dependencies
   - Run `npm run build`
   - Deploy to CDN

5. **View your site**

   Cloudflare provides a `*.pages.dev` URL (e.g., `standing-one.pages.dev`). Visit it to confirm the site works.

### Connecting custom domain: standing.one

#### Option A: Move DNS to Cloudflare (Recommended)

This is the simplest and most reliable approach.

1. **Add domain to Cloudflare**

   - In Cloudflare Dashboard, go to **Websites** → **Add a Site**
   - Enter `standing.one`
   - Choose a plan (Free works)
   - Cloudflare will scan existing DNS records

2. **Update nameservers at registrar**

   - Cloudflare will provide two nameservers (e.g., `ns1.cloudflare.com`, `ns2.cloudflare.com`)
   - Go to your domain registrar (where you bought `standing.one`)
   - Update nameservers to Cloudflare's nameservers
   - Save changes (propagation takes 2–24 hours)

3. **Add custom domain in Pages**

   - Go to your Pages project → **Custom Domains**
   - Click **Set up a custom domain**
   - Enter `standing.one`
   - Cloudflare will automatically create DNS records
   - SSL certificate is provisioned automatically (takes a few minutes)

4. **Add www subdomain** (optional)

   - Click **Set up a custom domain** again
   - Enter `www.standing.one`
   - Cloudflare can redirect `www` → `standing.one` automatically

5. **Verify**

   - Visit https://standing.one
   - Confirm site loads with SSL (green lock icon)

#### Option B: Keep DNS elsewhere (Advanced)

If you prefer to keep DNS at your current provider:

1. **Get CNAME target from Cloudflare**

   - Go to Pages project → **Custom Domains** → **Set up a custom domain**
   - Enter `standing.one`
   - Cloudflare will show a CNAME record to create

2. **Add CNAME at your DNS provider**

   **Note:** Apex domains (e.g., `standing.one` without `www`) require `CNAME` flattening or `ALIAS` records. Not all DNS providers support this. Check your provider's documentation.

   - Add a CNAME record:
     - Name: `@` or `standing.one` (for apex domain)
     - Target: `<your-project>.pages.dev` (provided by Cloudflare)
     - TTL: Automatic or 3600

   - For `www.standing.one`:
     - Name: `www`
     - Target: `<your-project>.pages.dev`
     - TTL: Automatic or 3600

3. **Verify DNS propagation**

   Use a tool like `dig` or https://dnschecker.org to confirm CNAME is propagating.

4. **SSL certificate**

   Cloudflare will provision SSL automatically after DNS verification (takes 5–30 minutes).

5. **Verify**

   Visit https://standing.one and confirm site loads with SSL.

### Cloudflare Web Analytics Setup

1. **Enable Cloudflare Web Analytics**

   - In Cloudflare Dashboard, go to **Web Analytics**
   - Click **Add a Site**
   - Enter `standing.one`
   - Copy the **Beacon Token**

2. **Update the site with your token**

   - Edit `src/layouts/BaseLayout.astro`
   - Replace `YOUR_TOKEN_HERE` in the Cloudflare Web Analytics script with your actual token:

     ```html
     <script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "YOUR_ACTUAL_TOKEN"}'></script>
     ```

3. **Commit and push**

   ```bash
   git add src/layouts/BaseLayout.astro
   git commit -m "Add Cloudflare Web Analytics token"
   git push
   ```

4. **Verify**

   - Wait for deployment
   - Visit the site
   - Check Cloudflare Dashboard → Web Analytics to confirm data is being collected

### Continuous deployment

Cloudflare Pages automatically redeploys when you push to the main branch:

1. Make changes locally
2. Commit and push:

   ```bash
   git add .
   git commit -m "Update content"
   git push
   ```

3. Cloudflare Pages will automatically build and deploy (takes 2–5 minutes)

## Project Structure

```
/
├── public/
│   ├── favicon.svg           # Site favicon
│   ├── robots.txt            # Search engine directives
│   └── styles/
│       └── global.css        # Global CSS styles
├── src/
│   ├── content/
│   │   ├── config.ts         # Content collections schema
│   │   ├── conditions/       # Condition guide markdown
│   │   │   └── si-pain.md
│   │   └── topics/           # Topic explainer markdown
│   │       ├── load-tolerance.md
│   │       ├── motor-control.md
│   │       ├── gait-single-leg.md
│   │       └── sleep-stress-pain.md
│   ├── layouts/
│   │   └── BaseLayout.astro  # Main layout with nav/footer
│   ├── pages/
│   │   ├── index.astro       # Homepage
│   │   ├── start-here.astro  # Start Here guide
│   │   ├── about.astro       # About page
│   │   ├── safety.astro      # Safety & red flags
│   │   ├── principles.astro  # Systems thinking principles
│   │   ├── tiger-walk.astro  # Personal journey (Daniel Cowen)
│   │   ├── search.astro      # Pagefind search page
│   │   ├── feedback.astro    # Feedback form
│   │   ├── thanks.astro      # Form submission confirmation
│   │   ├── conditions/
│   │   │   ├── index.astro   # Conditions index
│   │   │   └── [...slug].astro  # Dynamic condition pages
│   │   └── topics/
│   │       ├── index.astro   # Topics index
│   │       └── [...slug].astro  # Dynamic topic pages
│   └── env.d.ts              # TypeScript environment types
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore rules
├── astro.config.mjs          # Astro configuration
├── package.json              # Dependencies and scripts
├── README.md                 # This file
└── tsconfig.json             # TypeScript configuration
```

## Content Guidelines

### Tone and style

- Plain-spoken but technical
- Skimmable: short paragraphs, bullets, clear headings
- Avoid clinic/brand voice and universal claims
- No "always" language except safety warnings
- Focus on "what helped me" not "this will work for everyone"

### Disclaimers

Every condition page includes:
- Disclaimer box at top: "Educational only, not medical advice"
- Link to `/safety` page
- Red flags section with link

### Safety requirements

- All condition pages link to `/safety`
- Red flags are prominent and explicit
- No diagnostic claims
- Encourage professional evaluation when uncertain

### Author attribution

- Tiger Walk page: attributed to Daniel Cowen
- Other pages: no personal attribution
- **Do not publish email address anywhere**

## Maintenance

### Updating content

1. Edit markdown files in `src/content/` or `.astro` files in `src/pages/`
2. Update `lastUpdated` date
3. Test locally: `npm run build && npm run preview`
4. Commit and push to deploy

### Adding new pages

1. Create new file in appropriate directory
2. Add frontmatter (title, description, lastUpdated, tags if using content collections)
3. Write content
4. Update navigation in `BaseLayout.astro` if needed
5. Test and deploy

### Monitoring

- **Cloudflare Web Analytics:** Check dashboard for traffic and engagement
- **Formspree submissions:** Check email for feedback
- **Build logs:** Cloudflare Pages dashboard shows build status and errors

### Performance

Target Lighthouse scores: >90 across all metrics (Performance, Accessibility, Best Practices, SEO)

To test locally:
1. Build: `npm run build`
2. Preview: `npm run preview`
3. Run Lighthouse in Chrome DevTools on http://localhost:4321

## Troubleshooting

### Search not working

- Ensure `npm run build` completed successfully
- Verify `/dist/pagefind/` directory exists after build
- Check browser console for errors on `/search` page

### Feedback form not working

- Verify `PUBLIC_FORMSPREE_ENDPOINT` is set in Cloudflare Pages environment variables
- Check Formspree dashboard for submissions
- Ensure form endpoint URL is correct
- Test with a submission and verify email receipt

### Build fails

- Check Cloudflare Pages build logs
- Verify all dependencies are in `package.json`
- Ensure `NODE_VERSION` is 18+ if specified in environment variables
- Test build locally: `npm run build`

### DNS not propagating

- Wait 2–24 hours for nameserver changes
- Use https://dnschecker.org to check propagation
- Verify nameservers at registrar match Cloudflare's provided nameservers

### SSL certificate not provisioning

- Verify DNS is pointing to Cloudflare
- Wait up to 30 minutes for automatic provisioning
- Check Cloudflare Pages → Custom Domains for certificate status

## License

Content licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

Non-commercial use only. No ads, no affiliates, no selling.

## Contact

Use the [Feedback form](https://standing.one/feedback) for questions, suggestions, or corrections.

---

Built with Astro. Deployed on Cloudflare Pages. Maintained by Daniel Cowen.