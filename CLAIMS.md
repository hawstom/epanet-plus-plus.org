# Every factual claim on this site, with its source

One row per assertion, so each can be checked on its own. `EC` means the EngCalcs repository, which
is public at [github.com/hawstom/engcalcs](https://github.com/hawstom/engcalcs); a row citing a path
inside it is citing a file you can open. `LWN` means LibreWaterNet.org, the sister site whose pages
this one mirrors; where a row says a sentence is carried from LWN, that site's own claims ledger is
its first source. Rendered to `citations.html` by `tools/build.py`.

Ledger written 2026-09-27.

---

## 1. The headline and lede (index.html)

The headline and the lede are Tom Haws's own wording of 2026-09-27, made exact about the engine (OWA-EPANET 2.3.5, MIT-licensed) on his instruction the same day.

| # | Claim | Source |
|---|---|---|
| 1.1 | EPANET++ extends the EPANET engine with scenarios, a world map, fire flow, customers, custom properties, and asset libraries | Rows 2.1 to 2.6, one per extension |
| 1.2 | It is free, libre, and open source | GNU GPL v3 or later: `EC/CLAUDE.md` license line; row 6.1 |
| 1.3 | It is built on OWA-EPANET 2.3.5, Open Water Analytics' MIT-licensed continuation of EPA's EPANET | The default engine for a new project is EPANET (`EC/js/looped-network.js`, `defaultSettings()`, `engine: 'epanet'`). The engine is OWA-EPANET 2.3.5 (`EC/js/vendor/README.md`); see row 3.1 |
| 1.4 | The solver is the one the U.S. Environmental Protection Agency wrote and gave away | EPANET was written at EPA and is public domain under 17 U.S.C. § 105 (rows 7.2, 7.3). The engine we run is Open Water Analytics' continuation of it (row 7.6); see section 9 |
| 1.5 | Asset libraries can be imported across projects | `EC` commit `640c018f` "Import a library from another project file", merged to master in `bfb5d37d` (2026-09-18) on Tom's all-clear |
| 1.6 | It is not EPANET, and it is not affiliated with or endorsed by the EPA | Row 1.8 |
| 1.7 | It is one of many tools built on the engine EPA released | Row 7.5: EPANET's engine sits under many other programs, commercial and free |
| 1.8 | The first-screen disclaimer: EPANET is a program of the US EPA; this site is not EPA's; EPANET++ is not EPANET, not a version of it, and not an official successor; EPA has not reviewed, endorsed, approved, sponsored, or been asked | [epa.gov/water-research/epanet](https://www.epa.gov/water-research/epanet). Adapted from not-epanet.org's disclaimer paragraph, which its own ledger sources to Tom Haws's confirmation of 2026-09-06 that EPA had not been contacted. See section 9 |
| 1.9 | The screenshot title block: EPA Net3, 92 junctions, EPANET engine, GPL v3+ | Net3 as EPA ships it has 92 junctions, 2 reservoirs, and 3 tanks (97 nodes; the import on the Screenshots page reports 97). Carried from LWN |

## 2. Why ++ (index.html, features.html)

Each row is a statement about EPANET++ and not about EPANET. No row claims EPANET lacks the feature.

| # | Claim | Source |
|---|---|---|
| 2.1 | Scenarios hold only their differences from the base model, with an override report and a scenario comparison report | `EC/dev/roadmap-closed-ids.md` Tasks 201, 407, 412, 512; `EC/dev/features.md` |
| 2.2 | A world map, street or satellite, or your own backdrop; a wizard moves an XY model onto the map and converts nothing until you confirm | `EC/dev/features.md` (Tasks 145, 276, 476); `EC/js/lpn-terrain.js`. The confirm-or-cancel behavior is carried from LWN's Screenshots plate 6 |
| 2.3 | A whole-system fire flow analysis reporting, per junction, whether the required flow is met and which failure it hits, including pressure pulled down elsewhere | `EC/dev/roadmap-closed-ids.md` Task 530: whole-system sweep, `Failure modes` naming both modes, drawdowns measured, per-junction required flow |
| 2.4 | Customers: metered services with demand, service count, and pattern, connected by a draggable line to the node or pipe that serves them | `EC/dev/roadmap-closed-ids.md` Task 247: "metered demands lumped to the nearest node, with station, offset, per-service demand, service count, pattern and a draggable connection point that re-attaches to another asset"; `EC` merge `e82d8f9c` |
| 2.5 | Custom properties on any kind of asset, with labels and limits, overridable by a scenario, and flagged in place rather than cleared when a value breaks its limits | `EC/dev/custom-property-scope.md`: phases 1 and 2 shipped 2026-09-13; "everything is overridable by a scenario"; a value that breaks its design is "flagged in place, never cleared" (`EC/dev/ROADMAP.md` Task 636) |
| 2.6 | Libraries of pipe types, fittings, curves, patterns, controls, and rules, defined once and referred to by name; editing a pipe type edits every pipe using it | The six Libraries sections are `lpn_library_patterns`, `_curves`, `_pipetypes`, `_fittings`, `_controls`, `_rules` in `EC/lib/lang.ec.en.php`; Task 465 (pipe types), Task 590 (fittings) |
| 2.7 | Importing libraries skips a name already taken and lists it, so nothing already in the project changes | `EC/lib/lang.ec.en.php`, `lpn_library_import_tip` and `lpn_library_import_conflict` |
| 2.8 | The fittings list starts from the EPANET user manual's own table and is editable | `EC/lib/lang.ec.en.php`, `lpn_library_fittings_source`: the thirteen fittings of Table 3.3 of the EPANET 2.2 user manual |
| 2.9 | Group edit three ways: find and replace, select an area, spreadsheet tables | `EC/dev/features.md` (Task 266) |
| 2.10 | All of it is free, including the parts that are normally the paid tier | GPL v3 or later with no paid tier (row 6.1). "Normally the paid tier" is sanctioned wording in `EC/dev/positioning.md` §8; no vendor or price is named |

## 3. What is EPANET's (index.html, disclosures.html)

| # | Claim | Source |
|---|---|---|
| 3.1 | The engine is a 679 KB browser build of OWA-EPANET 2.3.5, released 2025-02-20, loaded on demand | `EC/js/vendor/epanet-js.js` is 678,695 bytes. `EC/js/vendor/README.md` names the engine OWA-EPANET 2.3.5. [OpenWaterAnalytics/EPANET releases](https://github.com/OpenWaterAnalytics/EPANET/releases), v2.3.5, February 20, 2025 |
| 3.2 | Extended-period runs, water age, source trace, chemical decay, pump energy, rule-based controls, and PRV/PSV/FCV valves run through the EPANET engine only | `EC/CLAUDE.md`, `lpn_` section: EPS "through the EPANET engine only"; "PRV/PSV/FCV solve through EPANET only". Water quality and pump energy are run-based (Tasks 566, 566.01) |
| 3.3 | Our own solver answers a single instant, pressures and flows only, with no time dimension | `EC/CLAUDE.md`: "The built-in solver solves one instant and is not getting a time dimension" |
| 3.4 | EPANET++ reads and writes EPANET's `.inp` file, and an unedited value comes back out character for character | `EC/CLAUDE.md`: "Export is character-exact on Net1/2/3"; `EC/js/lpn-inp.js` |
| 3.5 | A project also saves in a format of our own, because an `.inp` cannot hold scenarios, profile paths, the backdrop image, map view, multi-line Text, or longitude and latitude; five round trips are reported rather than dropped | Carried from LWN; its ledger rows 2.5a and 2.5b cite `EC/js/looped-network.js` `serializeProject()` and Task 281 |
| 3.6 | Extended-period results are checked against EPA's own Net3 report: 2,425 head comparisons over 25 steps, to 0.005 ft; water quality worst 0.105%; pump energy against the report's energy table | `EC/dev/lpn-spike/eps-net3-harness.js`; `EC/dev/roadmap-closed-ids.md` Tasks 566 and 566.01. Carried from LWN |
| 3.7 | The Hazen-Williams pair is derived from EPANET's form and differs from the common metric restatement by up to 0.12% from 50 mm to 2 m | `EC/js/PipeHydraulics.lib.js` header comment. Carried from LWN |
| 3.8 | The vocabulary is EPANET's: element names, the four curve types, the grammar of a rule, unit-switch behavior | `EC/CLAUDE.md`: "otherwise default to EPANET terminology"; "Four kinds" of curve; `EC/js/lpn-rules.js` |
| 3.9 | The curve editor and the asset table come from EPANET's; EPANET's five map colors are in the palette unsoftened; the default ramp is Viridis | Carried from LWN; its ledger rows 2.11 and 2.11a cite `EC/js/lpn-ramps.js` and `defaultSettings()` |

## 4. What exists, languages, and the invitation (index.html)

| # | Claim | Source |
|---|---|---|
| 4.1 | Draw junctions, reservoirs, tanks, pipes, pumps, valves, customers, and text on XY or on a latitude and longitude map with street or satellite view | `EC/dev/features.md`; customers per row 2.4 |
| 4.2 | Opening an `.inp` reports every difference rather than ignoring anything quietly | `EC/CLAUDE.md`: "Import reports every difference, never rejects, never drops silently" |
| 4.3 | Patterns, controls, tanks filling and draining, playback, water quality, and pump run time and energy cost | `EC/dev/features.md`, Extended period simulations section |
| 4.4 | Color the map by pressure, flow, velocity, or head loss; 41 color ramps | Carried from LWN; `EC/js/lpn-ramps.js` |
| 4.5 | Labels you drag, set, and keep, with leader lines | `EC/js/lpn-geom.js`, `EC/js/lpn-collide.js`; `EC/dev/positioning.md` §4 |
| 4.6 | "And although you of course prefer working on your PC, it works also on a phone in tall mode." | The one sanctioned phone sentence, verbatim: `EC/dev/positioning.md` §3 |
| 4.7 | The network editor is in 27 languages, translated in the program itself; right-to-left languages lay out right-to-left | `EC/lib/lang.ec.*.php` is 27 files; `EC/CLAUDE.md`: `lpn_` is "in scope in all 26 languages" beside English |
| 4.8 | The translations are AI-made against a hydraulics glossary, and each language's quality is recorded openly | `EC/dev/scripts/glossary.json`; `QUALITY` in `EC/lib/Language.Settings.php` |
| 4.9 | Looking for stakeholders, not for money: advisors, bug reports, power users with wish lists, non-profit directors | Tom Haws's four phrases, `EC/dev/positioning.md` §1, used in his order |
| 4.10 | There is no foundation and no governing document yet | `EC/dev/positioning.md` §1 and §8 |

## 5. Screenshots (screenshots.html)

| # | Claim | Source |
|---|---|---|
| 5.1 | Every caption and plate | Carried from LWN's screenshots page with the same fifteen captures, vetted publishable there against `EC/dev/screenshots/INDEX.md`. The counts are made consistent (fifteen throughout), and "upload for a spin" became "open it and try", because nothing is uploaded |
| 5.2 | The network in most plates is EPA's Net3 placed on the streets of Novato, California | Carried from LWN |

## 6. License and privacy (index.html, disclosures.html)

| # | Claim | Source |
|---|---|---|
| 6.1 | The software is GNU GPL v3 or later, with no paid tier | `EC/CLAUDE.md` license line; `EC/dev/positioning.md` §2 |
| 6.2 | The license paragraph in Disclosures item 2, quoted | Tom Haws, 2026-09-06, carried from LWN |
| 6.3 | Every calculation runs in your browser; there is no account; it installs and runs offline | `EC/CLAUDE.md`: no database, no authentication, all computation client-side; `EC/dev/features.md` (install for offline use) |
| 6.4 | Four features reach another server: OSM street tiles (shown on the first, empty project), Mapbox satellite tiles, Nominatim place-name search, and Mapbox terrain elevations; the last two ask their own consent | `EC/CLAUDE.md`, "Four third-party requests, all on this page" |
| 6.5 | No page of this site makes a request to another server, and none stores anything on your device | `check.sh` check 5 fails on any cross-origin fetch; the site has no script at all |

## 7. Credits and About EPANET (credits.html, epanet.html)

Carried from LWN's Credits and About EPANET pages; its ledger section 4 and 5 rows give the outside sources, repeated here in brief.

| # | Claim | Source |
|---|---|---|
| 7.1 | EPANET is a program of the US EPA, obtained from epa.gov/water-research/epanet | [epa.gov/water-research/epanet](https://www.epa.gov/water-research/epanet) |
| 7.2 | A work of the US government cannot be copyrighted in the United States | [17 U.S.C. § 105](https://uscode.house.gov/view.xhtml?req=%28title%3A17+section%3A105+edition%3Aprelim%29) |
| 7.3 | EPANET was created by Lewis A. Rossman for EPA and first appeared in 1993, with a formal report on its water quality model the same year | [Wikipedia: EPANET](https://en.wikipedia.org/wiki/EPANET); [OSTI record](https://www.osti.gov/biblio/5795398) |
| 7.4 | 2.2 was the last release EPA itself made | [USEPA/EPANET2.2](https://github.com/USEPA/EPANET2.2); `EC/js/vendor/README.md` |
| 7.5 | EPANET is used worldwide and its engine is embedded in many other programs | [Wikipedia: EPANET](https://en.wikipedia.org/wiki/EPANET); [EPA Science Matters](https://www.epa.gov/sciencematters/epanet-220-epa-and-water-community-collaboration) |
| 7.6 | Open Water Analytics continued EPANET in the open, in collaboration with EPA: 2.3 on 2024-07-17, 2.3.5 on 2025-02-20 | [OpenWaterAnalytics/EPANET releases](https://github.com/OpenWaterAnalytics/EPANET/releases) |
| 7.7 | The browser build of the engine is epanet-js, MIT, © Luke Butler, wrapping MIT OWA-EPANET compiled to WebAssembly | `EC/js/vendor/README.md`; `EC/js/vendor/epanet-js.LICENSE`. Named on the Credits page only, as a license credit (`EC/dev/positioning.md` §1, second exception) |
| 7.8 | Bootstrap 5.3.2 (MIT); Brewer color schemes (Apache 2.0); viridis, magma, inferno, plasma (CC0) | `EC/js/vendor/README.md`; `EC/js/lpn-ramps.js` |
| 7.9 | Cynthia Brewer published the schemes in 2002 with Mark Harrower and Penn State, and received the ICA Carl Mannerfelt Gold Medal in 2023 | [Wikipedia: Cynthia Brewer](https://en.wikipedia.org/wiki/Cynthia_Brewer) |
| 7.10 | The FSF released GPL version 3 on 2007-06-29 | [fsf.org/news/gplv3_launched](https://www.fsf.org/news/gplv3_launched) |
| 7.11 | A run report from the editor prints a version higher than EPA's download page offers | `EC/js/vendor/README.md`: printed as `2.3.05`, beside EPA's page offering 2.2.0 |
| 7.12 | The street map shows on the first, empty project; the search and the elevations each ask their own permission | Row 6.4. LWN's Credits page still says both services are off until turned on; that sentence was corrected here |

## 8. Disclosures items 3 to 5 (disclosures.html)

| # | Claim | Source |
|---|---|---|
| 8.1 | Development started on 28 July 2026; as of 1 September 2026 the software had carried one real-world design report | Tom Haws, 2026-09-06, carried from LWN |
| 8.2 | We do not publish a completeness claim against EPANET | `EC/dev/positioning.md` §2 |
| 8.3 | The AI paragraph, quoted | Tom Haws, 2026-09-06, carried from LWN |
| 8.4 | No EPA, government, or university affiliation, no sponsor, no foundation, no funding | `EC/dev/positioning.md` §1 and §8 |

## 9. Stated with a caution

- **"The same solver the U.S. Environmental Protection Agency wrote" (row 1.4).** The engine we
  run is OWA-EPANET 2.3.5, which Open Water Analytics developed from EPA's code after EPA's own
  2.2, in collaboration with EPA. The About EPANET and Credits pages say so. OWA-EPANET is MIT
  licensed; the EPA original is public domain.
- **EPA has not been asked (row 1.8).** Confirmed by Tom Haws on 2026-09-06 for the sister site.
  It must be confirmed again if anyone writes to EPA.
- **The exact release date of EPANET 2.2 and the name of the EPA division** are stated on the
  About EPANET page as unverified, as on LWN.

## 10. Who we are (advisors.html)

Not yet published (`noindex`, out of the sitemap and the nav) until Tom fills in its placeholder
cards. The two sentences already written about him.

| # | Claim | Source |
|---|---|---|
| 10.1 | Tom Haws wrote and copyrights EngCalcs, the calculator suite EPANET++ points to, starting in 2009, under the GNU GPL v3 or later the whole time | `EC/lib/HeadersFooters.lib.php:53`: "Copyright &copy; 2009&ndash;2026 Thomas Gail Haws. Licensed under the GNU GPL v3.0 or later." |
| 10.2 | The software and this site are written with heavy use of AI | `LWN/index.html:187`, "The software and this website are written with heavy use of AI"; row 8.3 (`EC/dev/positioning.md`, Tom Haws, 2026-09-06); `not-epanet.org/claims.html:116`, row 4.8b, Tom Haws, 2026-09-06: "one semi-retired engineer with an AI to build this in a summer" |

## 11. Claims deliberately not made

- Any statement that EPANET++ does everything EPANET does, or is as capable in any respect other
  than the measured agreements in row 3.6.
- Any statement that EPANET lacks a feature EPANET++ has.
- Any statement about what EPA thinks of this, or would think of it.
- Any number for how many people use the software, and any date or promise about future features.
- Any competing application or live commercial trademark, by name.
