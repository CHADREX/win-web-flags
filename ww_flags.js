/**
 * ww_flags.js
 * Injects a flag emoji font on Windows, where Segoe UI Emoji intentionally
 * does not render Regional Indicator sequences as country flags.
 * On all other platforms (macOS, iOS, Android, Linux) the script does nothing
 * and the font is never downloaded.
 *
 * Usage: <script src="ww_flags.js"></script>
 * ww_flags.woff2 must be in the same directory as this script.
 */

(function () {

  // Resolve woff2 path relative to this script tag (by src attribute)
  const FONT_URL = (function () {
    const scripts = document.querySelectorAll('script[src]');
    for (const s of scripts) {
      if (s.src.includes('ww_flags')) {
        return s.src.replace(/ww_flags\.js.*$/, 'ww_flags.woff2');
      }
    }
    // Fallback: hardcode absolute path
    return '/hub/order-gate/lib/ww_flags.woff2';
  })();

  // Check if running on Windows
  function isWindows() {
    return /Win/i.test(
      navigator.platform || navigator.userAgentData?.platform || ''
    );
  }

  // Canvas test: draw a flag emoji and count unique colors.
  // On Windows, flags render as letter boxes (monochrome) → few colors.
  // On working systems, flags render as colored images → many colors.
  function flagsAreBroken() {
    try {
      const canvas = document.createElement('canvas');
      canvas.width = canvas.height = 16;
      const ctx = canvas.getContext('2d');
      if (!ctx) return true;

      ctx.font = '14px "Segoe UI Emoji", sans-serif';
      ctx.fillText('\uD83C\uDDFA\uD83C\uDDE6', 0, 14); // 🇺🇦

      const data = ctx.getImageData(0, 0, 16, 16).data;
      const colors = new Set();
      for (let i = 0; i < data.length; i += 4) {
        if (data[i + 3] > 10) { // skip transparent pixels
          colors.add(`${data[i]},${data[i + 1]},${data[i + 2]}`);
        }
      }

      // Real flag = many colors; letter box = nearly monochrome
      return colors.size < 8;
    } catch (e) {
      return true;
    }
  }

  // Inject @font-face and apply font-family to the document
  function injectFont() {
    if (document.getElementById('ww-flags-style')) return; // already injected

    const style = document.createElement('style');
    style.id = 'ww-flags-style';
    style.textContent = `
      @font-face {
        font-family: 'WWFlags';
        src: url('${FONT_URL}') format('woff2');
        unicode-range: U+1F1E6-1F1FF; /* Regional Indicators only */
      }
    `;
    document.head.appendChild(style);

    // Prepend WWFlags to body font-family.
    // Browser will use it only for Regional Indicator codepoints (unicode-range).
    applyFontFamily(document.body);

    // Watch for dynamically added elements (SPA, lazy content)
    const observer = new MutationObserver((mutations) => {
      for (const m of mutations) {
        for (const node of m.addedNodes) {
          if (node.nodeType === 1) applyFontFamily(node);
        }
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });

    console.log('[ww_flags] font injected ->', FONT_URL);
  }

  // Prepend WWFlags to font-family without overriding existing fonts
  function applyFontFamily(el) {
    const current = getComputedStyle(el).fontFamily;
    if (current && !current.includes('WWFlags')) {
      el.style.fontFamily = `'WWFlags', ${current}`;
    }
    // Also patch child elements with explicit inline font-family
    for (const child of el.querySelectorAll('[style*="font-family"]')) {
      const cf = child.style.fontFamily;
      if (cf && !cf.includes('WWFlags')) {
        child.style.fontFamily = `'WWFlags', ${cf}`;
      }
    }
  }

  // Run only on Windows with broken flag rendering
  if (isWindows() && flagsAreBroken()) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', injectFont);
    } else {
      injectFont();
    }
  }

})();
