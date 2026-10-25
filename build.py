#!/usr/bin/env python3
"""Build the bilingual Digital Humanities Center (DHC) and student association website.

Content source files live in content/*.json. This script uses only the Python
standard library and writes the deployable site to dist/.
"""
from __future__ import annotations
import html
import json
import re
import shutil
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
DIST = ROOT / "dist"
TODAY_TEHRAN = datetime.now(ZoneInfo("Asia/Tehran"))

NAV = {
    "en": [
        ("home", "Home", "index.html"), ("about", "About", "about.html"),
        ("members", "Members", "members.html"), ("events", "Events", "events.html"),
        ("webinars", "Webinars", "webinars.html"), ("articles", "Articles", "articles.html"),
        ("contact", "Contact", "contact.html"), ("certificates", "Verify certificate", "certificates.html"),
    ],
    "fa": [
        ("home", "خانه", "index.html"), ("about", "درباره", "about.html"),
        ("members", "اعضا", "members.html"), ("events", "رویدادها", "events.html"),
        ("webinars", "وبینارها", "webinars.html"), ("articles", "مقاله‌ها", "articles.html"),
        ("contact", "تماس", "contact.html"), ("certificates", "اعتبارسنجی گواهی", "certificates.html"),
    ],
}
LABELS = {
    "en": {
        "university": "Shiraz University · Faculty of Humanities and Letters",
        "department": "Department of Foreign Languages and Linguistics",
        "association": "Digital Humanities Center (DHC)",
        "tagline": "Humanities, in dialogue with computation.",
        "footer_intro": "The Digital Humanities Center (DHC) and its student association explore how digital methods can support humanities research, teaching, and public engagement.",
        "footer_nav": "Explore", "footer_contact": "Contact", "privacy": "Privacy and data use",
        "admin_note": "Content is maintained by authorized DHC editors.", "theme": "Theme", "language": "فارسی",
        "skip": "Skip to main content", "menu": "Menu", "dark": "Dark", "light": "Light",
        "see_all": "View all", "read_more": "Read article", "details": "Full details", "register": "Registration",
        "join": "Attendance link", "expired": "This event has ended; attendance and registration links are no longer available.",
        "link_expired": "This link has expired or is unavailable.", "online": "Online", "in_person": "In person",
        "speaker": "Speaker", "speaker_time": "Speaker local time", "tehran_time": "Tehran time", "timezone": "Speaker timezone",
        "date": "Date", "language_label": "Language", "format": "Format", "platform": "Platform / venue", "abstract": "Abstract",
        "topic": "Topics", "status": "Recording status", "recording_available": "Approved recording on YouTube",
        "not_recorded": "This session was not recorded.", "restricted": "The speaker has not permitted the recording to be shared.",
        "permission_pending": "Permission to share has not been confirmed, so no recording link is provided.",
        "unknown_recording": "Recording status or the approved link has not been confirmed. Contact the association for details.",
        "filter_search": "Search by title or keyword", "filter_from": "From date", "filter_to": "To date", "filter_topic": "Topic",
        "all_topics": "All topics", "no_results": "No results match these filters.", "result_count": "Results", "clear_hint": "Try a shorter title or remove one of the filters.",
        "announcements": "Announcements", "upcoming": "Next session", "latest_articles": "Recently published", "latest_webinars": "Recent webinars",
        "no_upcoming_title": "No upcoming sessions are scheduled yet", "no_upcoming": "New events will appear here once the program is confirmed.",
        "no_announcements_title": "No recent announcements", "no_announcements": "There are no published updates at the moment.",
        "no_articles_title": "No articles published yet", "no_articles": "Approved tutorials and essays will appear here after editorial review.",
        "no_webinars_title": "The archive is being prepared", "no_webinars": "Published webinar records will appear here. Recording availability is stated individually.",
        "no_events_title": "No events to display", "no_events": "The association will publish the schedule here when details are confirmed.",
        "no_members_title": "No public member profiles", "no_members": "Member information is shown only after the relevant consent has been obtained.",
        "no_certificates_title": "No matching certificate", "certificate_note": "Enter the certificate number exactly as printed. This lookup displays only the holder name, issue date, and certificate type.",
        "certificate_format": "Temporary format rule", "certificate_heading": "Certificate verification", "certificate_submit": "Verify certificate",
        "contact_head": "Student association lead", "contact_supervisor": "Faculty supervisor", "not_configured": "Not configured yet",
        "message_form": "Send a message", "name": "Name", "email": "Email address", "subject": "Topic", "message": "Message",
        "send": "Submit message", "privacy_consent": "I understand this information will be used only to respond to my message.",
        "privacy_explain": "The form collects your name, email address, topic, and message. Designated association administrators can access submissions to respond to you. Submissions are not deleted automatically; the intended retention period is 12 months after the matter is closed, followed by a review for deletion. Do not include sensitive information. Contact the association through the published email links if you prefer not to use this form.",
        "translation_missing": "The English version is not available yet; the Persian text is shown here.",
        "former_members": "Former members", "current_members": "Current members", "aims": "Aims and activities", "workflow": "How to contribute",
        "member_consent": "Before adding a member profile, obtain explicit consent for the name and role. Obtain separate permission for photographs and use descriptive alt text.",
        "about_intro": "The Digital Humanities Center (DHC) and its student association bring students together to explore the questions, methods, and tools that connect the humanities with digital research.",
        "about_one_title": "Methods with context", "about_one": "Explore text analysis, digital archives, mapping, data visualization, computational methods, and critical approaches to digital culture.",
        "about_two_title": "Peer learning", "about_two": "Create space for workshops, talks, reading groups, tutorials, and collaborative projects across languages and disciplines.",
        "about_three_title": "Careful publishing", "about_three": "Share useful work accessibly, credit its authors, respect participants’ rights, and distinguish confirmed information from plans.",
        "article_author": "Author", "published": "Published", "back_articles": "Back to articles", "back_events": "Back to events", "back_webinars": "Back to webinars",
        "error_title": "Page not found", "error_body": "This address may be outdated or the page may have moved. Use the navigation to continue.",
        "privacy_title": "Privacy and data use", "privacy_body": "The DHC student association collects only the information needed to respond to contact messages. Published member details and photographs require explicit consent. Certificate verification shows only the four fields listed on the verification page.",
        "not_public": "This record is not published.", "session_details": "Session details", "rights_note": "A recording link is shown only when the recording is available and sharing permission has been confirmed.",
        "date_pair": "Gregorian and Persian calendar dates are listed together for events.", "contact_alternative": "The contact details below are the alternative route when the form is unavailable.",
    },
    "fa": {
        "university": "دانشگاه شیراز · دانشکده علوم انسانی و ادبیات",
        "department": "گروه زبان‌های خارجی و زبان‌شناسی",
        "association": "مرکز علوم انسانی دیجیتال (DHC)",
        "tagline": "علوم انسانی در گفت‌وگو با محاسبات.",
        "footer_intro": "مرکز علوم انسانی دیجیتال (DHC) و انجمن دانشجویی آن، نقش روش‌های دیجیتال را در پژوهش، آموزش و ارتباط عمومی در علوم انسانی بررسی می‌کنند.",
        "footer_nav": "بخش‌ها", "footer_contact": "تماس", "privacy": "حریم خصوصی و استفاده از داده‌ها",
        "admin_note": "محتوا به‌وسیله ویرایشگران مجاز DHC مدیریت می‌شود.", "theme": "پوسته", "language": "English",
        "skip": "رفتن به محتوای اصلی", "menu": "منو", "dark": "تیره", "light": "روشن",
        "see_all": "مشاهده همه", "read_more": "مطالعه مقاله", "details": "جزئیات کامل", "register": "ثبت‌نام",
        "join": "پیوند حضور", "expired": "این رویداد پایان یافته است؛ پیوندهای ثبت‌نام و حضور دیگر در دسترس نیستند.",
        "link_expired": "این پیوند منقضی شده یا در دسترس نیست.", "online": "برخط", "in_person": "حضوری",
        "speaker": "سخنران", "speaker_time": "زمان محلی سخنران", "tehran_time": "زمان تهران", "timezone": "منطقه زمانی سخنران",
        "date": "تاریخ", "language_label": "زبان", "format": "شیوه برگزاری", "platform": "بستر / محل برگزاری", "abstract": "چکیده",
        "topic": "موضوع‌ها", "status": "وضعیت ضبط", "recording_available": "نسخه ضبط‌شده با مجوز در یوتیوب",
        "not_recorded": "این نشست ضبط نشده است.", "restricted": "سخنران اجازه انتشار نسخه ضبط‌شده را نداده است.",
        "permission_pending": "اجازه انتشار تأیید نشده است؛ بنابراین پیوند ضبط نمایش داده نمی‌شود.",
        "unknown_recording": "وضعیت ضبط یا پیوند مجاز هنوز تأیید نشده است. برای اطلاعات بیشتر با انجمن تماس بگیرید.",
        "filter_search": "جست‌وجو بر اساس عنوان یا کلیدواژه", "filter_from": "از تاریخ", "filter_to": "تا تاریخ", "filter_topic": "موضوع",
        "all_topics": "همه موضوع‌ها", "no_results": "نتیجه‌ای با این فیلترها پیدا نشد.", "result_count": "نتیجه", "clear_hint": "عنوان کوتاه‌تری وارد کنید یا یکی از فیلترها را بردارید.",
        "announcements": "اطلاعیه‌ها", "upcoming": "نشست پیشِ رو", "latest_articles": "تازه‌ترین مطالب", "latest_webinars": "وبینارهای اخیر",
        "no_upcoming_title": "هنوز نشستی برای آینده برنامه‌ریزی نشده است", "no_upcoming": "پس از نهایی‌شدن برنامه، رویدادهای تازه در این بخش نمایش داده می‌شوند.",
        "no_announcements_title": "اطلاعیه تازه‌ای منتشر نشده است", "no_announcements": "در حال حاضر به‌روزرسانی منتشرشده‌ای وجود ندارد.",
        "no_articles_title": "هنوز مقاله‌ای منتشر نشده است", "no_articles": "راهنماها و مقاله‌های تأییدشده پس از بازبینی در این بخش قرار می‌گیرند.",
        "no_webinars_title": "آرشیو در حال آماده‌سازی است", "no_webinars": "اطلاعات وبینارهای منتشرشده در این بخش قرار می‌گیرد و وضعیت ضبط هر نشست جداگانه مشخص خواهد شد.",
        "no_events_title": "رویدادی برای نمایش وجود ندارد", "no_events": "پس از تأیید جزئیات، برنامه رویدادها در این بخش منتشر می‌شود.",
        "no_members_title": "نمایه عمومی اعضا موجود نیست", "no_members": "اطلاعات اعضا تنها پس از دریافت رضایت مربوط منتشر می‌شود.",
        "no_certificates_title": "گواهی منطبقی پیدا نشد", "certificate_note": "شماره را دقیقاً مطابق نسخه چاپ‌شده وارد کنید. نتیجه فقط نام دارنده، تاریخ صدور و نوع گواهی را نمایش می‌دهد.",
        "certificate_format": "الگوی موقت شماره", "certificate_heading": "اعتبارسنجی گواهی", "certificate_submit": "بررسی گواهی",
        "contact_head": "مسئول انجمن دانشجویی", "contact_supervisor": "استاد ناظر دانشکده", "not_configured": "هنوز تنظیم نشده است",
        "message_form": "ارسال پیام", "name": "نام", "email": "نشانی ایمیل", "subject": "موضوع", "message": "پیام",
        "send": "ارسال پیام", "privacy_consent": "می‌پذیرم که این اطلاعات فقط برای پاسخ‌گویی به پیامم استفاده شود.",
        "privacy_explain": "این فرم نام، نشانی ایمیل، موضوع و متن پیام را دریافت می‌کند. مدیران مشخص‌شده انجمن برای پاسخ‌گویی به پیام به اطلاعات دسترسی دارند. پیام‌ها به‌طور خودکار حذف نمی‌شوند؛ دوره نگهداری موردنظر ۱۲ ماه پس از بسته‌شدن موضوع است و پس از آن حذف بررسی می‌شود. اطلاعات حساس ارسال نکنید. در صورت تمایل به استفاده‌نکردن از فرم، از پیوندهای ایمیل منتشرشده استفاده کنید.",
        "translation_missing": "نسخهٔ فارسی هنوز آماده نیست؛ متن انگلیسی در این بخش نمایش داده می‌شود.",
        "former_members": "اعضای پیشین", "current_members": "اعضای فعلی", "aims": "اهداف و فعالیت‌ها", "workflow": "روش مشارکت",
        "member_consent": "پیش از افزودن نمایه، برای انتشار نام و نقش رضایت صریح بگیرید. اجازه انتشار عکس باید جداگانه دریافت شود و برای عکس متن جایگزین توصیفی بنویسید.",
        "about_intro": "مرکز علوم انسانی دیجیتال (DHC) و انجمن دانشجویی آن، دانشجویان را گرد هم می‌آورند تا پرسش‌ها، روش‌ها و ابزارهای پیونددهنده علوم انسانی و پژوهش دیجیتال را بررسی کنند.",
        "about_one_title": "روش‌شناسی همراه با زمینه", "about_one": "تحلیل متن، آرشیوهای دیجیتال، نقشه‌نگاری، مصورسازی داده، روش‌های محاسباتی و رویکردهای انتقادی به فرهنگ دیجیتال را بررسی کنید.",
        "about_two_title": "یادگیری همتا به همتا", "about_two": "برای کارگاه‌ها، سخنرانی‌ها، گروه‌های مطالعاتی، راهنماها و پروژه‌های مشترک میان زبان‌ها و رشته‌ها فضا ایجاد کنید.",
        "about_three_title": "انتشار مسئولانه", "about_three": "کارهای سودمند را دسترس‌پذیر منتشر کنید، نویسندگان را معرفی کنید، به حقوق مشارکت‌کنندگان احترام بگذارید و اطلاعات قطعی را از برنامه‌های احتمالی جدا کنید.",
        "article_author": "نویسنده", "published": "تاریخ انتشار", "back_articles": "بازگشت به مقاله‌ها", "back_events": "بازگشت به رویدادها", "back_webinars": "بازگشت به وبینارها",
        "error_title": "صفحه پیدا نشد", "error_body": "ممکن است نشانی قدیمی باشد یا صفحه جابه‌جا شده باشد. برای ادامه از راهبری سایت استفاده کنید.",
        "privacy_title": "حریم خصوصی و استفاده از داده‌ها", "privacy_body": "انجمن دانشجویی مرکز علوم انسانی دیجیتال فقط اطلاعات لازم برای پاسخ‌گویی به پیام‌ها را دریافت می‌کند. انتشار مشخصات اعضا و عکس‌ها به رضایت صریح نیاز دارد. صفحه اعتبارسنجی تنها چهار فیلد مشخص‌شده را نمایش می‌دهد.",
        "not_public": "این مورد منتشر نشده است.", "session_details": "جزئیات نشست", "rights_note": "پیوند ضبط تنها زمانی نمایش داده می‌شود که نسخه ضبط‌شده موجود و اجازه انتشار تأیید شده باشد.",
        "date_pair": "برای رویدادها، تاریخ میلادی و خورشیدی در کنار هم درج می‌شود.", "contact_alternative": "در صورت در دسترس‌نبودن فرم، از اطلاعات تماس زیر استفاده کنید.",
    },
}


def load_json(name: str):
    path = CONTENT / name
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return [] if name.endswith(".json") else {}


def esc(value) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def valid_url(value) -> str:
    value = str(value or "").strip()
    try:
        parsed = urlsplit(value)
        if parsed.scheme.lower() != "https" or not parsed.hostname or parsed.username or parsed.password:
            return ""
        return value
    except ValueError:
        return ""


def is_youtube_url(value: str) -> bool:
    if not valid_url(value):
        return False
    host = (urlsplit(value).hostname or "").lower().rstrip(".")
    return host == "youtu.be" or host.endswith(".youtu.be") or host == "youtube.com" or host.endswith(".youtube.com")


def valid_mail(value) -> str:
    value = str(value or "").strip()
    return value if re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value) else ""


def localized(item: dict, en_key: str, fa_key: str, lang: str, default=""):
    en = str(item.get(en_key) or "").strip()
    fa = str(item.get(fa_key) or "").strip()
    if lang == "fa":
        # Warn only when this reader's language is missing but the other is available.
        return (fa or en or default), bool(en and not fa)
    return (en or fa or default), bool(fa and not en)


def bdi(value) -> str:
    """Escape mixed-script text and isolate its bidi direction from surrounding UI."""
    return f'<bdi dir="auto">{esc(value)}</bdi>'


def translation_notice(missing: bool, lang: str) -> str:
    if not missing:
        return ""
    return f'<p class="not-configured" role="note">{esc(LABELS[lang]["translation_missing"])}</p>'


def fmt_paragraphs(text: str) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", str(text or "")) if p.strip()]
    return "".join(f'<p dir="auto">{esc(p).replace(chr(10), "<br>")}</p>' for p in paragraphs)


def date_value(value: str):
    try:
        return date.fromisoformat(str(value)[:10])
    except (ValueError, TypeError):
        return None


def event_has_ended(item: dict) -> bool:
    event_date = date_value(item.get("dateISO", ""))
    return bool(event_date and event_date < TODAY_TEHRAN.date())


def link_is_expired(item: dict) -> bool:
    if event_has_ended(item):
        return True
    raw = str(item.get("linkExpiresAt") or "").strip()
    if raw:
        try:
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=ZoneInfo("Asia/Tehran"))
            if dt <= datetime.now(timezone.utc):
                return True
        except ValueError:
            pass
    return False


def tag_links(tags, lang: str, route: str) -> str:
    if not tags:
        return ""
    chunks = []
    for tag in tags:
        tag = str(tag).strip()
        if not tag:
            continue
        href = f'{route}?tag={quote(tag)}'
        chunks.append(f'<a class="tag" href="{esc(href)}">{esc(tag)}</a>')
    return f'<div class="tag-list" aria-label="{esc(LABELS[lang]["topic"])}">{"".join(chunks)}</div>' if chunks else ""


def header_html(lang: str, current: str, page_key: str) -> str:
    L = LABELS[lang]
    other = "fa" if lang == "en" else "en"
    current_url = f"/{lang}/{current}"
    target_url = f"../{other}/{current}"
    nav_items = []
    for key, label, path in NAV[lang]:
        active = ' aria-current="page"' if key == page_key else ""
        extra = ' class="nav-certificate"' if key == "certificates" else ""
        nav_items.append(f'<a href="{esc(path)}"{extra}{active}>{esc(label)}</a>')
    language_label = L["language"]
    return f'''<a class="skip-link" href="#main">{esc(L["skip"])}</a>
<header class="site-header"><div class="shell header-inner">
  <a class="brand" href="index.html" aria-label="{esc(L['association'])} — {esc(L['university'])}">
    <span class="brand-mark" aria-hidden="true">DHC</span>
    <span class="brand-copy"><strong>{esc(L['association'])}</strong><small>{esc(L['university'])}</small></span>
  </a>
  <div class="header-tools">
    <a class="language-link" href="{esc(target_url)}" hreflang="{other}" lang="{other}" aria-label="Switch language">{esc(language_label)}</a>
    <button class="tool-button" type="button" data-theme-toggle aria-pressed="false"><span data-theme-label>{esc(L['dark'])}</span></button>
    <button class="tool-button nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="main-navigation">{esc(L['menu'])}</button>
  </div>
  <nav class="main-nav" id="main-navigation" data-main-nav aria-label="{'Main navigation' if lang == 'en' else 'راهبری اصلی'}">{''.join(nav_items)}</nav>
</div></header>'''


def footer_html(lang: str) -> str:
    L = LABELS[lang]
    paths = dict((key, path) for key, _, path in NAV[lang])
    return f'''<footer class="site-footer"><div class="shell footer-main">
  <div><a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">DHC</span><span class="brand-copy"><strong>{esc(L['association'])}</strong><small>{esc(L['department'])}</small></span></a><p style="margin-top:1rem;max-width:42ch">{esc(L['footer_intro'])}</p></div>
  <div><div class="footer-title">{esc(L['footer_nav'])}</div><ul class="footer-links">{''.join(f'<li><a href="{esc(path)}">{esc(label)}</a></li>' for _, label, path in NAV[lang][:7])}<li><a href="privacy.html">{esc(L['privacy'])}</a></li></ul></div>
  <div><div class="footer-title">{esc(L['footer_contact'])}</div><p>{esc(L['university'])}<br>{esc(L['department'])}</p><p><a href="contact.html">{esc(NAV[lang][6][1])}</a></p><p class="not-configured">{esc(L['admin_note'])}</p></div>
</div><div class="shell footer-bottom"><span>© {TODAY_TEHRAN.year} · {esc(L['association'])}</span><span>{esc(L['department'])}</span></div></footer>'''


def page_html(lang: str, current: str, page_key: str, title: str, description: str, body: str) -> str:
    L = LABELS[lang]
    direction = "rtl" if lang == "fa" else "ltr"
    other = "fa" if lang == "en" else "en"
    alt_path = f"/{other}/{current}"
    canonical = ""
    base = str(SETTINGS.get("publicBaseUrl") or "").rstrip("/")
    if base:
        canonical = f'<link rel="canonical" href="{esc(base)}/{lang}/{esc(current)}"><link rel="alternate" hreflang="en" href="{esc(base)}/en/{esc(current)}"><link rel="alternate" hreflang="fa" href="{esc(base)}/fa/{esc(current)}">'
    og_img = f'{base}/assets/images/social-card.svg' if base else '../assets/images/social-card.svg'
    theme_bootstrap = """(function(){try{var s=localStorage.getItem('dhc-theme');var d=window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches;document.documentElement.dataset.theme=s||(d?'dark':'light')}catch(e){}})();"""
    if title == L["association"]:
        document_title = f'{L["association"]} · {"Shiraz University" if lang == "en" else "دانشگاه شیراز"}'
    else:
        document_title = f'{title} · {L["association"]}'
    return f'''<!doctype html>
<html lang="{lang}" dir="{direction}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(document_title)}</title><meta name="description" content="{esc(description)}">
<meta name="color-scheme" content="light dark"><meta name="theme-color" content="#172724">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(document_title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:image" content="{esc(og_img)}"><meta name="twitter:card" content="summary_large_image">
{canonical}
<link rel="icon" href="../assets/images/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../assets/css/site.css">
<script>{theme_bootstrap}</script>
</head><body>
{header_html(lang, current, page_key)}
<main id="main">{body}</main>
{footer_html(lang)}
<script src="../assets/js/site.js" defer></script>
</body></html>'''


def page_intro(title: str, lead: str, lang: str, eyebrow: str = "Digital humanities") -> str:
    return f'''<section class="page-hero"><div class="shell"><p class="eyebrow">{esc(eyebrow if lang == 'en' else 'علوم انسانی دیجیتال')}</p><h1 dir="auto">{esc(title)}</h1><p class="lead" dir="auto">{esc(lead)}</p></div></section>'''


def empty_state(title: str, body: str) -> str:
    return f'<div class="empty-state"><strong>{esc(title)}</strong><p>{esc(body)}</p></div>'


def card_meta(parts) -> str:
    bits = [str(x) for x in parts if x]
    return f'<div class="card-meta">{"<span>·</span>".join(bdi(x) for x in bits)}</div>' if bits else ""


def event_card(event: dict, lang: str, detailed: bool = False) -> str:
    L = LABELS[lang]
    title, miss_t = localized(event, "titleEn", "titleFa", lang, "Untitled event")
    abstract, miss_a = localized(event, "abstractEn", "abstractFa", lang)
    date_label, miss_d = localized(event, "dateEn", "dateFa", lang)
    date_en = str(event.get("dateEn") or date_label).strip()
    date_fa = str(event.get("dateFa") or date_label).strip()
    paired_date = f'<span class="bidi" lang="en" dir="ltr">{esc(date_en)}</span><span aria-hidden="true"> · </span><span class="bidi" lang="fa" dir="rtl">{esc(date_fa)}</span>'
    modality = event.get("modality")
    modality_text = L["online"] if modality == "online" else L["in_person"] if modality == "in-person" else ""
    href = f'event-{esc(event.get("slug", ""))}.html'
    expired = link_is_expired(event)
    meta = f'<div class="card-meta">{paired_date}{("<span>·</span><span>" + bdi(event.get("speaker")) + "</span>") if event.get("speaker") else ""}{("<span>·</span><span>" + bdi(modality_text) + "</span>") if modality_text else ""}</div>'
    tags = tag_links(event.get("topicTags", []), lang, "events.html")
    links = ""
    if not expired:
        reg = valid_url(event.get("registrationUrl"))
        attendance = valid_url(event.get("attendanceUrl"))
        if reg:
            links += f'<a class="button secondary" href="{esc(reg)}" target="_blank" rel="noopener noreferrer">{esc(L["register"])}</a>'
        if attendance:
            links += f'<a class="button tertiary" href="{esc(attendance)}" target="_blank" rel="noopener noreferrer">{esc(L["join"])}</a>'
    else:
        expiry_message = L["expired"] if event_has_ended(event) else L["link_expired"]
        links += f'<p class="not-configured">{esc(expiry_message)}</p>'
    details = f'<a class="card-title-link" href="{href}"><h3 dir="auto">{esc(title)}</h3></a>'
    return f'''<article class="card" data-filter-card data-title="{esc(title)}" data-search="{esc(event.get('speaker', '') + ' ' + abstract)}" data-tags="{esc('|'.join(event.get('topicTags', [])))}" data-date="{esc(event.get('dateISO', ''))}">
      {meta}{details}{translation_notice(miss_t or miss_a or miss_d, lang)}
      {f'<p class="card-summary">{esc(abstract)}</p>' if abstract else ''}{tags}
      {f'<div class="hero-actions">{links}</div>' if links else ''}
    </article>'''


def article_card(article: dict, lang: str, archive: bool = False) -> str:
    L = LABELS[lang]
    title, mt = localized(article, "titleEn", "titleFa", lang, "Untitled article")
    summary, ms = localized(article, "summaryEn", "summaryFa", lang)
    date_label, md = localized(article, "dateEn", "dateFa", lang)
    slug = esc(article.get("slug", ""))
    href = f'article-{slug}.html'
    meta = card_meta([date_label, article.get("author")])
    tags = tag_links(article.get("topicTags", []), lang, "articles.html")
    return f'''<article class="card" data-filter-card data-title="{esc(title)}" data-search="{esc(article.get('author','') + ' ' + summary)}" data-tags="{esc('|'.join(article.get('topicTags', [])))}" data-date="{esc(article.get('dateISO', ''))}">
      {meta}<h3 dir="auto"><a class="card-title-link" href="{href}">{esc(title)}</a></h3>{translation_notice(mt or ms or md, lang)}
      {f'<p class="card-summary">{esc(summary)}</p>' if summary else ''}{tags}
      <p style="margin-top:1rem"><a href="{href}">{esc(L['read_more'])} →</a></p>
    </article>'''


def webinar_status(webinar: dict, lang: str) -> tuple[str, str]:
    L = LABELS[lang]
    status = webinar.get("recordingStatus", "unknown")
    url = valid_url(webinar.get("recordingUrl"))
    is_youtube = is_youtube_url(url)
    if status == "available" and webinar.get("rightsApproved") is True and is_youtube:
        return f'<a class="button secondary" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(L["recording_available"])}</a>', L["recording_available"]
    if status == "not_recorded":
        return f'<p class="not-configured">{esc(L["not_recorded"])}</p>', L["not_recorded"]
    if status == "restricted":
        return f'<p class="not-configured">{esc(L["restricted"])}</p>', L["restricted"]
    if status == "available" and webinar.get("rightsApproved") is not True:
        return f'<p class="not-configured">{esc(L["permission_pending"])}</p>', L["permission_pending"]
    return f'<p class="not-configured">{esc(L["unknown_recording"])}</p>', L["unknown_recording"]


def webinar_card(webinar: dict, lang: str) -> str:
    L = LABELS[lang]
    title, mt = localized(webinar, "titleEn", "titleFa", lang, "Untitled webinar")
    description, md = localized(webinar, "descriptionEn", "descriptionFa", lang)
    date_label, mdate = localized(webinar, "dateEn", "dateFa", lang)
    status_markup, status_text = webinar_status(webinar, lang)
    href = f'webinar-{esc(webinar.get("slug", ""))}.html'
    tags = tag_links(webinar.get("topicTags", []), lang, "webinars.html")
    return f'''<article class="card" data-filter-card data-title="{esc(title)}" data-search="{esc(webinar.get('speaker','') + ' ' + description)}" data-tags="{esc('|'.join(webinar.get('topicTags', [])))}" data-date="{esc(webinar.get('dateISO', ''))}">
      {card_meta([date_label, webinar.get('speaker')])}<h3 dir="auto"><a class="card-title-link" href="{href}">{esc(title)}</a></h3>{translation_notice(mt or md or mdate, lang)}
      {f'<p class="card-summary">{esc(description)}</p>' if description else ''}{tags}<div style="margin-top:1rem">{status_markup}</div>
    </article>'''


def filter_controls(lang: str, records: list[dict], initial_title="") -> str:
    L = LABELS[lang]
    topics = sorted({str(tag).strip() for r in records for tag in r.get("topicTags", []) if str(tag).strip()}, key=str.casefold)
    options = ''.join(f'<option value="{esc(tag)}">{esc(tag)}</option>' for tag in topics)
    return f'''<div class="filters" data-archive-filters>
      <div class="field"><label for="filter-search">{esc(L['filter_search'])}</label><input id="filter-search" data-filter-search type="search" placeholder="{'e.g. text analysis' if lang == 'en' else 'برای نمونه: تحلیل متن'}" value="{esc(initial_title)}"></div>
      <div class="field"><label for="filter-from">{esc(L['filter_from'])}</label><input id="filter-from" data-filter-from type="date"></div>
      <div class="field"><label for="filter-to">{esc(L['filter_to'])}</label><input id="filter-to" data-filter-to type="date"></div>
      <div class="field"><label for="filter-topic">{esc(L['filter_topic'])}</label><select id="filter-topic" data-filter-topic><option value="">{esc(L['all_topics'])}</option>{options}</select></div>
    </div><p class="card-meta" aria-live="polite" data-filter-count></p>'''


def home_body(lang: str, events, announcements, articles):
    L = LABELS[lang]
    event_future = [e for e in events if e.get("published") and (date_value(e.get("dateISO")) or date.min) >= TODAY_TEHRAN.date()]
    event_future.sort(key=lambda e: str(e.get("dateISO", "9999-12-31")))
    announcements = sorted([a for a in announcements if a.get("published")], key=lambda a: str(a.get("dateISO", "")), reverse=True)[:3]
    articles = sorted([a for a in articles if a.get("published")], key=lambda a: str(a.get("dateISO", "")), reverse=True)[:3]
    hero = f'''<section class="hero"><div class="shell hero-grid"><div>
      <p class="eyebrow">{esc(L['university'])}</p><h1>{esc(L['tagline'])}</h1>
      <p class="lead">{esc(L['about_intro'])}</p><p class="hero-note">{esc(L['department'])}</p>
      <div class="hero-actions"><a class="button" href="events.html">{esc(NAV[lang][3][1])} ↗</a><a class="button secondary" href="certificates.html">{esc(NAV[lang][7][1])}</a></div>
    </div><div class="hero-art"><img src="../assets/images/dh-network.svg" alt="" aria-hidden="true"><div class="hero-index"><strong>DH / 01</strong>{esc(L['association'])}</div></div></div></section>'''
    feature = f'''<div class="shell feature-strip"><div class="feature-block"><span class="feature-kicker">01 / {esc(L['aims'])}</span><h3>{esc(L['about_one_title'])}</h3><p>{esc(L['about_one'])}</p></div><div class="feature-block"><span class="feature-kicker">02 / {esc(L['workflow'])}</span><h3>{esc(L['about_two_title'])}</h3><p>{esc(L['about_two'])}</p></div><div class="feature-block"><span class="feature-kicker">03 / DHC</span><h3>{esc(L['about_three_title'])}</h3><p>{esc(L['about_three'])}</p></div></div>'''
    upcoming_content = ''.join(event_card(e, lang) for e in event_future[:1]) or empty_state(L['no_upcoming_title'], L['no_upcoming'])
    if announcements:
        announcement_content = '<div class="grid-3">' + ''.join(
            f'<article class="card" data-filter-card data-title="{esc(localized(a,"titleEn","titleFa",lang)[0])}" data-tags="" data-date="{esc(a.get("dateISO",""))}">{card_meta([localized(a,"dateEn","dateFa",lang)[0]])}<h3>{esc(localized(a,"titleEn","titleFa",lang)[0])}</h3>{translation_notice(localized(a,"titleEn","titleFa",lang)[1] or localized(a,"bodyEn","bodyFa",lang)[1],lang)}<p class="card-summary">{esc(localized(a,"bodyEn","bodyFa",lang)[0])}</p>{(f'<p><a href="{esc(valid_url(a.get("linkUrl")) or (a.get("linkUrl") if str(a.get("linkUrl","")).startswith(("events.html","articles.html","webinars.html")) else ""))}">{esc(localized(a,"linkLabelEn","linkLabelFa",lang)[0] or L["details"])}</a></p>' if valid_url(a.get("linkUrl")) or str(a.get("linkUrl","")).startswith(("events.html","articles.html","webinars.html")) else '')}</article>'
            for a in announcements) + '</div>'
    else:
        announcement_content = empty_state(L['no_announcements_title'], L['no_announcements'])
    article_content = '<div class="grid-3">' + ''.join(article_card(a, lang) for a in articles) + '</div>' if articles else empty_state(L['no_articles_title'], L['no_articles'])
    return hero + feature + f'''<section class="content-section"><div class="shell"><div class="section-heading"><div><p class="eyebrow">02 / {esc(L['upcoming'])}</p><h2>{esc(L['upcoming'])}</h2><p>{esc(L['date_pair'])}</p></div><a href="events.html">{esc(L['see_all'])} →</a></div><div class="grid-2">{upcoming_content}</div></div></section>
<section class="content-section" style="background:var(--surface-soft)"><div class="shell"><div class="section-heading"><div><p class="eyebrow">03 / {esc(L['announcements'])}</p><h2>{esc(L['announcements'])}</h2></div></div>{announcement_content}</div></section>
<section class="content-section"><div class="shell"><div class="section-heading"><div><p class="eyebrow">04 / {esc(L['latest_articles'])}</p><h2>{esc(L['latest_articles'])}</h2></div><a href="articles.html">{esc(L['see_all'])} →</a></div>{article_content}</div></section>'''


def about_body(lang: str) -> str:
    L = LABELS[lang]
    return page_intro(NAV[lang][1][1], L["about_intro"], lang) + f'''<section class="content-section"><div class="shell grid-3">
    <article class="card"><span class="pill">01</span><h2 style="margin-top:1rem;font-size:1.35rem">{esc(L['about_one_title'])}</h2><p>{esc(L['about_one'])}</p></article>
    <article class="card"><span class="pill">02</span><h2 style="margin-top:1rem;font-size:1.35rem">{esc(L['about_two_title'])}</h2><p>{esc(L['about_two'])}</p></article>
    <article class="card"><span class="pill">03</span><h2 style="margin-top:1rem;font-size:1.35rem">{esc(L['about_three_title'])}</h2><p>{esc(L['about_three'])}</p></article>
  </div></section><section class="content-section" style="background:var(--surface-soft)"><div class="shell prose"><h2>{esc(L['workflow'])}</h2><p>{esc(L['member_consent'])}</p><p>{esc(L['date_pair'])}</p><p>{esc(L['rights_note'])}</p></div></section>'''


def media_href(value) -> str:
    """Convert Pages CMS /media paths into safe, repo-base-compatible relative links."""
    raw = str(value or "").strip().replace("\\", "/")
    for prefix in ("/media/", "media/", "../media/", "./media/"):
        if raw.startswith(prefix):
            remainder = raw[len(prefix):]
            parts = remainder.split("/")
            if remainder and all(part not in ("", ".", "..") for part in parts):
                return "../media/" + "/".join(parts)
    return ""


def members_body(lang: str, members: list[dict]) -> str:
    L = LABELS[lang]
    public = [m for m in members if m.get("consentToPublish") is True]
    current = [m for m in public if m.get("current") is True]
    former = [m for m in public if m.get("current") is not True]
    def cards(entries):
        out = []
        for m in entries:
            bio, missing_bio = localized(m, "bioEn", "bioFa", lang)
            role, missing_role = localized(m, "roleEn", "roleFa", lang, "Member")
            term, missing_term = localized(m, "termEn", "termFa", lang)
            image_url = media_href(m.get("photoUrl")) if m.get("photoConsent") is True else ""
            image_alt, missing_alt = localized(m, "photoAltEn", "photoAltFa", lang, str(m.get("name") or "Member"))
            image_html = f'<img class="member-photo" src="{esc(image_url)}" alt="{esc(image_alt or m.get("name") or "Member")}">' if image_url else ""
            out.append(f'<article class="card">{image_html}<h3 dir="auto">{bdi(m.get("name") or role)}</h3><p class="card-meta">{esc(role)}{(" · " + esc(term)) if term else ""}</p>{translation_notice(missing_bio or missing_role or missing_term or (bool(image_url) and missing_alt),lang)}{fmt_paragraphs(bio)}</article>')
        return ''.join(out) if out else empty_state(L['no_members_title'], L['no_members'])
    current_html = cards(current)
    former_html = cards(former)
    return page_intro(NAV[lang][2][1], L["member_consent"], lang) + f'''<section class="content-section"><div class="shell"><h2>{esc(L['current_members'])}</h2><div class="member-grid">{current_html}</div><hr><h2>{esc(L['former_members'])}</h2><div class="member-grid">{former_html}</div></div></section>'''


def archive_body(lang: str, page_key: str, records: list[dict]) -> str:
    L = LABELS[lang]
    title = NAV[lang][{"events":3,"webinars":4,"articles":5}[page_key]][1]
    lead = {
        "events": L["date_pair"],
        "webinars": L["rights_note"],
        "articles": L["workflow"],
    }[page_key]
    if page_key == "events":
        published = [r for r in records if r.get("published") is True]
        cards = ''.join(event_card(r, lang) for r in sorted(published, key=lambda x: str(x.get("dateISO", "")), reverse=True))
        fallback = empty_state(L['no_events_title'], L['no_events'])
    elif page_key == "webinars":
        published = [r for r in records if r.get("published") is True]
        cards = ''.join(webinar_card(r, lang) for r in sorted(published, key=lambda x: str(x.get("dateISO", "")), reverse=True))
        fallback = empty_state(L['no_webinars_title'], L['no_webinars'])
    else:
        published = [r for r in records if r.get("published") is True]
        cards = ''.join(article_card(r, lang, archive=True) for r in sorted(published, key=lambda x: str(x.get("dateISO", "")), reverse=True))
        fallback = empty_state(L['no_articles_title'], L['no_articles'])
    listing = (filter_controls(lang, published) + f'<div class="grid-3">{cards}<div class="empty-state" data-filter-empty hidden><strong>{esc(L["no_results"])}</strong><p>{esc(L["clear_hint"])}</p></div></div>') if published else fallback
    return page_intro(title, lead, lang) + f'<section class="content-section"><div class="shell">{listing}</div></section>'


def event_detail_body(lang: str, event: dict) -> tuple[str, str]:
    L = LABELS[lang]
    title, mt = localized(event, "titleEn", "titleFa", lang, "Untitled event")
    abstract, ma = localized(event, "abstractEn", "abstractFa", lang)
    date_label, md = localized(event, "dateEn", "dateFa", lang)
    language, ml = localized(event, "languageEn", "languageFa", lang)
    modality = L["online"] if event.get("modality") == "online" else L["in_person"] if event.get("modality") == "in-person" else "—"
    expired = link_is_expired(event)
    paired_date = f'<span class="bidi" lang="en" dir="ltr">{esc(event.get("dateEn") or date_label)}</span><span aria-hidden="true"> · </span><span class="bidi" lang="fa" dir="rtl">{esc(event.get("dateFa") or date_label)}</span>'
    details = [
        (L["date"], paired_date), (L["speaker"], event.get("speaker")), (L["speaker_time"], event.get("speakerTime")),
        (L["timezone"], event.get("speakerTimeZone")), (L["tehran_time"], event.get("tehranTime")),
        (L["language_label"], language), (L["format"], modality), (L["platform"], event.get("platform")),
    ]
    dl = ''.join(f'<dt>{esc(k)}</dt><dd dir="auto">{v if k == L["date"] else esc(v)}</dd>' for k,v in details if v)
    link_html = ''
    if expired:
        expiry_message = L["expired"] if event_has_ended(event) else L["link_expired"]
        link_html = f'<div class="status info">{esc(expiry_message)}</div>'
    else:
        reg = valid_url(event.get("registrationUrl")); attendance = valid_url(event.get("attendanceUrl"))
        if reg: link_html += f'<a class="button secondary" href="{esc(reg)}" target="_blank" rel="noopener noreferrer">{esc(L["register"])}</a>'
        if attendance: link_html += f'<a class="button tertiary" href="{esc(attendance)}" target="_blank" rel="noopener noreferrer">{esc(L["join"])}</a>'
        if not link_html: link_html = f'<p class="not-configured">{esc(L["link_expired"])}</p>'
    tags = tag_links(event.get("topicTags", []), lang, "events.html")
    body = page_intro(title, date_label, lang, L["session_details"]) + f'''<section class="content-section"><div class="shell form-layout"><article class="card prose"><h2>{esc(L['abstract'])}</h2>{fmt_paragraphs(abstract)}{translation_notice(mt or ma or md or ml,lang)}{tags}<div class="hero-actions">{link_html}</div><p><a href="events.html">← {esc(L['back_events'])}</a></p></article><aside class="card"><h2>{esc(L['session_details'])}</h2><dl class="details-list">{dl}</dl></aside></div></section>'''
    return body, title


def webinar_detail_body(lang: str, webinar: dict) -> tuple[str, str]:
    L = LABELS[lang]
    title, mt = localized(webinar, "titleEn", "titleFa", lang, "Untitled webinar")
    description, md = localized(webinar, "descriptionEn", "descriptionFa", lang)
    date_label, mdate = localized(webinar, "dateEn", "dateFa", lang)
    status_markup, _ = webinar_status(webinar, lang)
    tags = tag_links(webinar.get("topicTags", []), lang, "webinars.html")
    body = page_intro(title, date_label, lang, L["session_details"]) + f'''<section class="content-section"><div class="shell prose"><div class="card">{card_meta([date_label, webinar.get('speaker')])}{fmt_paragraphs(description)}{translation_notice(mt or md or mdate,lang)}<h2>{esc(L['status'])}</h2>{status_markup}{tags}<p style="margin-top:1.5rem">{esc(L['rights_note'])}</p><p><a href="webinars.html">← {esc(L['back_webinars'])}</a></p></div></div></section>'''
    return body, title


def article_detail_body(lang: str, article: dict) -> tuple[str, str]:
    L = LABELS[lang]
    title, mt = localized(article, "titleEn", "titleFa", lang, "Untitled article")
    date_label, md = localized(article, "dateEn", "dateFa", lang)
    body_text, mb = localized(article, "bodyEn", "bodyFa", lang)
    summary, ms = localized(article, "summaryEn", "summaryFa", lang)
    author = article.get("author") or ""
    tags = tag_links(article.get("topicTags", []), lang, "articles.html")
    image_url = media_href(article.get("imageUrl"))
    alt, missing_alt = localized(article, "imageAltEn", "imageAltFa", lang)
    image_html = f'<img class="article-image" src="{esc(image_url)}" alt="{esc(alt)}">' if image_url else ''
    body = page_intro(title, summary or date_label, lang, L["article_author"]) + f'''<section class="content-section"><div class="shell"><article class="article-body">{card_meta([date_label, author])}{image_html}{fmt_paragraphs(body_text)}{translation_notice(mt or md or mb or ms or (bool(image_url) and missing_alt),lang)}{tags}<hr><p><a href="articles.html">← {esc(L['back_articles'])}</a></p></article></div></section>'''
    return body, title


def privacy_explanation(lang: str, settings: dict) -> str:
    months = max(1, int(settings.get("contactRetentionMonths") or 12))
    value = LABELS[lang]["privacy_explain"]
    if lang == "en":
        return value.replace("12 months", f"{months} months")
    persian_digits = str(months).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))
    return value.replace("۱۲ ماه", f"{persian_digits} ماه")


def contact_body(lang: str, settings: dict) -> str:
    L = LABELS[lang]
    privacy_text = privacy_explanation(lang, settings)
    head = settings.get("head", {})
    supervisor = settings.get("supervisor", {})
    contacts = []
    for person, heading_key, fallback_role_en, fallback_role_fa in [
        (head, "contact_head", "Current association head", "مسئول فعلی انجمن"),
        (supervisor, "contact_supervisor", "Faculty supervisor", "استاد ناظر انجمن"),
    ]:
        role = str(person.get("roleFa" if lang == "fa" else "roleEn") or (fallback_role_fa if lang == "fa" else fallback_role_en))
        name = str(person.get("name") or "").strip()
        mail = valid_mail(person.get("email"))
        detail = (f'<strong><bdi dir="auto">{esc(name)}</bdi></strong><br>' if name else '') + (f'<a href="mailto:{esc(mail)}" dir="ltr"><bdi dir="ltr">{esc(mail)}</bdi></a>' if mail else f'<span class="not-configured">{esc(L["not_configured"])}</span>')
        contacts.append(f'<article class="card"><h3>{esc(role)}</h3><p>{detail}</p></article>')
    social = settings.get("social", {})
    social_names = [("telegram", "Telegram"), ("instagram", "Instagram"), ("linkedin", "LinkedIn"), ("other", "Other official channel")]
    social_html = []
    for key, label in social_names:
        url = valid_url(social.get(key))
        social_html.append(f'<li><a href="{esc(url)}" target="_blank" rel="noopener noreferrer" lang="en" dir="ltr">{esc(label)}</a></li>' if url else f'<li><span>{esc(label)} — <span class="not-configured">{esc(L["not_configured"])}</span></span></li>')
    form = f'''<form class="card form-stack" method="post" target="contact-result-frame" data-contact-form data-endpoint="{esc(settings.get('appsScriptWebAppUrl',''))}" action="">
      <input type="hidden" name="requestId" value=""><input type="hidden" name="startedAt" value="">
      <div class="field"><label for="contact-name">{esc(L['name'])}</label><input id="contact-name" name="name" type="text" autocomplete="name" maxlength="100" required></div>
      <div class="field"><label for="contact-email">{esc(L['email'])}</label><input id="contact-email" name="email" type="email" autocomplete="email" maxlength="200" required></div>
      <div class="field"><label for="contact-topic">{esc(L['subject'])}</label><input id="contact-topic" name="topic" type="text" maxlength="160" required></div>
      <div class="field"><label for="contact-message">{esc(L['message'])}</label><textarea id="contact-message" name="message" maxlength="5000" required aria-describedby="message-hint"></textarea><span id="message-hint" class="hint">{'Maximum 5,000 characters.' if lang == 'en' else 'حداکثر ۵۰۰۰ نویسه.'}</span></div>
      <div class="field" style="position:absolute;inset-inline-start:-10000px;width:1px;height:1px;overflow:hidden" aria-hidden="true"><label for="contact-website">Website</label><input id="contact-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
      <label class="consent-row"><input type="checkbox" name="privacyAcknowledged" value="yes" required><span>{esc(L['privacy_consent'])}</span></label>
      <button class="button" type="submit">{esc(L['send'])}</button><p data-contact-status class="status info" role="status" aria-live="polite" hidden></p>
    </form><iframe name="contact-result-frame" title="Contact form submission response" class="visually-hidden"></iframe>'''
    return page_intro(NAV[lang][6][1], L["contact_alternative"], lang) + f'''<section class="content-section"><div class="shell"><div class="grid-2">{''.join(contacts)}</div><div class="form-layout" style="margin-top:1.5rem"><div><h2>{esc(L['message_form'])}</h2><p class="card-summary">{esc(privacy_text)}</p>{form}</div><aside class="card"><h2>{esc(L['footer_contact'])}</h2><ul class="footer-links">{''.join(social_html)}</ul><hr><p>{esc(L['university'])}<br>{esc(L['department'])}</p></aside></div></div></section>'''


def certificates_body(lang: str, settings: dict) -> str:
    L = LABELS[lang]
    pattern = str(settings.get("certificateNumberPattern") or "^[A-Z0-9-]{4,24}$")
    note = str(settings.get("certificatePatternNoteFa" if lang == "fa" else "certificatePatternNoteEn") or L["certificate_format"])
    return page_intro(L["certificate_heading"], L["certificate_note"], lang) + f'''<section class="content-section"><div class="shell form-layout"><div class="card"><form class="form-stack" data-certificate-form data-registry-url="../data/certificates.json" data-pattern="{esc(pattern)}">
      <div class="field"><label for="certificate-number">{esc(L['certificate_heading'])}</label><input id="certificate-number" name="certificate-number" type="text" class="mono" autocomplete="off" autocapitalize="characters" spellcheck="false" maxlength="64" required aria-describedby="certificate-pattern-note"></div>
      <button class="button" type="submit">{esc(L['certificate_submit'])}</button>
    </form><div class="status info" id="certificate-pattern-note"><strong>{esc(L['certificate_format'])}</strong><p>{esc(note)}</p><p class="mono formula">{esc(pattern)}</p></div><div data-certificate-result class="status info" role="status" aria-live="polite" hidden></div></div>
    <aside class="prose"><h2>{esc(L['certificate_heading'])}</h2><p>{esc(L['certificate_note'])}</p><p>{esc(L['rights_note'])}</p><p>{esc(L['privacy_body'])}</p></aside></div></section>'''


def privacy_body(lang: str) -> str:
    L = LABELS[lang]
    privacy_text = privacy_explanation(lang, SETTINGS)
    return page_intro(L["privacy_title"], L["privacy_body"], lang) + f'''<section class="content-section"><div class="shell prose"><h2>{esc(L['message_form'])}</h2><p>{esc(privacy_text)}</p><h2>{esc(L['current_members'])}</h2><p>{esc(L['member_consent'])}</p><h2>{esc(L['certificate_heading'])}</h2><p>{esc(L['privacy_body'])}</p></div></section>'''


def root_index():
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="x-ua-compatible" content="ie=edge"><title>DHC · Digital Humanities Center and Student Association · Shiraz University</title><meta name="description" content="Digital Humanities Center (DHC) and its student association at Shiraz University. English and Persian website."><meta name="color-scheme" content="light dark"><link rel="icon" href="assets/images/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/css/site.css"><script>(function(){var saved='';try{saved=localStorage.getItem('dhc-language')||''}catch(e){}var lang=saved||((navigator.language||'').toLowerCase().startsWith('fa')?'fa':'en');if(lang==='fa'||lang==='en'){window.location.replace(lang+'/index.html')}})();</script></head><body><main id="main" class="shell" style="padding-block:12vh"><p class="eyebrow">Shiraz University</p><h1>Digital Humanities Center (DHC)</h1><p class="lead">Student Association · Faculty of Humanities and Letters</p><div class="hero-actions"><a class="button" href="en/index.html" lang="en">English</a><a class="button secondary" href="fa/index.html" lang="fa" dir="rtl">فارسی</a></div><p style="margin-top:2rem;color:var(--muted)" lang="fa" dir="rtl">دانشگاه شیراز · مرکز علوم انسانی دیجیتال (DHC) و انجمن دانشجویی آن</p></main><script>document.querySelectorAll('a[href^="en/"],a[href^="fa/"]').forEach(function(a){a.addEventListener('click',function(){try{localStorage.setItem('dhc-language',a.href.includes('/fa/')?'fa':'en')}catch(e){}})});</script></body></html>'''


def main():
    global SETTINGS
    SETTINGS = load_json("site-settings.json")
    events = load_json("events.json") or []
    webinars = load_json("webinars.json") or []
    articles = load_json("articles.json") or []
    members = load_json("members.json") or []
    announcements = load_json("announcements.json") or []
    certificates = load_json("certificates.json") or []

    for group, entries in (("events", events), ("webinars", webinars), ("articles", articles)):
        slugs = [str(entry.get("slug", "")) for entry in entries]
        if len(slugs) != len(set(slugs)):
            raise SystemExit(f"Duplicate slug in content/{group}.json")
        for entry in entries:
            if entry.get("published") is True:
                if not entry.get("titleEn") and not entry.get("titleFa"):
                    raise SystemExit(f"Published {group} item is missing a title: {entry!r}")
                if not re.fullmatch(r"[a-z0-9-]+", str(entry.get("slug", ""))):
                    raise SystemExit(f"Published {group} item has an invalid slug: {entry.get('slug')!r}")
                if not entry.get("dateISO") or not entry.get("dateEn") or not entry.get("dateFa"):
                    raise SystemExit(f"Published {group} item needs an ISO date and both English/Persian display dates: {entry.get('slug')}")
                try:
                    date.fromisoformat(str(entry.get("dateISO"))[:10])
                except ValueError:
                    raise SystemExit(f"Published {group} item has an invalid ISO date: {entry.get('slug')}")
                if group == "events":
                    required = ("speaker", "speakerTimeZone", "speakerTime", "tehranTime", "languageEn", "languageFa", "modality", "platform")
                    missing = [field for field in required if not str(entry.get(field) or "").strip()]
                    if missing:
                        raise SystemExit(f"Published event {entry.get('slug')} is missing required fields: {', '.join(missing)}")
                    if entry.get("modality") not in ("online", "in-person"):
                        raise SystemExit(f"Published event {entry.get('slug')} must set modality to online or in-person.")
                    if not (entry.get("abstractEn") or entry.get("abstractFa")):
                        raise SystemExit(f"Published event {entry.get('slug')} needs an abstract in at least one language.")
                    try:
                        ZoneInfo(str(entry.get("speakerTimeZone")))
                    except Exception:
                        raise SystemExit(f"Published event {entry.get('slug')} has an invalid IANA timezone.")
                    if entry.get("linkExpiresAt"):
                        try:
                            datetime.fromisoformat(str(entry["linkExpiresAt"]).replace("Z", "+00:00"))
                        except ValueError:
                            raise SystemExit(f"Event {entry.get('slug')} has an invalid linkExpiresAt ISO timestamp.")
                    for url_field in ("registrationUrl", "attendanceUrl"):
                        url_value = str(entry.get(url_field) or "").strip()
                        if url_value and not valid_url(url_value):
                            raise SystemExit(f"Published event {entry.get('slug')} has a non-HTTPS or invalid {url_field}.")
                if group == "webinars":
                    if not entry.get("speaker") or not (entry.get("descriptionEn") or entry.get("descriptionFa")):
                        raise SystemExit(f"Published webinar {entry.get('slug')} needs a speaker and a description in at least one language.")
                    if entry.get("recordingStatus") not in ("available", "not_recorded", "restricted", "unknown"):
                        raise SystemExit(f"Published webinar {entry.get('slug')} needs an explicit recordingStatus.")
                    if entry.get("recordingStatus") == "available" and entry.get("rightsApproved") is True:
                        recording_url = valid_url(entry.get("recordingUrl"))
                        if not recording_url or not is_youtube_url(recording_url):
                            raise SystemExit(f"Webinar {entry.get('slug')} needs an approved HTTPS YouTube URL before it can be marked as shareable.")
                if group == "articles":
                    if not (entry.get("bodyEn") or entry.get("bodyFa")):
                        raise SystemExit(f"Published article {entry.get('slug')} needs body text in at least one language.")
                    if entry.get("imageUrl") and not (entry.get("imageAltEn") or entry.get("imageAltFa")):
                        raise SystemExit(f"Published article {entry.get('slug')} has an image but no alternative text.")
    cert_numbers = [str(c.get("number", "")).strip().upper() for c in certificates]
    if len(cert_numbers) != len(set(cert_numbers)):
        raise SystemExit("Duplicate certificate number in content/certificates.json")
    allowed_certificate_fields = {"number", "holderNameEn", "holderNameFa", "issueDateEn", "issueDateFa", "descriptionEn", "descriptionFa"}
    try:
        certificate_pattern = re.compile(str(SETTINGS.get("certificateNumberPattern") or "^[A-Z0-9-]{4,24}$"))
    except re.error as error:
        raise SystemExit(f"Invalid certificateNumberPattern in content/site-settings.json: {error}")
    for c in certificates:
        extras = set(c.keys()) - allowed_certificate_fields
        if extras:
            raise SystemExit(f"Certificate record has unsupported fields {sorted(extras)}; only public verification fields are allowed.")
        missing = [field for field in allowed_certificate_fields if not str(c.get(field) or "").strip()]
        if missing:
            raise SystemExit(f"Certificate record is missing required public fields: {', '.join(sorted(missing))}")
        if not certificate_pattern.fullmatch(str(c.get("number") or "").strip().upper()):
            raise SystemExit(f"Certificate number {c.get('number')!r} does not match certificateNumberPattern in site settings.")

    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copytree(ROOT / "assets", DIST / "assets")
    media_dir = CONTENT / "media"
    if media_dir.exists():
        shutil.copytree(media_dir, DIST / "media", dirs_exist_ok=True, ignore=shutil.ignore_patterns(".gitkeep"))
    (DIST / "data").mkdir()
    # This public JSON contains only the precise fields the verification page displays.
    (DIST / "data" / "certificates.json").write_text(json.dumps(certificates, ensure_ascii=False, indent=2), encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    (DIST / "index.html").write_text(root_index(), encoding="utf-8")

    for lang in ("en", "fa"):
        folder = DIST / lang
        folder.mkdir()
        page_data = [
            ("index.html", "home", LABELS[lang]["association"], LABELS[lang]["about_intro"], home_body(lang, events, announcements, articles)),
            ("about.html", "about", NAV[lang][1][1], LABELS[lang]["about_intro"], about_body(lang)),
            ("members.html", "members", NAV[lang][2][1], LABELS[lang]["member_consent"], members_body(lang, members)),
            ("events.html", "events", NAV[lang][3][1], LABELS[lang]["date_pair"], archive_body(lang, "events", events)),
            ("webinars.html", "webinars", NAV[lang][4][1], LABELS[lang]["rights_note"], archive_body(lang, "webinars", webinars)),
            ("articles.html", "articles", NAV[lang][5][1], LABELS[lang]["workflow"], archive_body(lang, "articles", articles)),
            ("contact.html", "contact", NAV[lang][6][1], LABELS[lang]["contact_alternative"], contact_body(lang, SETTINGS)),
            ("certificates.html", "certificates", NAV[lang][7][1], LABELS[lang]["certificate_note"], certificates_body(lang, SETTINGS)),
            ("privacy.html", "privacy", LABELS[lang]["privacy_title"], LABELS[lang]["privacy_body"], privacy_body(lang)),
        ]
        for filename, page_key, title, desc, body in page_data:
            (folder / filename).write_text(page_html(lang, filename, page_key, title, desc, body), encoding="utf-8")
        for event in events:
            if event.get("published") is not True: continue
            body, title = event_detail_body(lang, event)
            filename = f'event-{event["slug"]}.html'
            (folder / filename).write_text(page_html(lang, filename, "events", title, str(event.get("abstractEn") or event.get("abstractFa") or title), body), encoding="utf-8")
        for webinar in webinars:
            if webinar.get("published") is not True: continue
            body, title = webinar_detail_body(lang, webinar)
            filename = f'webinar-{webinar["slug"]}.html'
            (folder / filename).write_text(page_html(lang, filename, "webinars", title, str(webinar.get("descriptionEn") or webinar.get("descriptionFa") or title), body), encoding="utf-8")
        for article in articles:
            if article.get("published") is not True: continue
            body, title = article_detail_body(lang, article)
            filename = f'article-{article["slug"]}.html'
            (folder / filename).write_text(page_html(lang, filename, "articles", title, str(article.get("summaryEn") or article.get("summaryFa") or title), body), encoding="utf-8")
        not_found = page_intro(LABELS[lang]["error_title"], LABELS[lang]["error_body"], lang) + f'<section class="content-section"><div class="shell"><a class="button" href="index.html">{esc(NAV[lang][0][1])}</a></div></section>'
        (folder / "404.html").write_text(page_html(lang, "404.html", "", LABELS[lang]["error_title"], LABELS[lang]["error_body"], not_found), encoding="utf-8")

    # Root-level 404 has root-relative-to-project assets and language choices.
    root_404 = f"""<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>Page not found · Digital Humanities Center (DHC)</title><link rel=\"stylesheet\" href=\"assets/css/site.css\"></head><body><main class=\"shell\" style=\"padding-block:12vh\"><p class=\"eyebrow\">404</p><h1>Page not found</h1><p class=\"lead\">This address may be outdated or the page may have moved.</p><div class=\"hero-actions\"><a class=\"button\" href=\"en/index.html\">English home</a><a class=\"button secondary\" href=\"fa/index.html\" lang=\"fa\" dir=\"rtl\">صفحهٔ اصلی فارسی</a></div></main></body></html>"""
    (DIST / "404.html").write_text(root_404, encoding="utf-8")
    base = str(SETTINGS.get("publicBaseUrl") or "").rstrip("/")
    if base:
        paths = ["/", "/en/index.html", "/en/about.html", "/en/members.html", "/en/events.html", "/en/webinars.html", "/en/articles.html", "/en/contact.html", "/en/certificates.html", "/en/privacy.html", "/fa/index.html", "/fa/about.html", "/fa/members.html", "/fa/events.html", "/fa/webinars.html", "/fa/articles.html", "/fa/contact.html", "/fa/certificates.html", "/fa/privacy.html"]
        for lang in ("en", "fa"):
            paths.extend(f'/{lang}/event-{e["slug"]}.html' for e in events if e.get("published") is True)
            paths.extend(f'/{lang}/webinar-{w["slug"]}.html' for w in webinars if w.get("published") is True)
            paths.extend(f'/{lang}/article-{a["slug"]}.html' for a in articles if a.get("published") is True)
        (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{esc(base+p)}</loc></url>' for p in paths) + '</urlset>', encoding="utf-8")
    (DIST / "robots.txt").write_text("User-agent: *\nAllow: /\n" + (f"Sitemap: {base}/sitemap.xml\n" if base else "# Set publicBaseUrl in content/site-settings.json to enable a sitemap.\n"), encoding="utf-8")
    print(f"Built {len(list(DIST.rglob('*.html')))} HTML pages into {DIST}")
    print(f"Published content counts — events: {sum(bool(x.get('published')) for x in events)}, webinars: {sum(bool(x.get('published')) for x in webinars)}, articles: {sum(bool(x.get('published')) for x in articles)}, public consented member profiles: {sum(x.get('consentToPublish') is True for x in members)}, certificates: {len(certificates)}")

if __name__ == "__main__":
    main()
