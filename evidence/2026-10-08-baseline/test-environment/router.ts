// Test-environment router: forwards /functions/v1/<name> to a host-run function,
// everything else to the local Supabase gateway. Adds x-forwarded-for like the gateway.
const ports: Record<string, number> = { "app-login": 8101, "app-sync": 8102, "project-data-feed": 8103 };
Deno.serve({ port: 54400 }, async (req) => {
  const url = new URL(req.url);
  const m = url.pathname.match(/^\/functions\/v1\/([^/]+)(.*)$/);
  const target = m ? `http://127.0.0.1:${ports[m[1]]}${m[2] || "/"}${url.search}` : `http://127.0.0.1:54321${url.pathname}${url.search}`;
  const headers = new Headers(req.headers);
  if (m && !headers.has("x-forwarded-for")) headers.set("x-forwarded-for", "127.0.0.1");
  return fetch(target, { method: req.method, headers, body: req.body, redirect: "manual" });
});
