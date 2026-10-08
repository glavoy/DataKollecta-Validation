#!/bin/bash
# Test-environment only: run the three edge functions under a host Deno with an
# import map (esm.sh/deno.land are blocked by this environment's egress policy).
SP=/tmp/claude-0/-home-user/edb0297e-ac00-5503-bb55-9a2245b1a51e/scratchpad
export PATH=$SP/sdk/denonpm/node_modules/.bin:$PATH
cd /home/user/DataKollecta-Web
eval "$($SP/sdk/supabase status -o env 2>/dev/null | grep -E '^(SERVICE_ROLE_KEY)=')"
export SUPABASE_URL=http://127.0.0.1:54321 SUPABASE_SERVICE_ROLE_KEY=$SERVICE_ROLE_KEY
deno --version | head -1
MAP=$SP/fnhost/import_map.json
DENO_SERVE_ADDRESS=tcp:127.0.0.1:8101 deno run --allow-net --allow-env --import-map $MAP supabase/functions/app-login/index.ts &
DENO_SERVE_ADDRESS=tcp:127.0.0.1:8102 deno run --allow-net --allow-env --import-map $MAP supabase/functions/app-sync/index.ts &
DENO_SERVE_ADDRESS=tcp:127.0.0.1:8103 deno run --allow-net --allow-env --import-map $MAP supabase/functions/project-data-feed/index.ts &
deno run --allow-net $SP/fnhost/router.ts &
wait
