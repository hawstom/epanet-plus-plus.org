#!/usr/bin/env python3
"""build.py -- everything on this site that is written once and repeated on every page.

    python3 tools/build.py            # rewrite the pages
    python3 tools/build.py --check    # exit 1 if any page is out of date (check.sh runs this)

Three things, each between sentinels, so everything else on a page stays hand-written:

  1. THE SITE BAR (<!-- BEGIN GENERATED CHROME --> ... <!-- END GENERATED CHROME -->), from NAV.
  2. EVERY LINK INTO THE APP. An anchor carrying data-app="SUFFIX" gets href = APP_URL + SUFFIX.
  3. citations.html, rendered whole from CLAIMS.md.

APP_URL IS THE ONE PLACE THE APP'S ADDRESS IS WRITTEN (Tom, 2026-09-27: "A for development.
Release as B1 for A/B testing."). Today the site is Option A, a poster pointing at the app's
existing home. When B1 mounts the app at https://epanet-plus-plus.org/app/, change APP_URL below,
run this script, and every button on every page follows. check.sh fails if a page's app link
disagrees with APP_URL, so a hand edit cannot leave one button pointing at the old address.
"""

import html
import io
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

APP_URL = "https://librewaternet.org/app/"

ORIGIN = "https://epanet-plus-plus.org/"

CONTACT_URL = "https://hawsedc.com/engcalcs/contact.php"

# The site bar, in order. epanet.html is deliberately NOT on it (the LibreWaterNet pattern): it is
# a supporting page for Credits, about somebody else's software, and marks Credits as current.
NAV = [
    ("index.html", "Front page"),
    ("features.html", "Feature list"),
    ("screenshots.html", "Screenshots"),
    ("credits.html", "Credits"),
    ("disclosures.html", "Disclosures"),
    ("citations.html", "Citations"),
    (CONTACT_URL, "Contact"),
]
CURRENT_ALIAS = {"epanet.html": "credits.html"}

PAGES = ["index.html", "features.html", "screenshots.html", "credits.html",
         "disclosures.html", "epanet.html", "citations.html"]


def chrome(page):
    cur = CURRENT_ALIAS.get(page, page)
    links = []
    for href, text in NAV:
        mark = ' aria-current="page"' if href == cur else ""
        links.append('\t\t<a href="%s"%s>%s</a>' % (href, mark, text))
    return ("<!-- BEGIN GENERATED CHROME -->\n"
            "\t<div class=\"marks\">\n"
            "\t\t<a class=\"wordmark\" href=\"index.html\">EPANET<span class=\"pp\">++</span></a>\n"
            "\t</div>\n"
            "\t<nav>\n" + "\n".join(links) + "\n\t</nav>\n"
            "\t<!-- END GENERATED CHROME -->")


CHROME_RE = re.compile(r"<!-- BEGIN GENERATED CHROME -->.*?<!-- END GENERATED CHROME -->", re.S)
APP_RE = re.compile(r'data-app="([^"]*)" href="[^"]*"')


def apply(page, text):
    n = len(CHROME_RE.findall(text))
    if n != 1:
        sys.exit("%s: expected exactly one GENERATED CHROME block, found %d" % (page, n))
    text = CHROME_RE.sub(lambda m: chrome(page), text)
    text = APP_RE.sub(lambda m: 'data-app="%s" href="%s%s"' % (m.group(1), APP_URL, m.group(1)), text)
    return text


# --- CLAIMS.md -> citations.html -------------------------------------------------------------

def inline(t):
    """Markdown inline to HTML. Escape first, then re-introduce the few tags we allow."""
    # Code spans first, kept apart so the typographic apostrophe below never reaches inside one.
    codes = []

    def keep(m):
        codes.append("<code>%s</code>" % html.escape(m.group(1), quote=False))
        return "\x00%d\x00" % (len(codes) - 1)
    t = re.sub(r"`([^`]+)`", keep, t)
    t = html.escape(t, quote=False)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", t)
    t = t.replace("'", "&rsquo;")
    t = re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], t)
    return t


def render(md):
    out, lines, i = [], md.split("\n"), 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("## "):
            out.append("</div>\n<div class=\"item\">\n<h3>%s</h3>" % inline(ln[3:].strip()))
            i += 1
            continue
        if ln.startswith("# ") or ln.strip() == "---" or ln.strip() == "":
            i += 1
            continue
        if ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1]):
            head = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append('<div class="table-scroll"><table>')
            out.append("<thead><tr>%s</tr></thead>" % "".join("<th>%s</th>" % inline(c) for c in head))
            out.append("<tbody>")
            for r in rows:
                rid = "c" + r[0].replace(".", "-")
                first = '<td><a class="rownum" href="#%s">%s</a></td>' % (rid, inline(r[0]))
                out.append('<tr id="%s">%s%s</tr>' % (rid, first, "".join("<td>%s</td>" % inline(c) for c in r[1:])))
            out.append("</tbody></table></div>")
            continue
        if ln.startswith("- "):
            items = []
            while i < len(lines) and (lines[i].startswith("- ") or
                                      (lines[i].startswith("  ") and lines[i].strip() and items)):
                if lines[i].startswith("- "):
                    items.append(lines[i][2:].strip())
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            out.append('<ul class="facts">%s</ul>' % "".join("<li>%s</li>" % inline(x) for x in items))
            continue
        para = [ln.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("|", "- ", "#")):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(para)))
    body = "\n".join(out)
    if body.startswith("</div>\n"):
        body = body[len("</div>\n"):]
    return body + "\n</div>"


CITATIONS_SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Every claim, with its source</title>
<meta name="description" content="Every factual assertion on epanet-plus-plus.org, one per row, with the source it rests on.">
<link rel="canonical" href="https://epanet-plus-plus.org/citations.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="EPANET++">
<meta property="og:url" content="https://epanet-plus-plus.org/citations.html">
<meta property="og:title" content="Every claim, with its source">
<meta property="og:description" content="Every factual assertion on epanet-plus-plus.org, one per row, with the source it rests on.">
<meta property="og:image" content="https://epanet-plus-plus.org/img/0082.png">
<meta property="og:image:width" content="1921">
<meta property="og:image:height" content="920">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="icon-192.png">
<link rel="stylesheet" href="style.css">
</head>
<body>
<!-- GENERATED by tools/build.py from CLAIMS.md. Do not edit by hand; edit CLAIMS.md and rebuild. -->
<div class="sheet-bg" aria-hidden="true"></div>

<div class="sheet">

<header class="topbar">
\t<!-- BEGIN GENERATED CHROME --><!-- END GENERATED CHROME -->
</header>

<main>

<div class="hero">
\t<span class="label">The whole ledger</span>
\t<h1>Every claim, with its source<span class="rule-under"></span></h1>
\t<p class="lede">One row per assertion on this site, so each stands or falls on its own.</p>

\t<div class="disclaimer">
\t\t<span class="label">How to read this</span>
\t\t<p><code>EC</code> means the EngCalcs repository, which holds the software this site points
\t\tto. It is public at <a href="https://github.com/hawstom/engcalcs">github.com/hawstom/engcalcs</a>,
\t\tso a row citing a path inside it is citing a file you can open. Where a claim rests on an
\t\toutside source, the source is linked and you can go and disagree with us. Every claim number
\t\tis a link to its own row.</p>
\t</div>
</div>

<section>
<div class="item">
%s
</section>

</main>

<footer>
\t<p><b>Not the EPA&rsquo;s.</b> This site is not affiliated with, endorsed by, or sponsored by the
\tUnited States Environmental Protection Agency. EPANET is a public-domain program of the US EPA.
\tEPANET++ is not EPANET.</p>
\t<p>This page makes no request to any other server: no fonts, no scripts, no images from
\telsewhere, no analytics, no cookies, and no storage on your device.</p>
\t<p><a href="index.html">Back to the front page</a> &middot;
\t<a href="disclosures.html">Disclosures</a></p>
</footer>

</div>
</body>
</html>
"""


def citations():
    md = io.open(os.path.join(ROOT, "CLAIMS.md"), encoding="utf-8").read()
    return apply("citations.html", CITATIONS_SHELL % render(md))


def build():
    out = {}
    for p in PAGES:
        if p == "citations.html":
            out[p] = citations()
            continue
        out[p] = apply(p, io.open(os.path.join(ROOT, p), encoding="utf-8").read())
    return out


if __name__ == "__main__":
    pages = build()
    stale = []
    for p, text in pages.items():
        path = os.path.join(ROOT, p)
        cur = io.open(path, encoding="utf-8").read() if os.path.exists(path) else ""
        if cur != text:
            stale.append(p)
            if "--check" not in sys.argv:
                io.open(path, "w", encoding="utf-8").write(text)
    if "--check" in sys.argv:
        if stale:
            print("STALE: %s. Run: python3 tools/build.py" % ", ".join(stale))
            sys.exit(1)
        print("FRESH: every page matches tools/build.py and CLAIMS.md")
    else:
        print("rebuilt: %s" % (", ".join(stale) if stale else "nothing changed"))
