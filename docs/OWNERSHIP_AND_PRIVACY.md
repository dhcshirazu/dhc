# Ownership, access transfer, and privacy checklist

## Institutional ownership

Use institution-controlled accounts wherever possible. Do not make a graduating student the sole owner of any critical account or recovery method.

Maintain an access register outside the public repository with the account/service, institutional owner, at least two trusted administrators, recovery method, and last access review. Never publish passwords, backup codes, OAuth secrets, API keys, private consent evidence, or personal contact submissions in GitHub issues or this repository.

### GitHub

- Prefer a GitHub organization controlled by the department or institution.
- Keep at least two trusted organization/repository administrators and require two-factor authentication where available.
- Grant write access only to editors who need it. Remove access promptly when an officer leaves.
- Keep the Pages deployment environment restricted to the trusted default branch where the organization supports environment protection rules.
- Use pull requests and review for certificate records, public personal information, and official contact updates.

### Google account and Apps Script

- Use a designated institutional Google account, not one officer's personal Gmail, as the Apps Script owner and notification sender.
- Share the contact spreadsheet only with the current designated administrators. Verify permissions from a separate non-admin account.
- Keep two administrators able to recover the institutional account under institution policy. Document the script deployment URL and script-property names in the private access register; never put spreadsheet IDs or credentials in public issues if the institution treats them as confidential.
- On officer transition, verify the script still executes under the institutional account, notification email is current, and former officers no longer have spreadsheet access.

### Official social channels and domain

Maintain a private list of official channels: Telegram, Instagram, LinkedIn, and any additional channel. For each channel document its canonical URL, institutional owner, current custodians, recovery email/phone (in a private system), two-factor status, and transfer procedure.

- Link only to verified official profiles. Do not embed social feeds; use accessible text links.
- At each handover, update account ownership and recovery methods before removing the outgoing officers.
- If a channel becomes inactive, inaccessible, or changes ownership, remove or label the old link on the website and publish an update on remaining official channels.
- Keep the domain registrar and DNS under institutional control, with at least two trusted contacts.

## Contact-message privacy

The form requests only name, email, topic, message, and an acknowledgement of the privacy notice. It should not request sensitive data. Contact messages are used to answer the sender or route the enquiry to the appropriate association administrator.

- Access: the designated institutional account and administrators explicitly granted spreadsheet access.
- Notifications: sent to the configured association inbox. Email is not the long-term record; the restricted spreadsheet is the storage location.
- Retention target: review for deletion 12 months after the matter is closed, unless an institutional or legal requirement justifies retaining the record longer. Deletion is manual; there is no automatic deletion task in this starter.
- Review spreadsheet permissions at each officer transition and at least once per academic term.
- If the form is not configured or fails, keep a working official contact route on the page.
- The current anti-spam measures (honeypot, minimum completion time, per-email rate limit, Google account/mail protections) are basic. Monitor abuse and consider Google Forms or an additional challenge if needed.

## Consent and public content

- Obtain explicit, recorded consent before publishing a person's name and role; obtain separate permission for photographs.
- Do not commit consent forms or private evidence to the public repository. Keep consent documentation in institution-approved restricted storage.
- Before publishing a certificate record, confirm that the holder has been informed that the certificate number, name, issue date, and description are publicly verifiable and the underlying static JSON can be downloaded.
- Review social URLs, officer names, public emails, webinar rights, registration links, and image rights when an officer changes.

## Handover checklist

1. Review GitHub organization/repository, CMS, domain, DNS, Google Apps Script, spreadsheet, inbox, and all official social channels.
2. Add the incoming trusted administrators and verify they can recover each account.
3. Update the association head, supervisor, official contact details, and term dates in `content/site-settings.json`.
4. Remove outgoing members from access groups after transfer has been tested.
5. Test message submission, certificate verification, deployment, language switching, and all public links.
6. Record the date and responsible administrators in the private access register.
