#!/usr/bin/env bash
set -euo pipefail
MAB_ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$MAB_ROOT"
export WRANGLER_CACHE_DIR=/tmp/mab-wrangler-cache
export WRANGLER_LOG_PATH=/tmp/mab-wrangler-prod.log
MAB_RELEASE=$(mktemp -d /tmp/mab-production-XXXXXX)
git archive --output="$MAB_RELEASE/source.tar" HEAD
mkdir "$MAB_RELEASE/source"
tar -xf "$MAB_RELEASE/source.tar" -C "$MAB_RELEASE/source"
python3 "$MAB_RELEASE/source/tools/build-production.py" --output "$MAB_RELEASE/site"
test -s "$MAB_RELEASE/site/index.html"
test -s "$MAB_RELEASE/site/contact.js"
npx wrangler pages project list --json > "$MAB_RELEASE/projects.json"
if ! python3 - "$MAB_RELEASE/projects.json" <<'PY'
import json, sys
projects = json.load(open(sys.argv[1]))
sys.exit(0 if any(p.get('Project Name') == 'mab-produccion' for p in projects) else 1)
PY
then
  npx wrangler pages project create mab-produccion --production-branch main
fi
npx wrangler pages deploy "$MAB_RELEASE/site" --project-name=mab-produccion --branch=main
