#!/usr/bin/env python3
"""Quality gate for every built CV. Run by build.sh; fails the build on any hit.

Checks em dashes, GPA, UK spelling, page limits, and any private rules in .check-private.
Usage: python3 check.py [extra.pdf ...]
"""
import re, subprocess, sys, glob, os

UK_STEMS = ["digitis", "privatis", "organis", "recognis", "specialis", "prioritis", "standardis", "summaris", "utilis",
            "emphasis", "analys", "realis", "criticis", "finalis", "localis", "categoris", "visualis", "authoris", "centralis",
            "generalis", "harmonis", "hospitalis", "incentivis", "mobilis", "normalis", "penalis", "stabilis", "subsidis",
            "urbanis", "modernis", "optimis", "minimis", "maximis", "characteris", "capitalis", "monetis", "randomis",
            "parametris", "customis", "globalis", "internationalis", "operationalis"]
UK = (r"\b\w*isations?\b|\b(" + "|".join(UK_STEMS) + r")(e|es|ed|ing)\b"
      r"|\bcentres?\b|\bmetres?\b|diarrhoea|\bprogrammes?\b|\bbehaviour|\bneighbour|\bmodelling\b|\blabour\b|\bcolour|\bfavour")
UK_OK = {"emphasis", "analysis", "analyses", "synthesis"}
BANNED = [
    (r"\u2014", "em dash"),
    (r"\bGPA\b", "GPA"),
]
PUBLIC_ONLY = []

# Private rules live in a gitignored file: one "regex<TAB>reason" per line; prefix "public:" for public-CV-only rules.
_private = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".check-private")
if os.path.exists(_private):
    for line in open(_private, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line or line.startswith("#") or "\t" not in line:
            continue
        pat, why = line.split("\t", 1)
        (PUBLIC_ONLY if pat.startswith("public:") else BANNED).append((pat[len("public:"):] if pat.startswith("public:") else pat, why))

MAX_PAGES = {"general": 2}          # everything else: 2 pages max as well
DEFAULT_MAX = 2

def text(pdf):
    return subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout

def pages(pdf):
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else 0

def check(pdf, variant=None):
    problems = []
    t = text(pdf)
    for pat, why in BANNED:
        if re.search(pat, t): problems.append(why)
    uk = [m.group(0) for m in re.finditer(UK, t, re.I) if m.group(0).lower() not in UK_OK]
    if uk: problems.append("UK spelling: " + ", ".join(sorted(set(uk))))
    if variant == "general":
        for pat, why in PUBLIC_ONLY:
            if re.search(pat, t): problems.append(why)
    limit = MAX_PAGES.get(variant, DEFAULT_MAX)
    if variant and pages(pdf) > limit: problems.append(f"{pages(pdf)} pages (limit {limit})")
    return problems

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    targets = [(p, os.path.basename(os.path.dirname(p))) for p in glob.glob(os.path.join(here, "*", "cv.pdf"))]
    targets += [(p, None) for p in sys.argv[1:]]
    failed = 0
    for pdf, variant in sorted(targets):
        probs = check(pdf, variant)
        if probs:
            failed += 1
            print(f"FAIL {os.path.relpath(pdf, here)}: " + "; ".join(probs))
    print(f"QA: {len(targets) - failed}/{len(targets)} documents clean")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
