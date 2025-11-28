## Przegląd i porównanie popularnych rozwiązań: WordPress, Webflow, inne

Przejście od kryteriów decyzyjnych do konkretów: poniżej porównanie narzędzi, które najczęściej pojawiają się w briefach marketingu i product‑ownerów. Skupiam się na rzeczywistych zaletach/ograniczeniach i sygnałach, które pomogą wybrać.

#### Gutenberg (Full Site Editing)
Gutenberg to natywny blokowy edytor WordPressa z rosnącym wsparciem dla Full Site Editing. Zalety: relatywnie lekki output, zgodność ze standardami WP i brak dodatkowego lock‑inu do zewnętrznego pluginu. Dobrze działa, gdy chcecie zachować kontrolę nad strukturą treści i mieć prosty model aktualizacji. Ograniczenia: ekosystem bloków wciąż dojrzewa — niektóre bloki są niedopracowane, a krzywa uczenia dla niestandardowych bloków bywa stroma.

#### Elementor
Elementor to synonim szybkiego prototypowania i ogromnego marketplace’u gotowych widgetów. Dla marketerów to ogromna wygoda: drag‑and‑drop, gotowe sekcje i integracje. Główne minusy to nadmiar CSS/JS generowany przez widgety oraz ryzyko lock‑inu (szablony i shortcody). Przy dużej stronie trzeba liczyć się z pracą optymalizacyjną.

#### Bricks / Oxygen / Beaver Builder / Divi
Te narzędzia różnią się filozofią: Bricks i Oxygen celują w performance‑first — czystszy kod, mniejszy bloat, większe możliwości programistyczne. Divi i Beaver to UX‑first: szybkie tworzenie szablonów, bogate UI, mniejsza krzywa dla non‑dev. Kto powinien czego użyć? Jeśli CWV to KPI — rozważ Bricks/Oxygen. Jeśli priorytetem jest szybkość wdrożeń i duży katalog gotowych modułów — Divi/Beaver.

#### Webflow
Webflow to zintegrowane środowisko: edytor wizualny + hosting + CMS. Generuje schludny kod, daje dobre wyjście pod względem performance i dostępności, oraz prostą obsługę CMS‑ową bez WP. Ograniczenia: koszty rosną z ruchem i funkcjami, backendowe ograniczenia (logika, złożone e‑commerce) i migracje — eksport HTML/CSS jest możliwy, ale przeniesienie CMS i logiki wymaga pracy.

#### Wix Studio / Editor X / Framer Sites
Te platformy są świetne na kampanie, portfolio i microsites — szybkie prototypy, hosting i prostota. Zwykle mniej elastyczne pod kątem integracji z backendem i skalowalności.

#### WooCommerce vs Webflow e‑commerce; scenariusze headless
WooCommerce + builder sprawdzi się dla sklepów z szerokim katalogiem i niestandardową logiką. Webflow e‑commerce działa dobrze przy mniejszym asortymencie i prostych procesach sprzedaży. Headless ma sens, gdy potrzebujesz skalowalnego API, wielokanałowej publikacji lub gdy planujesz migrację frontu bez rezygnacji z istniejącego CMS.

Licencje i migracje
Plany kosztowe na 12–36 miesięcy muszą uwzględniać licencje, hosting, CDN i potencjalne opłaty za zwiększony ruch. Szukaj „light” motywów i bibliotek komponentów zgodnych z identyfikacją — skrócą wdrożenie i ułatwią migrację. Eksport/import bywa prosty (statyczny HTML/CSS) lub złożony (CMS, relacje, SEO). Przy planowaniu uwzględnij koszt migracji treści i mapowanie URL.