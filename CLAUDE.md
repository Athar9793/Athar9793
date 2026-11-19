# Project: MEP consultant portfolio website

- The whole site is `index.html` (single file, no build). Published by GitHub Pages from `main`.
- Business: Azmi MEP Consultants (Arabic: عزمي), Riyadh, KSA.

## Working rules
- For any change: commit on the session branch → open a PR → squash-merge it. Do not ask for approval.
- If information is missing, use clearly marked placeholders and continue. Never invent quotes or details presented as real.
- Keep the Arabic toggle in sync: any new visible English text must get an Arabic entry in the translation map at the end of `index.html`.
- Keep light/dark themes working: use the CSS colour variables, not hard-coded colours.
- Check changes in headless Chromium (Playwright) for script errors before opening the PR.
- Keep replies short and token usage low.

## Brand
- Colours: navy #102A43, blue #176B91, teal #00A6A6, silver #B8C4CE, light grey #F3F6F8. Fonts: Montserrat (headings), Inter (body).
- Logo files live in `branding/` (built from SVG; text converted to paths).
- 24 image slots: files go in `images/<folder>/<name>.webp` as listed in `images/README.md`; missing files fall back to a navy blueprint placeholder.
- Extra pages: `services/*.html` (one per service card) and `blog/*.html` (one per post) are generated from index.html content; each has its own small Arabic translation map.
