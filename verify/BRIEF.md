# Verification brief (source-matching pass)

You are verifying entries of an Arabic evidence corpus («حول سن الحضانة والرعاية المشتركة بالمناصفة»). Each entry in your batch file is a JSON object with: id, title (Arabic), author, work (title/section/page), notes, jurisdiction, original {lang, text, verbatim}, translation_ar, urls, links, about.

Thesis the corpus supports (so you can judge relevance and flag problems): custody of women (hadana) ends when the child reaches discernment — 7 years for a boy, 9 for a girl — and the child then goes to the father (or to equal shared care); childhood ends at puberty, not at 15; after separation of the parents the default is equal shared parenting (الرعاية المشتركة بالمناصفة); the child's right to both parents (silat al-rahim); father absence harms children.

## Your job, for EVERY entry in the batch
1. Open the entry's URL(s) with WebFetch. If the page is unreachable/blocked/asks for permission, do NOT retry the same URL more than once; find the same text on another authoritative site with WebSearch + WebFetch.
2. Decide:
   - If `original.verbatim` is true: does the quoted text appear in the source EXACTLY (same words, same order)? Minor orthographic differences (hamza, tashkeel, punctuation) are fine for Arabic; report any word-level difference. Note that the WebFetch tool may refuse to quote more than ~125 characters at a time — so ask it targeted questions ("does this exact sentence appear? which words differ?") rather than asking it to dump the page.
   - If `original.text` starts with «مضمونه:» (a gist): does the source support the gist accurately (numbers, ages, claims)? Then extract from the source (abstract, full text, statute article) the single best VERBATIM sentence or two (max ~450 characters, in the source language) that supports the gist, with its exact location (page/article/paragraph). Do not paraphrase; copy exactly. If you cannot get exact wording, say so and leave found_text empty.
3. Find the best DIRECT link that shows the text (official site: legifrance.gouv.fr, gesetze-im-internet.de, planalto.gov.br, infoleg.gob.ar, wetten.overheid.nl, fedlex.admin.ch, boe.es, pgdlisboa.pt / dre.pt, arkleg.state.ar.us, moj.go.jp, ohchr.org, au.int; pubmed.ncbi.nlm.nih.gov, doi.org, publisher pages; sunnah.com and dorar.net for hadith; shamela.ws book pages (https://shamela.ws/book/<book-id>/<page>) or islamweb.net library for fiqh books; archive.org / Google Books for other books). Report the link status.
4. Flag DOUBLE-EDGED content: if the same article/passage/abstract also contains something that undermines the thesis (e.g., a judge may extend custody beyond 7/9; a presumption against shared parenting; a finding that shared parenting harms children; a law giving the mother priority), copy that exact text into `double_edged`. We need to know this to decide whether to keep the entry.

## Rules
- Never invent text, page numbers, or links. If you could not verify, say `unreachable` or `not_found`.
- Use ONLY WebFetch, WebSearch, Read, Write, Bash (for writing the result file). Do NOT use any browser tools (mcp__claude-in-chrome__*, mcp__remote-devices__*): they belong to another process.
- Arabic you write (proposed_ar): plain modern Arabic, no tashkeel, Latin digits (7, 9, 2013), no jargon (do not use أتراب، طولية، مقطعية، بعدي، الأرجحية، إكلينيكي، نمائي، الوالدية); put the antecedent of a pronoun in square brackets when needed, e.g. «[الأب]». Translate meaning faithfully; "shared parenting / joint physical custody / equal time" → «الرعاية المشتركة بالمناصفة» only when the source means equal or near-equal time; "joint legal custody / co-parenting" → «الولاية المشتركة» / «تعاون الوالدين» (by their own meaning).
- Work entry by entry; do not skip. If an entry's URL is a book page (openlibrary) that cannot show the text, try archive.org full-text search (https://archive.org/advancedsearch.php or https://archive.org/details/<id>?q=...) and Google Books (https://www.google.com/search?tbm=bks&q="exact phrase") to locate the exact wording; a Google Books result page listing the snippet counts as verification if the snippet shows the words.

## Output
Write a JSON array to the result path given in your task, one object per entry, with EXACTLY these keys:
- id
- status: one of "verified_verbatim" (exact text confirmed), "verified_gist" (gist supported; found_text holds the verbatim support), "corrected" (text found but differs; found_text holds the correct wording), "mismatch" (source contradicts the entry), "unreachable", "not_found"
- found_text: exact text from the source (source language), or ""
- location: where exactly (article/section/page/paragraph), or ""
- source_url: best direct URL showing the text (official if possible), or ""
- url_status: "ok" | "dead" | "redirect" | "blocked" | "unknown" (for the entry's ORIGINAL url)
- proposed_ar: Arabic translation of found_text if found_text is not Arabic, else ""
- double_edged: exact text of any undermining passage nearby, else ""
- notes: short remarks (discrepancies, grade of hadith, edition)

Keep going until every entry has an object. Then reply with a 10-line summary (counts per status, and the ids that need my attention).
