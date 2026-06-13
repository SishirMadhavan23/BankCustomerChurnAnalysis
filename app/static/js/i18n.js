/**
 * Bank Customer Churn Analysis - Internationalization (i18n) Module
 * Supports English, Hindi, and Telugu
 */

let currentLanguage = 'en';
let translationsCache = {};

/**
 * Initialize i18n system
 */
async function initI18n() {
    try {
        // Get language from URL or stored preference
        const urlParams = new URLSearchParams(window.location.search);
        const lang = urlParams.get('lang') || localStorage.getItem('bcca_lang') || 'en';
        
        // Load translations
        const response = await fetch(`/api/translations?lang=${lang}`);
        const result = await response.json();
        
        if (result.success) {
            translationsCache = result.data;
            currentLanguage = lang;
            document.documentElement.setAttribute('data-lang', lang);
            document.getElementById('langSelect').value = lang;
            applyTranslations();
            updateLanguageDisplay();
        }
    } catch (error) {
        console.error('Failed to initialize i18n:', error);
    }
}

/**
 * Switch the UI language
 * @param {string} lang - Language code ('en', 'hi', 'te')
 */
async function switchLanguage(lang) {
    if (lang === currentLanguage) return;
    
    try {
        const response = await fetch(`/api/translations?lang=${lang}`);
        const result = await response.json();
        
        if (result.success) {
            translationsCache = result.data;
            currentLanguage = lang;
            document.documentElement.setAttribute('data-lang', lang);
            
            // Update URL
            const url = new URL(window.location);
            url.searchParams.set('lang', lang);
            window.history.replaceState({}, '', url);
            
            // Store preference
            localStorage.setItem('bcca_lang', lang);
            
            applyTranslations();
            updateLanguageDisplay();
            
            // Refresh charts if dashboard is visible
            if (typeof loadDashboard === 'function') {
                loadDashboard();
            }
        }
    } catch (error) {
        console.error('Failed to switch language:', error);
    }
}

/**
 * Apply translations to all elements with data-i18n attribute
 */
function applyTranslations() {
    // Translate elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const text = getTranslatedText(key);
        if (text) {
            // For input placeholders
            if (element.tagName === 'INPUT' && element.hasAttribute('placeholder')) {
                element.placeholder = text;
            } else {
                element.textContent = text;
            }
        }
    });
    
    // Update page title
    const titleKey = document.querySelector('title')?.getAttribute('data-i18n');
    if (titleKey) {
        const titleText = getTranslatedText(titleKey);
        if (titleText) {
            document.title = titleText;
        }
    }
    
    // Dispatch event for dynamic content
    document.dispatchEvent(new CustomEvent('languageChanged', { 
        detail: { language: currentLanguage } 
    }));
}

/**
 * Get translated text for a given key
 * @param {string} key - Translation key
 * @returns {string|null} Translated text or null
 */
function getTranslatedText(key) {
    if (translationsCache[key]) {
        return translationsCache[key];
    }
    // Fallback: return the key itself if not found
    return null;
}

/**
 * Update the language display in footer
 */
function updateLanguageDisplay() {
    const display = document.getElementById('currentLang');
    if (display) {
        const langName = getTranslatedText('language_name');
        if (langName) {
            display.textContent = `${langName}`;
        }
    }
}

/**
 * Get current language code
 * @returns {string} Current language code
 */
function getCurrentLanguage() {
    return currentLanguage;
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', initI18n);