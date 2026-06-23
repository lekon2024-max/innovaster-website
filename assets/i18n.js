/**
 * i18n — Innovaster multilingual system
 * Supports: EN (default), ES (Español), RU (Русский)
 * Usage: add data-i18n="key" to any translatable element
 */
(function() {
  'use strict';

  // ── Translation Data ──────────────────────────────
  var I18N = {
    en: {},
    es: {},
    ru: {}
  };

  // ── Language Detection ────────────────────────────
  var LANG = localStorage.getItem('i18n_lang') || 'en';

  function setLang(lang) {
    LANG = lang;
    localStorage.setItem('i18n_lang', lang);
    applyTranslations();
    updateSwitcher();
    document.documentElement.lang = lang;
  }

  // ── Apply Translations ────────────────────────────
  function applyTranslations() {
    if (LANG === 'en') {
      // English is default — restore original text
      document.querySelectorAll('[data-i18n]').forEach(function(el) {
        var key = el.getAttribute('data-i18n');
        if (el._i18nOriginal === undefined) {
          el._i18nOriginal = el.innerHTML;
        }
        el.innerHTML = el._i18nOriginal;
      });
      // Restore placeholders
      document.querySelectorAll('[data-i18n-placeholder]').forEach(function(el) {
        el.placeholder = el.getAttribute('data-i18n-original') || '';
      });
      // Restore titles
      document.querySelectorAll('[data-i18n-title]').forEach(function(el) {
        el.title = el.getAttribute('data-i18n-original-title') || '';
      });
      return;
    }

    var translations = I18N[LANG];
    if (!translations) return;

    // Text content
    document.querySelectorAll('[data-i18n]').forEach(function(el) {
      var key = el.getAttribute('data-i18n');
      if (el._i18nOriginal === undefined) {
        el._i18nOriginal = el.innerHTML;
      }
      if (translations[key]) {
        el.innerHTML = translations[key];
      }
    });

    // Input placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(function(el) {
      var key = el.getAttribute('data-i18n-placeholder');
      if (!el.getAttribute('data-i18n-original')) {
        el.setAttribute('data-i18n-original', el.placeholder || '');
      }
      if (translations[key]) {
        el.placeholder = translations[key];
      }
    });

    // Title attributes
    document.querySelectorAll('[data-i18n-title]').forEach(function(el) {
      var key = el.getAttribute('data-i18n-title');
      if (!el.getAttribute('data-i18n-original-title')) {
        el.setAttribute('data-i18n-original-title', el.title || '');
      }
      if (translations[key]) {
        el.title = translations[key];
      }
    });
  }

  // ── Language Switcher ──────────────────────────────
  function updateSwitcher() {
    document.querySelectorAll('.lang-btn').forEach(function(btn) {
      var lang = btn.getAttribute('data-lang');
      btn.classList.toggle('active', lang === LANG);
    });
  }

  // ── Initialize ─────────────────────────────────────
  function init() {
    // Set up language button click handlers
    document.querySelectorAll('.lang-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var lang = this.getAttribute('data-lang');
        setLang(lang);
      });
    });

    // Apply saved language on load
    if (LANG !== 'en') {
      // Wait for DOM and translations
      setTimeout(function() {
        applyTranslations();
        updateSwitcher();
        document.documentElement.lang = LANG;
      }, 100);
    }
    updateSwitcher();
  }

  // ── Load Translations ──────────────────────────────
  function loadTranslations() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/assets/i18n_data.js', true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try {
          // Evaluate the JS to get the data
          var fn = new Function(xhr.responseText + '; return I18N_DATA;');
          var data = fn();
          if (data) {
            for (var lang in data) {
              if (I18N[lang]) {
                for (var key in data[lang]) {
                  I18N[lang][key] = data[lang][key];
                }
              }
            }
          }
          init();
        } catch(e) {
          console.warn('i18n: failed to parse translations', e);
          init();
        }
      } else {
        init();
      }
    };
    xhr.onerror = function() { init(); };
    xhr.send();
  }

  // ── Auto-start ─────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadTranslations);
  } else {
    loadTranslations();
  }

  // Expose globally
  window.i18nSetLang = setLang;
  window.i18nGetLang = function() { return LANG; };
})();
