(() => {
  'use strict';

  const root = document.documentElement;
  const themeButton = document.querySelector('[data-theme-toggle]');
  const navButton = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-main-nav]');

  function applyTheme(theme) {
    root.dataset.theme = theme;
    if (themeButton) {
      const next = theme === 'dark' ? (root.lang === 'fa' ? 'روشن' : 'Light') : (root.lang === 'fa' ? 'تیره' : 'Dark');
      themeButton.setAttribute('aria-label', root.lang === 'fa' ? `تغییر پوسته؛ حالت بعدی ${next}` : `Change theme; next mode ${next}`);
      themeButton.setAttribute('aria-pressed', String(theme === 'dark'));
      const label = themeButton.querySelector('[data-theme-label]');
      if (label) label.textContent = next;
    }
  }
  if (themeButton) {
    let saved = null;
    try { saved = localStorage.getItem('dhc-theme'); } catch (_) { /* Storage can be disabled. */ }
    const systemDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(saved || (systemDark ? 'dark' : 'light'));
    themeButton.addEventListener('click', () => {
      const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      try { localStorage.setItem('dhc-theme', next); } catch (_) { /* Current session still works. */ }
    });
  }
  if (navButton && nav) {
    const compactNav = window.matchMedia('(max-width: 1080px)');
    const syncNavForViewport = () => {
      if (compactNav.matches) {
        nav.hidden = true;
        navButton.setAttribute('aria-expanded', 'false');
      } else {
        nav.hidden = false;
        navButton.setAttribute('aria-expanded', 'true');
      }
    };
    syncNavForViewport();
    if (compactNav.addEventListener) compactNav.addEventListener('change', syncNavForViewport);
    navButton.addEventListener('click', () => {
      const opening = nav.hidden;
      nav.hidden = !opening;
      navButton.setAttribute('aria-expanded', String(opening));
    });
  }
  document.querySelectorAll('a.language-link').forEach(link => {
    link.addEventListener('click', () => {
      const nextLanguage = link.getAttribute('hreflang');
      if (nextLanguage === 'en' || nextLanguage === 'fa') {
        try { localStorage.setItem('dhc-language', nextLanguage); } catch (_) { /* Language links still work. */ }
      }
    });
  });

  // Search and filter static archive cards; the page remains usable without JavaScript.
  const filterRoot = document.querySelector('[data-archive-filters]');
  if (filterRoot) {
    const search = filterRoot.querySelector('[data-filter-search]');
    const from = filterRoot.querySelector('[data-filter-from]');
    const to = filterRoot.querySelector('[data-filter-to]');
    const topic = filterRoot.querySelector('[data-filter-topic]');
    const cards = Array.from(document.querySelectorAll('[data-filter-card]'));
    const empty = document.querySelector('[data-filter-empty]');
    const count = document.querySelector('[data-filter-count]');
    const params = new URLSearchParams(window.location.search);
    const selectedTag = (params.get('tag') || '').trim().toLocaleLowerCase();
    if (topic && selectedTag) {
      const option = Array.from(topic.options).find(o => o.value.toLocaleLowerCase() === selectedTag);
      if (option) topic.value = option.value;
    }
    if (selectedTag && search) search.value = '';

    const filter = () => {
      const q = (search?.value || '').trim().toLocaleLowerCase();
      const dateFrom = from?.value || '';
      const dateTo = to?.value || '';
      const tag = (topic?.value || '').trim().toLocaleLowerCase();
      let shown = 0;
      cards.forEach(card => {
        const title = (card.dataset.title || '').toLocaleLowerCase();
        const tags = (card.dataset.tags || '').split('|').map(s => s.trim().toLocaleLowerCase()).filter(Boolean);
        const date = card.dataset.date || '';
        const matches = (!q || title.includes(q) || (card.dataset.search || '').toLocaleLowerCase().includes(q))
          && (!dateFrom || (date && date >= dateFrom))
          && (!dateTo || (date && date <= dateTo))
          && (!tag || tags.includes(tag));
        card.hidden = !matches;
        if (matches) shown += 1;
      });
      if (empty) empty.hidden = shown !== 0;
      if (count) count.textContent = root.lang === 'fa' ? `${shown} مورد` : `${shown} result${shown === 1 ? '' : 's'}`;
    };
    [search, from, to, topic].filter(Boolean).forEach(el => el.addEventListener(el.tagName === 'INPUT' ? 'input' : 'change', filter));
    filter();
  }

  // Certificate verification: static hosting only exposes the approved public fields in this registry.
  const certificateForm = document.querySelector('[data-certificate-form]');
  if (certificateForm) {
    const numberField = certificateForm.querySelector('[name="certificate-number"]');
    const result = document.querySelector('[data-certificate-result]');
    const submit = certificateForm.querySelector('button[type="submit"]');
    const isFa = root.lang === 'fa';
    const text = isFa ? {
      checking: 'در حال بررسی شماره گواهی…', valid: 'گواهی معتبر است', invalid: 'گواهی معتبری با این شماره پیدا نشد.', emptyRegistry: 'اعتبارسنجی هنوز فعال نیست؛ هنوز هیچ رکورد گواهی منتشر نشده است.',
      format: 'شماره با الگوی فعلی مطابقت ندارد. الگوی فعلی موقت است؛ شماره را بررسی کنید.', error: 'بررسی گواهی در حال حاضر ممکن نیست. لطفاً بعداً دوباره تلاش کنید یا با انجمن تماس بگیرید.',
      holder: 'نام دارنده', issue: 'تاریخ صدور', description: 'عنوان گواهی', number: 'شماره گواهی'
    } : {
      checking: 'Checking certificate number…', valid: 'Certificate verified', invalid: 'No valid certificate was found for that number.', emptyRegistry: 'Certificate verification is not ready because no certificate records have been published yet.',
      format: 'The number does not match the current pattern. This pattern is a placeholder; check the number.', error: 'Certificate verification is temporarily unavailable. Please try again later or contact the association.',
      holder: 'Certificate holder', issue: 'Issue date', description: 'Certificate type', number: 'Certificate number'
    };
    const endpoint = certificateForm.dataset.registryUrl;
    const patternSource = certificateForm.dataset.pattern || '^[A-Z0-9-]{4,24}$';
    let registryPromise;
    function show(message, state = 'info', details = '') {
      result.className = `status ${state}`;
      result.replaceChildren();
      const strong = document.createElement('strong');
      strong.textContent = message;
      result.appendChild(strong);
      if (details) {
        const p = document.createElement('p');
        p.textContent = details;
        p.style.margin = '.4rem 0 0';
        result.appendChild(p);
      }
      result.hidden = false;
    }
    certificateForm.addEventListener('submit', async event => {
      event.preventDefault();
      const number = (numberField.value || '').trim().toLocaleUpperCase();
      let pattern;
      try { pattern = new RegExp(patternSource); } catch (_) { show(text.error, 'error'); return; }
      if (!pattern.test(number)) { show(text.format, 'error'); return; }
      show(text.checking, 'info');
      submit.disabled = true;
      try {
        registryPromise ||= fetch(endpoint, { cache: 'no-store' }).then(response => {
          if (!response.ok) throw new Error('registry unavailable');
          return response.json();
        });
        const records = await registryPromise;
        if (!Array.isArray(records)) throw new Error('invalid registry');
        if (records.length === 0) { show(text.emptyRegistry, 'info'); return; }
        const record = records.find(item => String(item.number || '').trim().toLocaleUpperCase() === number);
        if (!record) { show(text.invalid, 'error'); return; }
        const fields = [
          [text.number, record.number],
          [text.holder, isFa ? record.holderNameFa : record.holderNameEn],
          [text.issue, isFa ? record.issueDateFa : record.issueDateEn],
          [text.description, isFa ? record.descriptionFa : record.descriptionEn]
        ];
        result.className = 'status success';
        result.replaceChildren();
        const heading = document.createElement('strong');
        heading.textContent = text.valid;
        result.appendChild(heading);
        const dl = document.createElement('dl');
        dl.className = 'details-list';
        fields.forEach(([label, value]) => {
          const dt = document.createElement('dt'); dt.textContent = label;
          const dd = document.createElement('dd'); dd.textContent = String(value || '—');
          dl.append(dt, dd);
        });
        result.appendChild(dl);
      } catch (_) {
        registryPromise = null;
        show(text.error, 'error');
      } finally {
        submit.disabled = false;
      }
    });
  }

  // Apps Script receives the form in a hidden frame, then posts a minimal result message back.
  const contactForm = document.querySelector('[data-contact-form]');
  if (contactForm) {
    const isFa = root.lang === 'fa';
    const status = document.querySelector('[data-contact-status]');
    const submit = contactForm.querySelector('button[type="submit"]');
    const endpoint = (contactForm.dataset.endpoint || '').trim();
    const sendCopy = isFa ? 'در حال ارسال پیام…' : 'Submitting message…';
    let pendingId = '';
    let timeoutHandle = null;
    const showStatus = (message, kind) => {
      status.textContent = message;
      status.className = `status ${kind}`;
      status.hidden = false;
    };
    if (!endpoint) {
      submit.disabled = true;
      showStatus(isFa ? 'فرم هنوز به حساب Google انجمن متصل نشده است. تا زمان راه‌اندازی، از اطلاعات تماس رسمیِ درج‌شده در همین صفحه استفاده کنید.' : 'This form has not been connected to the association’s Google account yet. Until setup is complete, use the official contact details listed on this page.', 'info');
    } else {
      contactForm.action = endpoint;
      contactForm.addEventListener('submit', () => {
        pendingId = (contactForm.querySelector('[name="requestId"]').value = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(36).slice(2)}`);
        contactForm.querySelector('[name="startedAt"]').value = String(Date.now());
        submit.disabled = true;
        showStatus(sendCopy, 'info');
        if (timeoutHandle) clearTimeout(timeoutHandle);
        timeoutHandle = window.setTimeout(() => {
          if (pendingId) {
            showStatus(isFa ? 'پاسخی از سرویس دریافت نشد. وضعیت پیام مشخص نیست؛ لطفاً از راه دیگری با انجمن تماس بگیرید.' : 'No response was received from the service. The submission status is unknown; please contact the association another way.', 'error');
            submit.disabled = false;
            pendingId = '';
          }
        }, 30000);
      });
      window.addEventListener('message', event => {
        const data = event.data;
        if (!data || data.source !== 'dhc-contact-form' || !pendingId || data.requestId !== pendingId) return;
        clearTimeout(timeoutHandle);
        pendingId = '';
        submit.disabled = false;
        if (data.success) {
          contactForm.reset();
          showStatus(isFa ? 'پیام شما ثبت شد. این نشانی فقط برای پاسخ‌گویی به پیام استفاده می‌شود.' : 'Your message has been submitted. Your details will be used only to respond to this message.', 'success');
        } else {
          showStatus(isFa ? 'ارسال پیام انجام نشد. لطفاً دوباره تلاش کنید یا از روش دیگری با انجمن تماس بگیرید.' : 'The message could not be submitted. Please try again or contact the association another way.', 'error');
        }
      });
    }
  }
})();
