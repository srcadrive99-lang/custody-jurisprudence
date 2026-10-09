# Brief for research agents adding NEW sources (حجة لنا لا علينا)

Corpus: «حول سن الحضانة والرعاية المشتركة بالمناصفة» — an Arabic evidence corpus of verified texts. Thesis: custody of women (hadana) ends at discernment — 7 for a boy, 9 for a girl — then the child goes to the father or to equal shared care; childhood ends at puberty, not at 15; after separation the default is equal shared parenting («الرعاية المشتركة بالمناصفة»); the child's right to both parents (silat al-rahim); father absence harms children; «لا تخيير مع تغييب» (a child's "choice" after years of exclusion of one parent is manufactured).

Golden rule: every source must be «حجة لنا لا علينا» — it must help this thesis and must NOT also contain material that an opponent can quote against it (e.g., judges may extend custody beyond 7/9; mother has priority by default; shared parenting harms children). If a source is double-edged, report it in a separate "rejected" list with the exact undermining text; do not propose it as a card.

The file /home/claude/work/verify/EXISTING_CARDS.tsv lists the cards already in the corpus (card number, section, id, title, author, work, url). Do NOT propose duplicates of these.

For EVERY proposed source you must have actually seen the text on its web page in this session (WebFetch), copied exactly, with a direct link that shows it. Never rely on memory for quotations, numbers, article numbers or case citations. Prefer official/primary pages: court websites, government legal portals, statistics offices, PubMed/journal pages, shamela.ws book pages, archive.org. If the WebFetch tool asks for a permission that is not granted, or a site blocks you, move to another source; do not retry more than once.

Access notes: pubmed.ncbi.nlm.nih.gov returns a bot-check to WebFetch; use OpenAlex (`https://api.openalex.org/works/doi:<doi>` or `https://api.openalex.org/works/pmid:<pmid>`; the abstract is an abstract_inverted_index you must reconstruct in order) plus a second open source (CrossRef, publisher page, university repository, PMC). Wiley/T&F/ScienceDirect/JSTOR often block; search the exact title to find an open copy (repository PDFs, author pages).

Tools: WebFetch, WebSearch, Read, Write, Bash only. Do NOT use browser tools (mcp__claude-in-chrome__*, mcp__remote-devices__*).

Arabic style for anything you write in Arabic: plain modern Arabic, no tashkeel, Latin digits (7, 9, 2013), no jargon (never: أتراب، طولية، مقطعية، بعدي، الأرجحية، إكلينيكي، نمائي، الوالدية), antecedent of a pronoun in square brackets when needed «[الأب]». «الرعاية المشتركة بالمناصفة» only when the source means equal or near-equal time; joint legal custody → «الولاية المشتركة»; co-parenting → «تعاون الوالدين».

Output: write a JSON array to the result path given in your task. One object per proposed source with EXACTLY these keys:
- key: short slug
- category: one of the categories named in your task
- author: authors/court/office exactly as on the source
- year
- title_latin: title of the work/judgment/report in its language (or Arabic title for Arabic sources)
- where: journal/volume/pages, or court + case number + date, or report name + table
- jurisdiction: country/body (Arabic), e.g. "باكستان — المحكمة العليا"
- quote: the exact verbatim text (source language), max ~500 characters, with ellipses allowed
- quote_ar: faithful Arabic translation (for non-Arabic quotes), else ""
- location: article/paragraph/page where the quote sits
- url: direct link that shows the text
- url2: optional second link (official or PDF) or ""
- about: 1–2 Arabic sentences on the standing of the source (who they are, how authoritative)
- level: Arabic evidence level, e.g. "حكم محكمة عليا", "تشريع نافذ", "إحصاء رسمي للدولة", "دراسة سجلات وطنية", "تحليل جامع للدراسات", "نص فقهي معتمد"
- argument: 1–2 Arabic sentences: how this is an argument for the thesis
- double_edged: "" if clean, else the exact undermining text (then also put the source in the rejected list)
Also include at the end of the array one object {"key":"_rejected","items":[{"source":"...","why":"...","text":"..."}]} listing sources you examined and rejected.
Finish with a short summary (what you found, what you rejected, which pages you could not read).
