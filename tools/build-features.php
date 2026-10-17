<?php
/**
 * build-features.php -- put the suite's feature list onto features.html.
 *
 * THE SOURCE OF TRUTH IS IN THE OTHER REPOSITORY. `dev/features.md` in EngCalcs is itself
 * generated, from `dev/features-source.md`, by `dev/scripts/generate_features.php`. Nothing here
 * writes a feature sentence; this script only transforms them into the markup this page uses, so
 * the list cannot drift by somebody retyping it.
 *
 * Run it after the feature list changes over there:
 *
 *     php tools/build-features.php [path/to/engcalcs/dev/features.md]
 *
 * It rewrites only what sits between the sentinel comments in features.html. The page's design
 * and its framing prose are hand-written and are never touched.
 *
 * THREE DEPARTURES FROM THE SOURCE, all deliberate, all declared below rather than done quietly:
 *
 *  - SKIP_SECTIONS. A whole `## area` this site does not show. See that array's own note.
 *  - SKIP_IDS. One sentence kept off this page, with the reason.
 *  - OVERRIDE. A sentence replaced because it would be wrong on a public page. The map is EMPTY
 *    and should stay that way -- an override is a debt, not a mechanism, because it makes this
 *    page and the source disagree about the same fact. The honest fix is upstream, in
 *    features-source.md. See the array's own note.
 *
 * The last two are keyed by the task IDs the source cites, so a reworded sentence still lands
 * correctly and a DELETED one stops the build instead of vanishing silently.
 */

$src = $argv[1] ?? __DIR__ . '/../../hawsedc.subset/engcalcs/dev/features.md';
$page = __DIR__ . '/../features.html';

/**
 * Sentences kept OFF this page, with the reason. Key: the source's cited IDs.
 *
 * `486` is the phone sentence, and it used to be RELOCATED rather than dropped: dev/positioning.md
 * §3 keeps mobile out of "a list of reasons to choose us" and gave it one home, the honest-edges
 * note at the foot of this page. **Tom deleted that whole note on 2026-09-12**, so the one place
 * the claim was allowed to stand is gone and there is nowhere to relocate it TO. It is therefore
 * not on this page at all, which §3 permits -- the rule constrains where the claim may appear, it
 * does not require the claim. Restore the note and this goes back to being a relocation.
 */
$SKIP_IDS = array('486' => 'the honest-edges note that was its only sanctioned home is gone');

/**
 * Sections of the source this page does NOT show. Key: the `## ` heading, value: the reason.
 *
 * **THIS SITE DOES NOT ADVERTISE THE CALCULATOR SUITE** (Tom, 2026-09-11: *"I don't think that LW
 * and its features page should advertise EC at all. I think we need to remove it."*). The two
 * products were one program until the divorce of 2026-09-11 (EngCalcs Task 625); the network model
 * now has its own chrome, its own front door at /app/, and no suite navbar. A features page that
 * still listed Manning pipe flow, orifice drain time, micro-hydropower, canal seepage and rock
 * chute sizing was selling somebody else's software on LibreWaterNet's own page.
 *
 * **SKIPPED HERE RATHER THAN DELETED AT THE SOURCE**, because `dev/features.md` is the EngCalcs
 * suite's own feature list and those features are real and still shipped -- they simply are not
 * this site's. One source of truth, two audiences; the choice of what to show belongs to the site
 * making it. A feature genuinely shared by both belongs in a section this page keeps, and the
 * offline/install line was moved there at the source for exactly that reason.
 */
$SKIP_SECTIONS = array(
	'The calculators' => 'the single-purpose hydraulic calculators are a separate suite (Task 625)',
);

/**
 * Sentence replaced. Key: cited IDs. See the docblock -- each entry needs a reason.
 *
 * **EMPTY, AND THAT IS THE STATE IT IS MEANT TO BE IN.** An override is a DEBT, not a mechanism:
 * it means a sentence is wrong at the source and this page is papering over it, so the two repos
 * quietly disagree about the same fact. The one entry this map ever held -- the colour bullet,
 * which understated the ramp catalogue and contradicted index.html -- was fixed upstream in
 * dev/features-source.md instead, and removed from here. Fix the next one there too; reach for
 * this array only when the source cannot be touched, and empty it again as soon as it can.
 */
$OVERRIDE = array();

$md = @file_get_contents($src);
if ($md === false) { fwrite(STDERR, "cannot read $src\n"); exit(1); }

$sections = array();
$cur = null;
$skipped = array();
$seen = array();
$pointers = array();
foreach (preg_split('/\R/', $md) as $line) {
	if (preg_match('/^## (.+)$/', $line, $m)) {
		$cur = trim($m[1]);
		if (isset($SKIP_SECTIONS[$cur])) { $cur = null; continue; }
		$sections[$cur] = array();
		continue;
	}
	if ($cur === null) { continue; }
	if (!preg_match('/^- (.*?)\s*<!--\s*(.+?)\s*-->\s*$/', $line, $m)) { continue; }
	$text = $m[1];
	$ids  = $m[2];
	$seen[$ids] = true;
	if (isset($OVERRIDE[$ids])) { $text = $OVERRIDE[$ids]; }
	if (isset($SKIP_IDS[$ids])) { $skipped[$ids] = $text; continue; }
	$sections[$cur][] = array($text, $ids);
	// A POINTER row carries `see: <heading>` where IDs would be (EngCalcs generate_features.php). It
	// is not a feature: it is shown, linked to its section, and left out of the count.
	if (strpos($ids, 'see: ') === 0) { $pointers[$cur][count($sections[$cur]) - 1] = trim(substr($ids, 5)); }
}

foreach (array_keys($SKIP_IDS) as $ids) {
	if (!isset($seen[$ids])) { fwrite(STDERR, "skipped feature $ids is no longer in the source\n"); exit(1); }
}
foreach (array_keys($OVERRIDE) as $ids) {
	if (!isset($seen[$ids])) { fwrite(STDERR, "overridden feature $ids is no longer in the source\n"); exit(1); }
}

/** Markdown inline -> HTML. Backticks are the only markup the source uses in a bullet. */
function inline($s) {
	$s = htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
	// The apostrophe is TYPOGRAPHIC on the page and PLAIN in the source (EDR-17, 2026-09-06).
	// htmlspecialchars turns it into &#039;, which renders as a typewriter mark in the middle of
	// a serif page whose hand-written half uses &rsquo;. The source stays plain so it is easy to
	// type; the conversion belongs here, at the one place a sentence becomes markup. A backtick
	// span is code and keeps the plain mark, so this runs BEFORE code spans are made.
	$s = preg_replace('/(\w)&#0?39;(?=\w|\b)/u', '$1&rsquo;', $s);
	return preg_replace('/`([^`]+)`/', '<code>$1</code>', $s);
}
function slug($s) {
	return trim(preg_replace('/-+/', '-', preg_replace('/[^a-z0-9]+/', '-', strtolower($s))), '-');
}

$total = 0;
$nav = array();
$body = array();
foreach ($sections as $title => $items) {
	if (!$items) { continue; }
	$id = slug($title);
	$total += count($items) - (isset($pointers[$title]) ? count($pointers[$title]) : 0);
	$nav[] = '<a href="#' . $id . '">' . inline($title) . '</a>';
	// **A SINGLE-COLUMN TABLE, one feature per row** (Tom, 2026-09-12: *"Can you please make the
	// features list a single-column table like other sites?"*). It was a two-column `ul`, which
	// is what made 37 one-sentence rows read as a sprawl: the eye has to find where the left
	// column ends and the right one begins, on every section. One column of full-width rows with
	// a rule between them is the shape a specification table has everywhere else.
	$out = "<section class=\"act\" id=\"$id\">\n<h2>" . inline($title)
		. ' <span class="ct">' . count($items) . "</span></h2>\n<table class=\"feats\">\n<tbody>\n";
	foreach ($items as $k => $it) {
		$cell = inline($it[0]);
		if (isset($pointers[$title][$k])) {
			$h = inline($pointers[$title][$k]);
			$cell = str_replace('(see ' . $h . ')', '(see <a href="#' . slug($pointers[$title][$k]) . '">' . $h . '</a>)', $cell);
			// A pointer may say only where its section sits, "(above)" or "(below)" (Tom, 2026-10-17).
			$cell = preg_replace('/\((above|below)\)/', '(<a href="#' . slug($pointers[$title][$k]) . '">$1</a>)', $cell);
		}
		$out .= "\t<tr><td>" . $cell . " <!-- " . $it[1] . " --></td></tr>\n";
	}
	$body[] = $out . "</tbody>\n</table>\n</section>";
}

$html = "<p class=\"count\">" . $total . " things it does.</p>\n\n"
	. "<nav class=\"jump\" aria-label=\"Sections\">\n\t" . implode("\n\t", $nav) . "\n</nav>\n\n"
	. implode("\n\n", $body) . "\n";

$doc = @file_get_contents($page);
if ($doc === false) { fwrite(STDERR, "cannot read $page\n"); exit(1); }
$doc = splice($doc, 'FEATURES', $html, $page);
file_put_contents($page, $doc);
echo "features.html: $total features in " . count($body) . " sections, from $src\n";

function splice($doc, $name, $new, $page) {
	$a = "<!-- BEGIN GENERATED $name -->";
	$b = "<!-- END GENERATED $name -->";
	$i = strpos($doc, $a);
	$j = strpos($doc, $b);
	if ($i === false || $j === false || $j < $i) { fwrite(STDERR, "$page has no $name sentinels\n"); exit(1); }
	return substr($doc, 0, $i + strlen($a)) . "\n" . $new . substr($doc, $j);
}
