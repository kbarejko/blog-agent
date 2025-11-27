## Migracja i wdrożenie: plan 4–6 tygodni bez bólu

Masz już bibliotekę treści i szablony — czas bezboleśnie przenieść wszystko do nowej platformy. Plan 4–6 tygodni to realne ramy, jeśli robisz to etapami i nie pomijasz kontroli jakości.

Tydzień 1 — inwentaryzacja i priorytety
- Zrób pełny eksport treści: lista URL, typy stron, wolumen mediów, meta. Wykorzystaj crawlery (Screaming Frog) i analytics, żeby wyłowić top 20% stron generujących 80% ruchu. To one wymagają największej uwagi przy zachowaniu SEO.

Tydzień 2 — struktura kolekcji i makiety
- Na podstawie mapy treści zaprojektuj kolekcje i taksonomię w narzędziu docelowym. Zdecyduj, które pola będą wymagane (slug, meta, language, canonical). Równolegle przygotuj low‑fi makiety stron kluczowych: homepage, oferta, case study, szablon bloga — sprawdź działanie komponentów dynamicznych.

Tydzień 3 — wymagania prawne i tracking; ustawienia domeny
- Skonfiguruj polityki prywatności, cookie consent i DPA oraz umieść mechanizm blokowania trackerów do czasu zgody. Wdróż GA4, Facebook Pixel i inne integracje w środowisku staging. Przygotuj rekordy DNS, SSL i role użytkowników (editor, publisher, admin).

Tydzień 4 — importy, media i przekierowania
- Importuj treści (CSV/JSON/API), przypnij media i napraw ścieżki obrazów. Rygorystycznie testuj mapę przekierowań 301: każdy stary URL musi kierować na nowy. Ustaw canonicale tam, gdzie struktura się zmienia. Zaktualizuj linki wewnętrzne w treściach i menu.

Tydzień 5 — optymalizacja i QA
- Testy prędkości i Core Web Vitals: lazy‑load obrazów, next‑gen formats (WebP/AVIF), preconnect i minimalizacja JS. Przeprowadź QA: mobile, dostępność (WCAG), formularze, integracje z CRM, testy formularzy oraz procesy leadów.

Tydzień 6 — publikacja i monitoring
- Wybierz okno wdrożeniowe przy niskim ruchu, wprowadź content freeze, opublikuj i natychmiast monitoruj: uptime, błędy 404, Search Console (crawl errors) i crawl budget. Miej gotowy rollback i plan backupów.

Procesy edycyjne i ryzyka
- Wprowadź wersjonowanie, workflow zatwierdzania i harmonogram publikacji. Najczęstsze błędy: brak przekierowań (utrata ruchu), duplikacja treści bez canonical, nieprzydzielone role i brak backupów — to rodzi chaos w kolekcjach. Minimalizujesz ryzyko, testując eksport/import na próbce i trzymając checklistę przed publikacją.