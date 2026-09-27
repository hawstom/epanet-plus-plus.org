#!/bin/sh
# Everything this repository checks. Run it before every commit:  sh check.sh
#
# Checks 1 to 7 are LibreWaterNet.org's, carried over on the sibling pattern; the reasons for each are
# written out in that repository's check.sh and are not repeated at length here. 8 to 11 are this
# site's own.

cd "$(dirname "$0")" || exit 1
fail=0
say() { printf '%s\n' "$*"; }
bad() { fail=1; printf 'FAIL  %s\n' "$*"; }

ORIGIN='https://epanet-plus-plus.org/'

# VISITOR TEXT: the page without comments, <style>, <script> and <code>. Non-greedy on purpose: a
# greedy removal eats the rest of the document and the check then passes over nothing.
prose() {
	awk '{ buf = buf $0 "\n" }
	     END { gsub(/<!--([^-]|-[^-]|--[^>])*-->/, "", buf)
	           gsub(/<style[^>]*>([^<]|<[^\/]|<\/[^s])*<\/style>/, "", buf)
	           gsub(/<script[^>]*>([^<]|<[^\/]|<\/[^s])*<\/script>/, "", buf)
	           gsub(/<code>[^<]*<\/code>/, "", buf)
	           print buf }' "$1"
}

# 1. EVERY PAGE DECLARES UTF-8 IN ITS FIRST 1024 BYTES. The host sends text/html with no charset,
#    so a page that does not say so is decoded as Windows-1252.
for f in *.html; do
	head -c 1024 "$f" | grep -qi 'charset[ ]*=[ ]*.\?utf-8' \
		|| bad "$f declares no UTF-8 charset in its first 1024 bytes"
done

# 2. EVERY LOCAL src RESOLVES. Looped in this shell, not down a pipe, so `bad` can fail the build.
for f in *.html; do
	for src in $(grep -o 'src="[^"]*"' "$f" | sed 's/src="//;s/"//'); do
		case "$src" in http*|data:*|//*) continue ;; esac
		[ -f "$src" ] || bad "$f references a missing file: $src"
	done
done

# 3. EVERY LOCAL href RESOLVES. A root-relative href is checked against this tree too: this site
#    declares no server mounts (Option A serves no /app/ here).
for f in *.html; do
	for href in $(grep -o 'href="[^"]*"' "$f" | sed 's/href="//;s/"//'); do
		case "$href" in http*|\#*|mailto:*|data:*|//*) continue ;; esac
		[ -n "$href" ] || { bad "$f has an empty href (run: python3 tools/build.py)"; continue; }
		path=${href%%#*}; path=${path%%\?*}
		case "$path" in
			/) path=index.html ;;
			/*) path=".$path" ;;
		esac
		[ -f "$path" ] || bad "$f links to a missing file: $href"
	done
done

# 4. EVERY PAGE IS A DOCUMENT, WITH ITS CARD AND ITS OWN ADDRESS.
for f in *.html; do
	head -c 200 "$f" | grep -qi '<!doctype html>' || bad "$f does not open with <!doctype html> (quirks mode)"
	grep -qi '<html lang="[a-z-]*"' "$f" || bad "$f has no <html lang>"
	grep -qi '<head>' "$f" && grep -qi '<body' "$f" || bad "$f lacks a real <head> or <body>"
	grep -qi '<meta name="viewport"' "$f" || bad "$f has no viewport meta (a phone lays it out at 980px)"
	grep -qi '<meta name="description"' "$f" || bad "$f has no meta description"
	grep -qi '<meta property="og:image"' "$f" || bad "$f has no og:image"
	grep -qi '<meta property="og:site_name" content="EPANET++"' "$f" || bad "$f has no og:site_name EPANET++"
	can=$(grep -o '<link rel="canonical" href="[^"]*"' "$f" | sed 's/.*href="//;s/"//')
	ogu=$(grep -o '<meta property="og:url" content="[^"]*"' "$f" | sed 's/.*content="//;s/"//')
	# Each page nominates ITSELF under the one origin. The front page is the bare origin.
	want="$ORIGIN$f"; [ "$f" = index.html ] && want="$ORIGIN"
	[ "$can" = "$want" ] || bad "$f canonical is '$can', expected '$want'"
	[ "$ogu" = "$want" ] || bad "$f og:url is '$ogu', expected '$want'"
done

# 5. NOTHING IS FETCHED FROM ANYBODY ELSE. An outbound LINK is fine; a fetch is not.
for f in *.html style.css; do
	grep -o '<link[^>]*rel="stylesheet"[^>]*>' "$f" | grep -q 'http' && bad "$f loads a stylesheet from another origin"
	grep -o '<link[^>]*rel="preconnect"[^>]*>' "$f" | grep -q 'http' && bad "$f preconnects to another origin"
	grep -o '<script[^>]*src="http[^"]*"' "$f" | grep -q . && bad "$f loads a script from another origin"
	grep -o '<img[^>]*src="http[^"]*"' "$f" | grep -q . && bad "$f loads an image from another origin"
	grep -o '@import' "$f" | grep -q . && bad "$f uses @import"
	grep -o '@font-face' "$f" | grep -q . && bad "$f declares a webfont"
	grep -oE 'url\(["'"'"']?https?:' "$f" | grep -q . && bad "$f fetches a CSS asset from another origin"
	grep -qE 'localStorage|sessionStorage|indexedDB|document\.cookie' "$f" && bad "$f touches storage on the visitor's device"
done

# 6. THE EM DASH RATCHET, IN VISITOR TEXT ONLY, AT ZERO.
for f in *.html; do
	n=$(prose "$f" | grep -o -e '—' -e '&mdash;' | wc -l)
	[ "$n" = 0 ] || bad "$f has $n em dash(es) in visitor text; the ratchet is at zero"
done

# 7. TAGS NEST. A stray </div> once moved every screenshot on LibreWaterNet's front page out of its
#    container and nothing else noticed.
for f in *.html; do
	python3 - "$f" <<'PYEOF' || fail=1
import sys
from html.parser import HTMLParser
VOID = {'br','img','input','meta','link','hr','source','area','base','col','embed','param','track','wbr'}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack=[]; self.err=[]
    def handle_starttag(self, t, a):
        if t not in VOID: self.stack.append((t, self.getpos()[0]))
    def handle_endtag(self, t):
        if t in VOID: return
        if not self.stack:
            self.err.append('line %d: stray </%s>' % (self.getpos()[0], t)); return
        if self.stack[-1][0] != t:
            self.err.append('line %d: </%s> closes <%s> opened at line %d'
                            % (self.getpos()[0], t, self.stack[-1][0], self.stack[-1][1]))
            for i in range(len(self.stack)-1, -1, -1):
                if self.stack[i][0] == t:
                    del self.stack[i:]; break
        else:
            self.stack.pop()
f = sys.argv[1]
p = P(); p.feed(open(f, encoding='utf-8').read())
left = [x for x in p.stack if x[0] not in ('html', 'body')]
if p.err or left:
    for e in p.err[:5]: print('FAIL  %s %s' % (f, e))
    for t, l in left[:5]: print('FAIL  %s: <%s> opened at line %d is never closed' % (f, t, l))
    sys.exit(1)
PYEOF
done

# 8. THE GENERATED PARTS ARE FRESH: the site bar, every app link (= APP_URL in tools/build.py, the
#    ONE place the app's address is written), and citations.html from CLAIMS.md.
python3 tools/build.py --check >/dev/null || bad "a page is stale against tools/build.py or CLAIMS.md. Run: python3 tools/build.py"

# 9. THE FOUR STRUCK CLAIMS STAY STRUCK (EngCalcs dev/scripts/public_claim_check.php holds the same
#    four for the app). Each was written, shipped, and struck by Tom personally.
for f in *.html; do
	prose "$f" | grep -inE 'your[[:space:]]+phone|PC[[:space:]]+application|only[[:space:]]+third[- ]?party[[:space:]]+request|no[[:space:]]+extended[- ]?period[[:space:]]+simulation' \
		| sed "s|^|FAIL  $f: struck claim: |" | grep . && fail=1
done

# 10. THE SITEMAP LISTS EXACTLY THE PAGES.
for f in *.html; do
	want="$ORIGIN$f"; [ "$f" = index.html ] && want="$ORIGIN"
	grep -q "<loc>$want</loc>" sitemap.xml || bad "sitemap.xml does not list $want"
done
n_pages=$(ls *.html | wc -l); n_locs=$(grep -c '<loc>' sitemap.xml)
[ "$n_pages" = "$n_locs" ] || bad "sitemap.xml has $n_locs entries for $n_pages pages"

# 11. EVERY DIRECTORY IS DECLARED SERVED OR BLOCKED. The document root is this repository, so an
#     undeclared directory is public. LibreWaterNet's tools/ was publicly executable until 2026-09-18.
SERVED='img'
BLOCKED='tools'
for d in */; do
	d=${d%/}
	case " $SERVED $BLOCKED " in *" $d "*) ;; *) bad "directory $d/ is neither served nor blocked; declare it in check.sh" ;; esac
done
for d in $BLOCKED; do
	grep -qF "RedirectMatch 404 \"^/$d(/|\$)\"" .htaccess || bad ".htaccess does not block /$d/"
done

if [ "$fail" = 0 ]; then say 'All checks pass.'; else say ''; say 'BLOCKING FAILURES above.'; fi
exit "$fail"
