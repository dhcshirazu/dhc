# Deployment and configuration

## GitHub Pages

1. Put the repository under an institution-controlled GitHub organization or institutional account. Add a second trusted administrator and keep recovery methods current.
2. Push the complete repository to the default branch, named `main` in the included workflow.
3. Open **Settings → Pages → Build and deployment** and choose **GitHub Actions** as the source.
4. Inspect the **Build and publish DHC website** workflow under **Actions**. It runs `python build.py`, checks the generated pages, uploads `dist/`, and deploys the generated site.
5. Add the resulting public site URL to `content/site-settings.json` as `publicBaseUrl` (without a trailing slash), commit the change, and let the workflow redeploy.

For the current `dhc_website` repository, the default project-site URL is `https://<GITHUB-OWNER>.github.io/dhc_website/`, where `<GITHUB-OWNER>` is the exact GitHub username or organization that owns the repository. Set `publicBaseUrl` to the same URL without the trailing slash, for example `https://<GITHUB-OWNER>.github.io/dhc_website`. The site uses relative internal links, while `publicBaseUrl` is required for canonical links and the sitemap. If using a custom domain, configure the domain in GitHub Pages settings and add the appropriate DNS records; a `CNAME` file alone does not configure DNS.

## Pages CMS editor interface

[Pages CMS](https://app.pagescms.org/) is the recommended browser-based editor. It edits files in the repository and saves changes through GitHub; it does not require a separate content database.

1. Sign in using the association-approved GitHub account.
2. Install the Pages CMS GitHub App on the website repository only, with the least access its workflow requires.
3. Open the repository and ensure the `.pages.yml` file is present at the repository root.
4. Use the configured groups (`DHC site settings and contacts`, `Events`, `Webinar archive`, `Articles and tutorials`, `Current and former members`, `Announcements`, and `Certificate verification records`) to edit content.
5. Make content edits on a review branch or through pull requests where practical. Only approved changes should reach `main`.

Pages CMS authentication is not a substitute for repository permissions. Only trusted, authorized GitHub accounts should have write access. The public website and source repository may expose committed data, so never save contact-form submissions, private consent records, passwords, recovery codes, or other secrets in this repository.

## Local preview

```sh
python build.py
python -m http.server 8000 --directory dist
```

Browse to `http://localhost:8000/`. The page works without a framework, package install, or Node build step.

## Contact-form backend

The contact form has no active endpoint in the starter repository. It becomes submittable only after `appsScriptWebAppUrl` is set.

1. Use an institution-controlled Google account. Create a new Apps Script project and copy `apps-script/Code.gs` into it.
2. Create a Google spreadsheet for private message storage. Share it only with designated association administrators and the institutional account running the script.
3. In Apps Script **Project Settings → Script Properties**, set:
   - `SPREADSHEET_ID` — the ID from the spreadsheet URL.
   - `NOTIFICATION_EMAIL` — the designated inbox that receives message alerts.
4. Save the script and deploy it as a **Web app**, executing as the designated account. The public needs access to submit the form; use the deployment access option that allows anonymous/public visitors, if permitted by the institution's policy.
5. Authorize the requested Google services. Copy the deployed `/exec` URL into `appsScriptWebAppUrl` in `content/site-settings.json` and commit.
6. Submit a test message from English and Persian pages. Confirm the response is announced to a screen reader, the row is stored, the inbox is notified, and non-admin accounts cannot open the spreadsheet.
7. Test the honeypot/rate limit in a controlled environment. A hidden honeypot and per-email rate limit reduce simple spam but do not equal a full CAPTCHA. If abuse becomes material, switch to a Google Form with appropriate Google abuse protections or add an independently reviewed verification step.

The Apps Script response uses an iframe and `postMessage` so the website can display a clear success/error state without reading cross-origin response data. The response frame is configured to allow embedding; the page sends only a submission result and request token, not form content. Do not reuse the script for unrelated sensitive data.

## Verification before launch

- Test keyboard-only navigation, visible focus, theme toggle, mobile navigation, archive filters, empty states, and language switching.
- Verify every external link uses HTTPS and is the correct official destination.
- Test a valid and an invalid certificate number in both languages; confirm no personal fields beyond those approved appear.
- Test an expired event link and all three webinar recording states (available with permission, not recorded, and permission not granted).
- Check the current Chrome, Firefox, Safari, and a mobile browser where practical. Use an automated accessibility checker, then do manual keyboard and screen-reader checks; a successful automated scan is not a WCAG certification.
