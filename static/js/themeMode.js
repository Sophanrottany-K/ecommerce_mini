
// theme.js

// ===== Config =====
const BREAKPOINT_LG_MIN = '(min-width: 992px)';

// ===== Media queries =====
const mqLgUp = window.matchMedia(BREAKPOINT_LG_MIN);
const mqSysDark = window.matchMedia('(prefers-color-scheme: dark)');

// ===== Helpers =====
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
const htmlEl = document.documentElement;

function getSavedTheme() {
  try { return localStorage.getItem('theme'); } catch { return null; }
}

function setSavedTheme(modeOrNull) {
  try {
    if (modeOrNull) localStorage.setItem('theme', modeOrNull);
    else localStorage.removeItem('theme');
  } catch { /* ignore */ }
}

// Compute current theme according to policy
function computeAutoTheme() {
  // POLICY: lg+ uses system; below lg = dark
  if (mqLgUp.matches) {
    return mqSysDark.matches ? 'dark' : 'light';
  } else {
    return 'dark';
  }
}

function resolveTheme() {
  const saved = getSavedTheme(); // 'dark' | 'light' | null
  return saved || computeAutoTheme();
}

function applyTheme(theme) {
  htmlEl.setAttribute('data-theme', theme);
  updateAllButtons(theme);
}

function iconFor(theme) {
  return theme === "dark"
    ? '<i class="bi bi-sun"></i>'
    : '<i class="bi bi-moon"></i>';
}

function updateButton(el, theme) {
  const isDark = theme === 'dark';
  const newCta = isDark ? 'Change to light theme' : 'Change to dark theme';
  el.setAttribute('aria-label', newCta);
  el.innerHTML = iconFor(theme);
}

function updateAllButtons(theme) {
  $$('[data-theme-toggle]').forEach(btn => updateButton(btn, theme));
}

// ===== Init =====
let currentTheme = resolveTheme();
applyTheme(currentTheme);

// React to viewport/system changes ONLY if no saved preference
function maybeAutoUpdate() {
  if (!getSavedTheme()) {
    currentTheme = resolveTheme();
    applyTheme(currentTheme);
  }
}
mqLgUp.addEventListener('change', maybeAutoUpdate);
mqSysDark.addEventListener('change', maybeAutoUpdate);

// ===== Events =====
// Toggle
document.addEventListener('click', (e) => {
  const t = e.target.closest('[data-theme-toggle]');
  if (!t) return;

  const next = (htmlEl.getAttribute('data-theme') === 'dark') ? 'light' : 'dark';
  setSavedTheme(next);          // persist user choice
  currentTheme = next;
  applyTheme(next);
});

// Reset (optional: add a [data-theme-reset] button in HTML)
document.addEventListener('click', (e) => {
  const t = e.target.closest('[data-theme-reset]');
  if (!t) return;
  setSavedTheme(null);
  currentTheme = resolveTheme();
  applyTheme(currentTheme);
});
