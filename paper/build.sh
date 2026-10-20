#!/bin/sh
# Builds paper/ars-artium-oracle.pdf from the Typst source (needs uv; fetches the typst package).
cd "$(dirname "$0")" && uv run --no-project --with typst==0.15.0 python -c "import typst; typst.compile('ars-artium-oracle.typ', output='ars-artium-oracle.pdf')"
