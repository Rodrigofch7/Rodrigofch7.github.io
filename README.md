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

## Structure
- `index.html` — everything (markup, styles, script) in one file
- `assets/` — video demos referenced by the projects section

## Notes
- No dependencies to install — open `index.html` directly or serve statically
