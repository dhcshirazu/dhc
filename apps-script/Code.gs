/**
 * Contact form endpoint for the Digital Humanities Center (DHC) and its student association website.
 * Deploy as a Google Apps Script web app that executes as the designated account.
 * Configure Script Properties: SPREADSHEET_ID and NOTIFICATION_EMAIL.
 * The response page posts only a success flag and request token to the parent page.
 */
const CONFIG = {
  sheetName: 'Contact messages',
  maxPerEmailPerWindow: 3,
  rateWindowSeconds: 10 * 60,
  minCompletionMs: 2500,
  maxNameLength: 100,
  maxEmailLength: 200,
  maxTopicLength: 160,
  maxMessageLength: 5000
};

function doGet() {
  return ContentService.createTextOutput('DHC contact endpoint is ready. Submit the contact form from the official website.');
}

function doPost(e) {
  const p = (e && e.parameter) || {};
  const requestId = safeRequestId(p.requestId);
  let success = false;
  try {
    if (String(p.website || '').trim()) throw new Error('Spam honeypot triggered.');
    const startedAt = Number(p.startedAt || 0);
    if (!startedAt || Date.now() - startedAt < CONFIG.minCompletionMs || Date.now() - startedAt > 24 * 60 * 60 * 1000) {
      throw new Error('Invalid form timing.');
    }
    const name = cleanText(p.name, CONFIG.maxNameLength);
    const email = cleanEmail(p.email);
    const topic = cleanText(p.topic, CONFIG.maxTopicLength);
    const message = cleanText(p.message, CONFIG.maxMessageLength);
    if (!name || !email || !topic || !message || p.privacyAcknowledged !== 'yes') throw new Error('Required fields are missing.');
    applyRateLimit(email);

    const props = PropertiesService.getScriptProperties();
    const spreadsheetId = props.getProperty('SPREADSHEET_ID');
    const notificationEmail = props.getProperty('NOTIFICATION_EMAIL');
    if (!spreadsheetId || !notificationEmail) throw new Error('Server is not configured.');

    const receivedAt = new Date();
    let notificationStatus = 'sent';
    try {
      MailApp.sendEmail({
        to: notificationEmail,
        subject: '[DHC website] New contact message: ' + topic.replace(/[\r\n]+/g, ' ').slice(0, 100),
        body: [
          'A new message was submitted through the association website.',
          '', 'Name: ' + name, 'Email: ' + email, 'Topic: ' + topic,
          '', 'Message:', message,
          '', 'Received at: ' + receivedAt.toISOString(),
          'Reply directly to the sender using the supplied email address.'
        ].join('\n'),
        replyTo: email,
        name: 'DHC website contact form'
      });
    } catch (mailError) {
      notificationStatus = 'failed: ' + String(mailError.message || mailError).slice(0, 180);
    }

    const spreadsheet = SpreadsheetApp.openById(spreadsheetId);
    let sheet = spreadsheet.getSheetByName(CONFIG.sheetName);
    if (!sheet) sheet = spreadsheet.insertSheet(CONFIG.sheetName);
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Received at (UTC)', 'Name', 'Email', 'Topic', 'Message', 'Notification status', 'Request ID']);
      sheet.setFrozenRows(1);
    }
    // Do not delete submissions automatically. Administrators review and delete per the privacy policy.
    sheet.appendRow([receivedAt.toISOString(), safeSheetValue(name), safeSheetValue(email), safeSheetValue(topic), safeSheetValue(message), safeSheetValue(notificationStatus), safeSheetValue(requestId)]);
    success = true;
  } catch (error) {
    console.error('Contact form rejected or failed: ' + String(error && error.message || error));
    success = false;
  }
  return responsePage(success, requestId);
}

function cleanText(value, maxLength) {
  return String(value || '').replace(/\u0000/g, '').trim().slice(0, maxLength);
}

function safeSheetValue(value) {
  const text = String(value == null ? '' : value);
  // Prevent user-controlled text from being interpreted as a spreadsheet formula.
  return /^[=+@\-\t\r]/.test(text) ? "'" + text : text;
}

function cleanEmail(value) {
  const email = cleanText(value, CONFIG.maxEmailLength);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) throw new Error('Invalid email address.');
  return email;
}

function safeRequestId(value) {
  const input = String(value || '').slice(0, 80);
  return /^[a-zA-Z0-9_-]{1,80}$/.test(input) ? input : '';
}

function applyRateLimit(email) {
  const digest = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, email.toLowerCase());
  const key = 'contact:' + Utilities.base64EncodeWebSafe(digest).replace(/=+$/g, '').slice(0, 40);
  const cache = CacheService.getScriptCache();
  const current = Number(cache.get(key) || 0);
  if (current >= CONFIG.maxPerEmailPerWindow) throw new Error('Rate limit reached.');
  cache.put(key, String(current + 1), CONFIG.rateWindowSeconds);
}

function responsePage(success, requestId) {
  const payload = JSON.stringify({ source: 'dhc-contact-form', success: Boolean(success), requestId: requestId });
  const safePayload = payload.replace(/</g, '\\u003c');
  const output = HtmlService.createHtmlOutput(
    '<!doctype html><html><head><meta charset="utf-8"><title>Contact form response</title></head>' +
    '<body><p>Submission response sent.</p><script>window.top.postMessage(' + safePayload + ', "*");</script></body></html>'
  );
  // The iframe response reveals no message contents; it only posts the result token to the parent.
  return output.setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
