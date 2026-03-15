# 🏳 win-web-flags

Fix missing country flag emoji on Windows by injecting a subsetted emoji font — only for browsers/systems that need it.

Windows intentionally does not render flag emoji (Regional Indicator sequences) in **Segoe UI Emoji**. All other platforms (macOS, iOS, Android, Linux) have flags out of the box. This project fixes that for websites without touching anything on non-Windows platforms.

---

## How it works

1. **`ww_flags.js`** — detects Windows + broken flag rendering via canvas test, then injects a `@font-face` with `unicode-range: U+1F1E6-1F1FF` so the browser pulls the font only for flag characters
2. **`convert_ww_flags.py`** — subsets any emoji `.ttf` down to flag glyphs only and converts to `.woff2` (~50–80 KB instead of the full font)
3. A **MutationObserver** handles dynamically added content (SPAs, lazy-loaded elements)

The canvas test draws 🇺🇦 and counts unique pixel colors — flag emoji render as colorful pixels, broken Windows rendering shows monochrome letter boxes.

---

## Requirements

- An emoji font (`.ttf`) that includes country flags — example: [JoyPixels](https://www.joypixels.com/), [Twemoji](https://github.com/mozilla/twemoji-colr), [Noto Color Emoji](https://fonts.google.com/noto/specimen/Noto+Color+Emoji)
- Python 3.7+ with `fonttools` and `brotli` for the conversion script

---

## Setup

### 1. Install Python dependencies

```bash
pip install fonttools brotli
```

### 2. Convert emoji TTF → WOFF2 (flags only)

```bash
python convert_ww_flags.py ww_flags.ttf
```

Output:
```
ww_flags_flags.ttf    ← subsetted TTF
ww_flags_flags.woff2  ← final web font (~50–80 KB)
flags_test.html       ← browser test page with all ~250 flags
```

Rename `ww_flags_flags.woff2` to `ww_flags.woff2`.

### 3. Deploy to your website

Put both files in the same directory:
```
ww_flags.js
ww_flags.woff2
```

Add to your HTML:
```html
<script src="ww_flags.js"></script>
```

That's it. On non-Windows platforms the script does nothing and the font is never downloaded.

---

## Demo / Test

After running `convert_ww_flags.py`, open `flags_test.html` in your browser (woff2 must be in the same folder). All ~250 country flags should render using the injected font.

---

## Browser support

| Browser | Windows | macOS / Linux / mobile |
|---------|---------|------------------------|
| Chrome  | ✅ Fixed | ✅ Native (script skipped) |
| Firefox | ✅ Fixed | ✅ Native (script skipped) |
| Edge    | ✅ Fixed | ✅ Native (script skipped) |

---

## Files

| File | Description |
|------|-------------|
| `ww_flags.js` | Detection + font injection script |
| `convert_ww_flags.py` | TTF → WOFF2 subsetting tool |
| `flags_test.html` | Generated test page (run convert script first) |

---

## License

Scripts (`ww_flags.js`, `convert_ww_flags.py`) — **MIT**

The emoji font itself is **not covered** by this license — check the license of whichever font you use.
