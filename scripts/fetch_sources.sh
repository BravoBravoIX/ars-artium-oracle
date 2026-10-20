#!/usr/bin/env bash
# Download the public sources this study needs, into SOURCE_DIR, and check them against the
# SHA-256 sums of the copies used for the published results (sources/SHA256SUMS).
# None of these files is redistributed here. Every download uses HTTPS with the certificate
# verified (curl's default). Needs bash, curl and sha256sum.
# Usage: scripts/fetch_sources.sh SOURCE_DIR
#        WITH_IMAGES=1 scripts/fetch_sources.sh SOURCE_DIR   (also the LJS 251 page images, 508 MB)
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
SUMS="$HERE/sources/SHA256SUMS"
OUT="$1"
mkdir -p "$OUT"/gutenberg
UA="ars-artium-oracle source fetch (one request at a time)"
get() { [ -s "$2" ] || { curl -fsSL --proto '=https' --retry 3 -A "$UA" -o "$2.part" "$1" && mv "$2.part" "$2"; sleep 2; }; }

# 1. Latin reference texts for the letter model of test 3 (Project Gutenberg, public domain in
#    the USA): Caesar, Cicero, Sallust, Quintilian, Virgil, Catullus, Augustine, Cicero's Cato
#    Maior, Erasmus.
for id in 218 226 7402 21827 227 23294 33849 14945 8400; do
  get "https://www.gutenberg.org/cache/epub/$id/pg$id.txt" "$OUT/gutenberg/pg$id.txt"
done

# 2. Optional: the page images of Penn LJS 251 (Internet Archive item ljs251, uploaded by Penn
#    Libraries, Public Domain Mark; the Penn record says No Copyright - United States). Needed
#    only to check the transcription against the manuscript.
if [ "${WITH_IMAGES:-0}" = 1 ]; then
  mkdir -p "$OUT/ljs251"
  get https://archive.org/download/ljs251/ljs251_jp2.zip "$OUT/ljs251/ljs251_jp2.zip"
fi

status=0
cd "$OUT"
while read -r sum path; do
  [ -e "$path" ] || continue
  if [ "$(sha256sum "$path" | cut -d' ' -f1)" = "$sum" ]; then
    echo "OK       $path"
  else
    echo "CHANGED  $path (differs from the copy the results were made from; results may differ)" >&2
    status=1
  fi
done < "$SUMS"
exit $status
