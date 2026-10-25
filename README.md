# Digital Humanities Student Association — Shiraz University

A bilingual, accessible static website for the Digital Humanities Student Association at Shiraz University, within the Faculty of Humanities and Letters and the Department of Foreign Languages and Linguistics.

## What is included

- Separate English (`/en/`) and Persian (`/fa/`) pages with LTR/RTL layouts and page-equivalent language links.
- Responsive design, light/dark themes, visible keyboard focus, semantic page structure, and empty states for unpublished content.
- Distinct archive pages for events, webinars, articles, members, plus certificate verification and a privacy page.
- Search/filter controls for title/keyword, date range, and tags. Topic tags link to the relevant archive with the topic preselected.
- A configurable certificate-number pattern. The current rule is explicitly a placeholder.
- A Google Apps Script contact form integration; the form remains disabled until the institutional endpoint is configured.
- Pages CMS configuration for browser-based editing of JSON content files, plus a GitHub Actions build/deploy workflow.
- A simple Python builder using only the Python standard library.

The repository starts with empty event, webinar, article, member, announcement, and certificate records. It does not invent real officers, contact details, events, articles, or certificate holders. Add only approved content before launch.

## Run and inspect locally

Python 3.10+ is sufficient; no package installation is needed.

```sh
python build.py
python check_site.py
python -m http.server 8000 --directory dist
```

Open `http://localhost:8000/`. Use a local HTTP server instead of opening HTML files directly: certificate lookup fetches the JSON registry.

## Source folders

- `content/*.json` — editable source content and site settings.
- `content/media/` — uploaded images used in article and member records.
- `.pages.yml` — schema for Pages CMS.
- `build.py` — validates and builds published records into static pages.
- `assets/` — style sheet, client-side behavior, illustration, favicon, and social preview artwork.
- `apps-script/Code.gs` — optional contact form server-side endpoint.
- `.github/workflows/pages.yml` — build and deploy workflow.
- `docs/` — setup, editing, privacy, and ownership guidance.

## Important operational notes

1. **Do not publish unconsented member details or photographs.** A profile is omitted unless `consentToPublish` is `true`; a photo appears only when `photoConsent` is also `true`.
2. **The certificate registry is public static content.** It contains only the seven approved display fields and is downloadable as part of the website. Do not add birth dates, contact details, student IDs, signatures, or other personal information. A static registry cannot prevent bulk enumeration; see `docs/CONTENT_WORKFLOW.md` for the server-side alternative when non-enumerability is a requirement.
3. **Contact messages are not deleted automatically.** Restrict the linked spreadsheet to designated administrators and review retention on a regular schedule.
4. **Replace all blank account URLs, email addresses, and contacts before launch.** Configure `publicBaseUrl` so canonical and sitemap URLs can be generated.
5. **GitHub Pages is static hosting.** Form submission processing is handled by the separately deployed Google Apps Script web app.

## First launch sequence

1. Create or select an institution-controlled GitHub organization/repository and add at least two trusted administrators.
2. Configure the public URL and official contacts in `content/site-settings.json`.
3. Configure Pages CMS if browser-based editing is desired.
4. Configure Google Apps Script and test the contact form.
5. Review content consent, certificate privacy, links, and translations.
6. In GitHub repository settings, set **Pages → Build and deployment → Source → GitHub Actions**.
7. Push to `main`; the workflow builds `dist/` and deploys it.

Read `docs/DEPLOYMENT.md`, `docs/CONTENT_WORKFLOW.md`, and `docs/OWNERSHIP_AND_PRIVACY.md` before publishing.
