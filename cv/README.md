# CV variants

One CV per target market, plus a general version. All four share the same facts;
they differ in framing, emphasis, and ordering.

| Variant | Use for | Published? |
|---|---|---|
| `general/` | The website, LinkedIn, anyone who asks generically | **Yes** — `assets/Rodrigo_Franca_Chaves_CV.pdf` |
| `consulting/` | Economic consulting (Analysis Group, Cornerstone, Brattle, CRA) | No — attach manually |
| `research/` | Policy institutes, international organizations, research groups | No — attach manually |
| `analytics/` | Data science / analytics roles in tech and finance | No — attach manually |

## Build

```bash
./build.sh          # builds all four, copies general/ to assets/
```

Requires `pdflatex` with `charter`, `titlesec`, `enumitem`, `tabularx`, `microtype`
(all in TeX Live). Each variant runs pdflatex twice — hyperref needs the second pass.

## Layout

```
shared/     preamble.tex  header.tex  education.tex  publications.tex
<variant>/  cv.tex  summary.tex
```

`shared/` holds what must never diverge: the macros, contact block, degrees, and
papers. Each variant owns its `summary.tex` plus the experience, projects, and
skills sections inside its `cv.tex`.

**Facts live in more than one place.** Tailoring means each variant restates the
same experience differently, so a factual correction — a date, a figure, a job
title — has to be applied in all four `cv.tex` files. Grep before you edit:

```bash
grep -rn "1.1M" */cv.tex
```

## Keep the targeted variants off the public site

Only `general/` is copied into `assets/`. Do not link the others from the website:
a consulting recruiter finding an analytics-tailored CV undercuts the point of
tailoring. Built PDFs are gitignored; the `.tex` sources are tracked.
