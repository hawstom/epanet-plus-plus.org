# EPANET++ (epanet-plus-plus.org): working guide

**This repository is a website, not the software.** The water network editor it advertises lives in
the EngCalcs repository (`~/webdev/hawsedc.com/engcalcs`), and is served today as LibreWaterNet at
`https://librewaternet.org/app/`. Never copy code, strings, or numbers from EngCalcs into these
pages; link, or restate in your own words, and give the fact a row in `CLAIMS.md`.

**What this site is:** a mirrored rebrand of LibreWaterNet.org (`~/webdev/librewaternet.org`), the
same pages and the same stylesheet, positioned as EPANET extended (Tom, 2026-09-27: *"This is
essentially identically a mirrored rebrand of LWN with EPANET comparison tweaks because we are more
advanced now."*). LibreWaterNet leads with the invitation; this site leads with the extension claim.
Plan and rulings: `dev/epanet-plus-plus-plan.md` in EngCalcs (EngCalcs Task 697).

## The authority for every claim is in the OTHER repository

`dev/positioning.md` in EngCalcs is the record of what may be said, what has been struck, and why.
**Read it before writing or editing a sentence of copy.** `~/webdev/librewaternet.org/CLAUDE.md`
restates the rules that bite most often; all of them apply here. The ones that bite hardest on a site
with EPANET in its name:

- **Never a completeness claim against EPANET.** Not "does everything EPANET does", not a parity
  table. The "++" names what was added; it is not a claim to everything EPANET does.
- **Never say what EPANET lacks.** Every extension is written as a fact about us. Tom has already
  struck one "not downstream of EPANET" list for naming things EPANET does have.
- **No EPA affiliation, review, sponsorship, or endorsement, implied or stated.** The disclaimer
  sits on the front page's first screen and in every footer. Do not move it down.
- **The four struck phrases stay struck**: "your phone", "PC application", "the only third-party
  request", "no extended-period simulation". `check.sh` check 9 fails on them.
- **The phone claim is one sanctioned sentence, verbatim**: *"And although you of course prefer
  working on your PC, it works also on a phone in tall mode."* "A phone", never "your phone".
- **No competing application and no live commercial trademark by name.** epanet-js is named once,
  on Credits, as a license credit (positioning.md §1, second exception); Tom kept it off the front
  page (2026-09-27, Q4).
- **No line telling the visitor the button opens a LibreWaterNet-branded app** (Tom, 2026-09-27,
  Q2: *"No."*).
- **Do not restore "We are still finding out what EPANET can do that we cannot, and we say so."**
  Tom removed it from the lede, and the same reasoning took the "we have no idea what we are not"
  quote off this site's Disclosures page (*"I don't think it's most honest at this point to imply
  that we are not or that we don't know EPANET."*).
- **The headline and lede are Tom's wording, verbatim.** Change a word only on his ruling.
- **A claim corrected on LibreWaterNet is not corrected here**, and the reverse. When a claim is
  ruled on over there, grep for it here the same day.
- **Write the fact and stop.** Do not announce the site's own virtues. Quote Tom only from a dated
  first-person source. American spelling, serial comma, no em dash in visitor text.

## The app link is written in ONE place

`APP_URL` at the top of `tools/build.py`. Every button into the app is an anchor carrying
`data-app="SUFFIX"`, and the build writes `APP_URL + SUFFIX` into its href. Option A (today) points
at `https://librewaternet.org/app/`. **Release is Option B1** (Tom, 2026-09-27: *"A for development.
Release as B1 for A/B testing."*): the app mounted at `https://epanet-plus-plus.org/app/`,
nominating this origin as its own canonical. That is EngCalcs engineering (a host-aware canonical in
`lib/Canonical.lib.php`, per the plan), plus one line here: change `APP_URL` and rebuild.

## Before every commit

    python3 tools/build.py     # the site bar, every app link, and citations.html from CLAIMS.md
    sh check.sh                # eleven checks, seconds

- The site bar is generated between `BEGIN/END GENERATED CHROME`; edit `NAV` in `tools/build.py`.
- `citations.html` is generated whole from `CLAIMS.md`. **Never edit it by hand.**
- Every page: `<!doctype html>`, `<html lang="en">`, charset first in `<head>`, a viewport line, a
  description, `og:image`, `og:site_name` EPANET++, and a canonical equal to its `og:url`, both
  `https://epanet-plus-plus.org/<page>` (the front page is the bare origin). A new page also goes
  into `PAGES` in `tools/build.py` and into `sitemap.xml`.
- **No font, script, stylesheet, or image from another origin, ever**, and no storage. An outbound
  link is fine. The site has no script at all.
- The document root is this repository. A new directory must be declared served or blocked in
  `check.sh` check 11, and a blocked one needs its `RedirectMatch 404` in `.htaccess`. Never add an
  `Options` line to `.htaccess`: without `AllowOverride Options` it 500s the whole host.

## Pages

| Page | What it is |
|---|---|
| `index.html` | Tom's headline and lede, the first-screen disclaimer, what the ++ adds, what is EPANET's, what exists, languages, who we need, license and privacy |
| `features.html` | The feature list, hand-maintained: LibreWaterNet's list plus the extensions, in our words |
| `screenshots.html` | LibreWaterNet's fifteen annotated plates, same captures (`img/`) |
| `credits.html`, `epanet.html`, `disclosures.html` | Mirrored from LibreWaterNet, rebranded |
| `citations.html` | Generated from `CLAIMS.md` |

The images are LibreWaterNet's committed captures, vetted publishable there against EngCalcs'
`dev/screenshots/INDEX.md`. Never publish an image that index marks No.

## Viewing locally

    php -S 127.0.0.1:8097 -t ~/webdev/epanet-plus-plus.org

or open `index.html` from the file system; every link is relative.

## State

Built 2026-09-27, not deployed, no remote. `epanetpp.org` (its own repository beside this one) is a
301 to this origin. Tom publishes; a push here will publish once the host points at it.
