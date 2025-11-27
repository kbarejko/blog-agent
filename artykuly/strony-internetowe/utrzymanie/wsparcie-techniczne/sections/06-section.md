## Wsparcie techniczne dla e‑commerce i systemów krytycznych

Po optymalizacji wydajności przechodzimy do obszaru, gdzie błędy kosztują bezpośrednio przychód: e‑commerce i systemy krytyczne. Tu każde opóźnienie musi mieć z góry ustaloną procedurę i właściciela.

Uptime i okna serwisowe powinny być planowane poza szczytem ruchu. Okno maintenance to nie jest czas na eksperymenty — komunikacja i status page to obowiązek. Mechanizm trybu maintenance powinien przełączać serwis w tryb informacyjny lub read‑only, by nie tracić transakcji.

Ciągłość transakcji wymaga redundancji integracji z bramkami płatności i warstwą anti‑fraud. Miej zawsze fallback gateway i politykę retry dla tymczasowych błędów. Monitoruj stawki autoryzacji (decline rate) i ustaw alerty — np. spadek autoryzacji o >2 pkt proc. w odniesieniu do baseline → natychmiastowa eskalacja.

Monitorowanie koszyka i checkoutu to codzienność. Śledź porzucone koszyki, błędy w walidacji i spike 5xx na endpointach checkoutu. Kluczowe metryki: abandonment rate, checkout error rate, średni czas transakcji. Szybka korelacja logów i Sentry pomaga znaleźć przyczynę.

Integracje z ERP, WMS, CRM, marketplace’ami i feedami produktowymi trzeba traktować jak krytyczne. Webhooki i feedy powinny mieć retry, dead‑letter queue i monitoring latencji. Błąd w feedzie potrafi ukryć produkty i zabić sprzedaż.

Sandboxy i testy end‑to‑end są niezbędne. Testuj płatności, refundy i scenariusze 3DS w środowisku testowym po każdej zmianie. Automatyczne E2E w pipeline minimalizują ryzyko regresji trafiającej na produkcję.

Przed kampaniami robimy testy regresji i load testy. Symuluj peak, sprawdź limity bramek i API partnerów. Pre‑warming CDN, podniesienie limitów kolejek i rezerwacja instancji to standard checklisty pre‑kampanijnej.

Plany pojemności obejmują rate‑limit, kolejki (SQS, RabbitMQ) i strategie degradacji gracji — czyli stopniowe wyłączanie funkcji niekrytycznych, by obsłużyć checkout. Ustal progi eskalacyjne i automatyczne przełączenia.

Runbook incydentów sprzedażowych musi być gotowy: detekcja → fallback gateway → rollback/feature‑flag → komunikacja → post‑mortem. Rollback plan i code‑freeze przed i w trakcie kampanii (48–72 h) minimalizują ryzyko.

Spadki autoryzacji i błędy API operatorów to najczęstsze awarie zewnętrzne. Mierz MTTR dla transakcji i odzyskiwania koszyków; celuj w jak najkrótsze czasy (często <1–2 h dla krytycznych problemów), bo każda godzina przestoju to realna strata przychodu.