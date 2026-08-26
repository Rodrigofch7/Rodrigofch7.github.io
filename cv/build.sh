#!/usr/bin/env bash
# Builds every CV variant. The general one is what the website publishes.
set -euo pipefail
cd "$(dirname "$0")"
VARIANTS=(general consulting research analytics antitrust analysisgroup epic brattle)

for v in "${VARIANTS[@]}"; do
  [ -d "$v" ] || { echo "skipping $v (not present)"; continue; }
  ( cd "$v"
    pdflatex -interaction=nonstopmode -halt-on-error cv.tex >/dev/null
    pdflatex -interaction=nonstopmode -halt-on-error cv.tex >/dev/null   # hyperref needs a 2nd pass
  )
  echo "built $v/cv.pdf ($(pdfinfo "$v/cv.pdf" | awk '/Pages/{print $2}') pages)"
done

# Nothing is published to the site: the CV is not hosted publicly.
echo "all variants built locally; none published"
