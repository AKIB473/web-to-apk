/**
 * TitanChart — Contact Form
 *
 * Sends form data to a Telegram chat via the Bot API.
 *
 * ⚠️  NEVER hardcode bot tokens in source code.
 *     Use environment variables injected at build time (see README).
 *
 * During local dev: copy .env.example → .env and fill in values.
 * In production CI: set VITE_BOT_TOKEN and VITE_CHAT_ID as GitHub Secrets.
 */

// ── Config (injected by Vite/build tool from env vars) ────────────────────────
// Fallback empty strings are safe — the form will show an error if not configured.
const BOT_TOKEN = typeof __BOT_TOKEN__ !== 'undefined' ? __BOT_TOKEN__ : '';
const CHAT_ID   = typeof __CHAT_ID__   !== 'undefined' ? __CHAT_ID__   : '';

const MAX_CHARS = 1000;

// ── DOM refs ──────────────────────────────────────────────────────────────────
const form          = document.getElementById('contact-form');
const submitBtn     = document.getElementById('submit-btn');
const btnText       = submitBtn.querySelector('.btn-text');
const btnSpinner    = submitBtn.querySelector('.btn-spinner');
const charCount     = document.getElementById('char-count');
const statusSuccess = document.getElementById('status-success');
const statusError   = document.getElementById('status-error');
const errorDetail   = document.getElementById('error-detail');
const msgTextarea   = document.getElementById('message');

// ── Character counter ─────────────────────────────────────────────────────────
msgTextarea.addEventListener('input', () => {
  const len = msgTextarea.value.length;
  charCount.textContent = `${len} / ${MAX_CHARS}`;
  charCount.className = 'char-count';
  if (len > MAX_CHARS * 0.85) charCount.classList.add('near-limit');
  if (len >= MAX_CHARS)       charCount.classList.add('at-limit');
  if (len >= MAX_CHARS) msgTextarea.value = msgTextarea.value.slice(0, MAX_CHARS);
});

// ── Validation ────────────────────────────────────────────────────────────────
function validateField(id, errorId, check, msg) {
  const el  = document.getElementById(id);
  const err = document.getElementById(errorId);
  if (!check(el.value.trim())) {
    el.classList.add('invalid');
    err.textContent = msg;
    return false;
  }
  el.classList.remove('invalid');
  err.textContent = '';
  return true;
}

function validateForm() {
  const okName  = validateField('name',    'name-error',    v => v.length >= 2,            'Name must be at least 2 characters.');
  const okEmail = validateField('email',   'email-error',   v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v), 'Please enter a valid email address.');
  const okMsg   = validateField('message', 'message-error', v => v.length >= 10,           'Message must be at least 10 characters.');
  return okName && okEmail && okMsg;
}

// Clear invalid state on input
['name', 'email', 'message'].forEach(id => {
  document.getElementById(id).addEventListener('input', () => {
    document.getElementById(id).classList.remove('invalid');
    const errEl = document.getElementById(`${id}-error`);
    if (errEl) errEl.textContent = '';
  });
});

// ── UI helpers ────────────────────────────────────────────────────────────────
function setLoading(on) {
  submitBtn.disabled = on;
  btnText.hidden     = on;
  btnSpinner.hidden  = !on;
}

function showStatus(type, detail) {
  statusSuccess.hidden = true;
  statusError.hidden   = true;
  if (type === 'success') {
    statusSuccess.hidden = false;
    statusSuccess.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } else {
    if (detail) errorDetail.textContent = detail;
    statusError.hidden = false;
    statusError.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

// ── Build Telegram message ────────────────────────────────────────────────────
function buildMessage({ name, email, subject, message }) {
  const timestamp = new Date().toLocaleString('en-GB', { timeZone: 'UTC' });
  return [
    '📬 <b>New Contact Form Submission</b>',
    '',
    `👤 <b>Name:</b> ${escapeHtml(name)}`,
    `📧 <b>Email:</b> ${escapeHtml(email)}`,
    subject ? `📌 <b>Subject:</b> ${escapeHtml(subject)}` : null,
    '',
    `💬 <b>Message:</b>`,
    escapeHtml(message),
    '',
    `🕐 <i>${timestamp} UTC</i>`,
    `🔗 <i>via TitanChart Contact Form</i>`,
  ].filter(line => line !== null).join('\n');
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

// ── Send to Telegram ──────────────────────────────────────────────────────────
async function sendToTelegram(text) {
  if (!BOT_TOKEN || !CHAT_ID) {
    throw new Error('Bot token or chat ID not configured. See .env.example.');
  }

  const res = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: CHAT_ID, text, parse_mode: 'HTML' }),
  });

  const data = await res.json();
  if (!data.ok) throw new Error(data.description || 'Telegram API error');
  return data;
}

// ── Form submit ───────────────────────────────────────────────────────────────
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  statusSuccess.hidden = true;
  statusError.hidden   = true;

  if (!validateForm()) return;

  const payload = {
    name:    document.getElementById('name').value.trim(),
    email:   document.getElementById('email').value.trim(),
    subject: document.getElementById('subject').value.trim(),
    message: document.getElementById('message').value.trim(),
  };

  setLoading(true);

  try {
    await sendToTelegram(buildMessage(payload));
    showStatus('success');
    form.reset();
    charCount.textContent = `0 / ${MAX_CHARS}`;
  } catch (err) {
    console.error('[TitanChart]', err);
    showStatus('error', err.message);
  } finally {
    setLoading(false);
  }
});
