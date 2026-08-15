# Portfolio Site

Single-page personal portfolio built with plain HTML/CSS/JS — no framework, no build step.

## Stack
- **HTML/CSS/JS**: one static `index.html`, custom CSS (no framework), vanilla JS for the "click to copy email" chips
- **Fonts**: Google Fonts (Inter)
- **Hosting**: static file, deployable anywhere (GitHub Pages, Netlify, S3, etc.)

## Assets
- Project demo videos compressed via `ffmpeg` in the Ubuntu terminal before adding to `/assets` (kept file size small for fast page loads):
  ```bash
  ffmpeg -i input.mp4 -vcodec libx264 -crf 28 -preset veryslow -an output.mp4
  ```
  - `-crf 28`: quality/size tradeoff (lower = better quality, bigger file)
  - `-an`: strips audio (not needed for silent looping demos)
  - Videos embedded with `autoplay loop muted playsinline` for lightweight, hands-off looping
- Social/link preview card (`assets/og-card.jpg`, 1200×630) — the image LinkedIn, X, Slack, etc. show when the site is shared. Edit `assets/og-card.source.html`, then re-render:
  ```bash
  chrome --headless --force-device-scale-factor=2 --window-size=1200,630 \
    --screenshot=card.png assets/og-card.source.html
  ffmpeg -y -i card.png -vf scale=1200:630 -q:v 3 assets/og-card.jpg
  ```
  - After deploying a new card, refresh LinkedIn's cache via the [Post Inspector](https://www.linkedin.com/post-inspector/)
- Publication thumbnails are capped at 560px wide (2× their 280px display size):
  ```bash
  ffmpeg -y -i original.jpg -vf scale=560:-2 -q:v 7 assets/pub_name.jpg
  ```
- Video poster frames (first frame, shown before the video decodes):
  ```bash
  ffmpeg -y -i assets/video_x.mp4 -vf "select=eq(n\,0),scale=900:-2" -frames:v 1 -q:v 5 assets/poster_x.jpg
  ```
- Favicon is an "RC" monogram in `assets/favicon.svg`, which carries its own
  `prefers-color-scheme` block so it adapts to the browser's tab theme.
  `assets/favicon-64.png` is the raster fallback, rasterised by screenshotting the SVG
  in headless Chrome at 64×64.
- Hero headshot resized with `ffmpeg` to a 480px `1x` and a 960px `2x` variant, served via `srcset` (also used as the Open Graph preview image and favicon):
  ```bash
  ffmpeg -i input.jpeg -vf "scale=480:480:flags=lanczos" -q:v 3 assets/rodrigo-headshot.jpg
  ```

## CV
LaTeX source lives in `cv/cv.tex` and compiles with `pdflatex` (needs the `charter`, `titlesec`, `enumitem`, `tabularx` packages — all in TeX Live). To rebuild after editing:
```bash
cd cv && pdflatex -interaction=nonstopmode cv.tex   # run twice: hyperref needs a second pass
cp cv.pdf ../assets/Rodrigo_Franca_Chaves_CV.pdf
```
The site's "Download CV" button points at `assets/Rodrigo_Franca_Chaves_CV.pdf`, so the copy step is what actually publishes a new version.

## Structure
- `index.html` — everything (markup, styles, script) in one file
- `assets/` — video demos, publication thumbnails, social card, and the published CV PDF
- `cv/` — LaTeX source for the CV (build artifacts gitignored)

## Notes
- No dependencies to install — open `index.html` directly or serve statically
