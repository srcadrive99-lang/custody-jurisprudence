# Link-liveness check brief

Your batch file is a JSON array of objects {id, card, title, url, label}. For EVERY url decide whether it is alive and still points to the intended content.

Method (fast, ≤2 requests per link):
- pubmed.ncbi.nlm.nih.gov/<pmid>/ : WebFetch returns a bot-check; instead fetch `https://api.openalex.org/works/pmid:<pmid>` — if a work is returned with a plausible title, mark "ok" and record its title; if OpenAlex says not found, mark "check".
- doi.org/<doi> : fetch `https://api.crossref.org/works/<doi>` (URL-encode the DOI) — if it resolves, mark "ok" and record the title; else try `https://api.openalex.org/works/doi:<doi>`; if both fail, mark "dead".
- shamela.ws, islamweb.net, islamicbook.ws, sunnah.com, dorar.net, archive.org, openlibrary.org, hudoc.echr.coe.int, courtlistener.com, government portals, publishers, everything else: WebFetch the URL once with the prompt "What is the page title and what is it about? Say 'NOT FOUND' if it is an error/404/empty page." Mark "ok" if the page is the intended book/article/judgment (compare with the entry's title), "redirect" if it lands on a different but related page (give the new URL), "dead" for 404/empty, "blocked" if the fetcher was refused (robots/captcha/permission) — do not retry blocked links more than once, and for blocked links try a quick WebSearch of the title to confirm the resource exists (then mark "blocked_exists").
- Do not use browser tools (mcp__claude-in-chrome__*, mcp__remote-devices__*). Only WebFetch, WebSearch, Read, Write, Bash.

Output: write a JSON array to the result path given in your task, one object per link with keys: id, url, status ("ok" | "redirect" | "dead" | "blocked" | "blocked_exists" | "check"), landed_title (string), new_url ("" unless redirect/replacement found), note. Keep going until every link has an object, then reply with counts per status and the list of dead/check links.
