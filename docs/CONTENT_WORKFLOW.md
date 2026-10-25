# Content editing and editorial workflow

## Editorial path

1. A contributor submits an article, event proposal, or webinar record to the association's editorial contact.
2. An editor checks accuracy, permissions, links, accessibility, translations, calendar dates, and rights.
3. An authorized editor updates the relevant JSON through Pages CMS or a Git commit/pull request.
4. A reviewer checks the diff. Approved content is merged into `main`.
5. GitHub Actions rebuilds and publishes the website automatically. If the build fails, read the workflow log, correct the JSON, and retry.

Content remains in readable JSON files under `content/`. Avoid manually editing the generated `dist/` folder; it is recreated by `build.py` and deployed as a build artifact.

## Content files

### Events — `content/events.json`

Each published event needs a lowercase, hyphenated `slug`, English and Persian titles, `dateISO` in Gregorian `YYYY-MM-DD`, `dateEn`, and `dateFa` in the Persian calendar. The two display dates are maintained explicitly; do not guess a Persian-calendar date. Include speaker name, speaker timezone (`Area/City` IANA name), speaker-local time, Tehran time, language, modality, platform/venue, a bilingual abstract, and topic tags.

Use HTTPS registration/attendance URLs only. Add `linkExpiresAt` as an ISO timestamp with timezone, such as `2026-11-04T18:00:00+03:30`, when the platform link has a known expiry. Links are hidden once the event date is past or the expiry time has passed. Do not leave permanent Meet/Skype/Adobe Connect URLs in archived pages.

Set `published` to `true` only when the information is confirmed. Unpublished records remain source content and are not rendered.

### Webinars — `content/webinars.json`

Set `recordingStatus` to one of:

- `available` — only if `rightsApproved` is `true` and `recordingUrl` is a valid YouTube URL. The site then shows the link.
- `not_recorded` — the session was not recorded.
- `restricted` — it was recorded, but the speaker has not permitted sharing.
- `unknown` — the status has not yet been confirmed.

Keep title and description in both languages, plus speaker, date in both calendars, topic tags, and publication status. Never infer permission from the presence of a video link.

### Articles — `content/articles.json`

Use a stable, lowercase hyphenated `slug`, paired English/Persian titles and summaries, author credit, ISO date and both display dates, topic tags, and `published: true` after editorial approval. Write `bodyEn` and `bodyFa` as plain text; separate paragraphs with a blank line. Use `topicTags` consistently so tags connect related articles and webinars.

Upload images to `content/media/`. Put the resulting media path in `imageUrl` and provide meaningful `imageAltEn` and `imageAltFa` text. A caption or source attribution should be included in the article body when needed. Do not use an image unless the association has permission to publish it.

### Members — `content/members.json`

Record each member's public name, both-language role, service term, concise biography (optional), and whether they are current. Do not publish a profile unless `consentToPublish` is `true`. Store photo permissions separately: `photoConsent` must also be `true` before showing `photoUrl`. A photo alt text should convey the useful information without merely repeating a name. Review consent if a profile or photograph is reused in a new context.

The current/former archive is derived from `current`. The page intentionally displays no private email, phone number, student number, or other personal contact details by default.

### Announcements — `content/announcements.json`

Enter the title, text, Gregorian ISO date plus English and Persian display dates, and set `published` to `true` only after confirmation. Link only to an internal page or verified HTTPS URL. Announcements appear on the home page in reverse date order.

### Certificates — `content/certificates.json`

Each record must contain exactly these seven fields:

- `number`
- `holderNameEn`
- `holderNameFa`
- `issueDateEn`
- `issueDateFa`
- `descriptionEn`
- `descriptionFa`

Do not add email, phone, national/student ID, date of birth, signature image, grades, or any other field. A build-time validation fails if extra fields are added or certificate numbers are duplicated. Only trusted GitHub editors should add/correct records. The site and repository are public: even though the verification page asks for a number, the static registry can be downloaded and enumerated. The included lookup is suitable only when the listed name/date/type are intentionally public. If certificate holders must not be enumerable, move the registry to a private data source and use a server-side lookup that returns only the requested match.

### Site settings — `content/site-settings.json`

This file contains public contact names/emails, official social URLs, base URL, contact form endpoint URL, certificate format regex, and retention period. Do not place credentials or API tokens here. The certificate regex is currently a broad placeholder (`^[A-Z0-9-]{4,24}$`). Agree the final format with the association before replacing it.

## Bilingual consistency

- Keep language links on the equivalent page, and use the same slug across English/Persian versions of an item.
- Maintain paired English and Persian event dates. The Gregorian ISO value powers sorting/filtering; the display strings should be reviewed by a Persian-calendar-literate editor.
- Use a Persian-capable system font stack (`Vazirmatn`, `Noto Sans Arabic`, `Tahoma`, then a sans-serif fallback). Preserve ZWNJ where orthographically appropriate.
- When a translation is not ready, leave its field blank; the build shows the available version with a translation notice rather than silently inventing a translation.
- Use one spelling consistently for the association name, academic unit names, topic tags, roles, and recording status labels.
