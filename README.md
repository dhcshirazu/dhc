# DHC — Digital Humanities Center & Student Association | Shiraz University

A bilingual, accessible static website for the **Digital Humanities Center (DHC)** and its student association at Shiraz University, within the Faculty of Humanities and Letters and the Department of Foreign Languages and Linguistics.

## Naming convention

- **English brand:** Digital Humanities Center (DHC)
- **English description:** the Center and its student association
- **Persian brand:** مرکز علوم انسانی دیجیتال (DHC)
- **Persian description:** مرکز علوم انسانی دیجیتال (DHC) و انجمن دانشجویی آن
- **GitHub repository:** `dhc_website`
- **Expected GitHub Pages URL:** `https://<GITHUB-OWNER>.github.io/dhc_website/`

Replace `<GITHUB-OWNER>` with the exact GitHub username or organization that owns the repository. The brand wording used in generated pages is centralized in `build.py` under `LABELS`; update both language entries there if the approved wording changes. The `dhc-` prefix is used for browser storage keys and the contact-form message protocol.

## What is included

- Separate English (`/en/`) and Persian (`/fa/`) pages with LTR/RTL layouts and page-equivalent language links.
- Responsive design, light/dark themes, visible keyboard focus, semantic page structure, and empty states for unpublished content.
- Distinct archive pages for events, webinars, articles, members, certificate verification, and privacy.
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
- `check_site.py` — validates generated page structure, local links, images, and certificate records.
- `assets/` — styles, client-side behavior, illustration, favicon, and social preview artwork.
- `apps-script/Code.gs` — optional contact form server-side endpoint.
- `.github/workflows/pages.yml` — build and deploy workflow.
- `docs/` — deployment, content, privacy, and ownership guidance.

## Important operational notes

1. **Do not publish unconsented member details or photographs.** A profile is omitted unless `consentToPublish` is `true`; a photo appears only when `photoConsent` is also `true`.
2. **The certificate registry is public static content.** It contains only the seven approved display fields and is downloadable as part of the website. Do not add birth dates, contact details, student IDs, signatures, or other personal information. A static registry cannot prevent bulk enumeration; see `docs/CONTENT_WORKFLOW.md` for the server-side alternative when non-enumerability is a requirement.
3. **Contact messages are not deleted automatically.** Restrict the linked spreadsheet to designated administrators and review retention on a regular schedule.
4. **Configure the public site URL before launch.** Set `publicBaseUrl` in `content/site-settings.json` to `https://<GITHUB-OWNER>.github.io/dhc_website` without the trailing slash. Replace `<GITHUB-OWNER>` with the actual account or organization name.
5. **GitHub Pages is static hosting.** Contact-form processing is handled by the separately deployed Google Apps Script web app.
6. **Keep institutional control of the repository and integrations.** Maintain at least two trusted administrators and document recovery and handover procedures outside the public repository.

## First launch sequence

1. Upload this project to the `dhc_website` repository's root. Do not put the contents inside an extra nested `dhc_website/` directory.
2. Set `publicBaseUrl` in `content/site-settings.json` to the expected URL without the final slash.
3. Push to the `main` branch and set **Settings → Pages → Build and deployment → Source → GitHub Actions**.
4. Check **Actions** and wait for the build and deployment jobs to complete successfully.
5. Open `https://<GITHUB-OWNER>.github.io/dhc_website/` and confirm that the English and Persian pages load.
6. Configure Pages CMS if browser-based editing is desired.
7. Configure Google Apps Script, add approved content, and test forms, links, translations, and certificate privacy before announcing the website.

Read `docs/DEPLOYMENT.md`, `docs/CONTENT_WORKFLOW.md`, and `docs/OWNERSHIP_AND_PRIVACY.md` before publishing.
