## Stos narzędzi i architektura: od GA4 po BI i server-side tagging

Skoro masz plan pomiaru i taksonomię, pora na narzędzia. GA4 to domyślny silnik web analytics: elastyczny model zdarzeń, darmowy export do BigQuery i gotowe integracje z reklamami. Gdy wymagana jest ścisła kontrola nad danymi (np. sektor publiczny, podwyższone ryzyka RODO) sens mają Piwik PRO lub Matomo – w wersji cloud lub on‑prem. Trade‑off: słabszy ekosystem reklamowy i więcej pracy przy integracjach.

Tag manager to centrum dowodzenia. Google Tag Manager daje modularność, wersjonowanie i QA. Alternatywy (Piwik PRO TM, Tealium, Adobe Launch) sprawdzają się w większych organizacjach, ale podnoszą koszty i próg wejścia. Zasada: jak najmniej tagów po stronie przeglądarki, jak najwięcej logiki po stronie serwera.

Dlaczego server‑side? Mniej JS = szybsza strona, trwalsza identyfikacja first‑party i pełniejsza kontrola, co wysyłasz do vendorów. Architektura najprostsza do startu: GTM Server na subdomenie (np. sgtm.twojadomena.pl) pod reverse proxy. Przeglądarka wysyła jedno zdarzenie do serwera, a tam mapujesz je na cele: GA4, Google Ads, Meta CAPI, LinkedIn, TikTok. Kluczowe są deduplikacja i spójność ID: event_id oraz stabilny transaction_id/lead_id pochodzący z backendu.

Raportowanie. Looker Studio wystarczy na szybkie dashboardy, ale do analizy operacyjnej wygodne są Metabase (szybkie zapytania) lub Power BI (model danych, uprawnienia). Export GA4 do BigQuery daje surowe hity, które łączysz z CRM/ERP: marża, zwroty, statusy leadów. To tu liczysz LTV, LTV:CAC i budujesz segmenty pod value‑based bidding. Koszty GCP przy ruchu MŚP są zazwyczaj niskie, o ile pilnujesz retencji i partiacji danych.

Lejki produktowe i retencja? Mixpanel lub Amplitude wygrywają na szybkości cohort i ad‑hocowych zapytań, zwłaszcza w aplikacjach/SaaS. UX‑owe „oko w ekran” zapewni Hotjar albo Microsoft Clarity – używaj z próbkowaniem (np. 5–10%), maskuj pola wrażliwe i odpalaj dopiero po zgodzie.

Wymogi prawne i praktyka: CMP z prawidłową integracją (Consent Mode v2), minimalizacja danych, audyt tagów. Piwik PRO/Matomo on‑prem pomaga, gdy nie chcesz transferów poza EOG, ale nie zwalnia z obowiązków.

Minimalny stack MŚP:
- GA4 + GTM (web), CMP, Looker Studio, Hotjar/Clarity. Opcjonalnie BigQuery.

Rozszerzony dla scale‑upu:
- GTM Server + proxy, BigQuery + BI (Power BI/Metabase), Mixpanel/Amplitude, pełne integracje Ads/Meta/LinkedIn/TikTok (EC/CAPI), pipeline do CRM.

Zacznij od MVP: 20% kluczowych eventów (purchase/qualified_lead, add_to_cart/begin_checkout, form_submit), Primary conversions z wartością i poprawną deduplikacją. Dokumentuj zmiany w changelogu, wersjonuj tagi, testuj najpierw na stagingu, a dopiero potem na produkcji.