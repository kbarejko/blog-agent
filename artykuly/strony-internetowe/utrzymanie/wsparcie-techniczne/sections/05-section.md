## Wydajność i doświadczenie użytkownika w ramach wsparcia technicznego

Po zabezpieczeniu i backupach kolejnym priorytetem jest szybkość i stabilność — bo slow = lost. W praktyce monitorujemy Core Web Vitals: LCP (target <2.5s), CLS (<0.1) i INP (wersja FID — cel <200ms). Do tego TTFB (najlepiej <200–500ms), błędy JavaScript i wskaźniki 5xx — one często przekładają się bezpośrednio na spadki konwersji.

Narzędzia to kombo: Lighthouse i WebPageTest dają lab‑metrics i waterfall; GA4 oraz Search Console pokazują field‑data; Sentry i agregowane logi wykrywają JS‑error i regresy; Prometheus/Grafana śledzą TTFB i 5xx. Wsparcie powinno łączyć te źródła — tylko wtedy widzisz pełny obraz.

Performance budget to umowny limit (np. LCP, wagę strony, liczba requestów). Definiujesz budżety i alerty progowe — przykładowo: LCP >2.5s dla >5% użytkowników → alarm; 5xx rate >0.5% → wysoka eskalacja. Alerty ustawiaj według sezonowości: niższe progi w czasie kampanii.

Caching to fundament: edge (CDN), server‑side (reverse proxy), aplikacja (HTTP cache, fragment cache). Dodaj kompresję (gzip/ Brotli), optymalizację obrazów i lazy‑loading mediów. Kluczowe: cache busting przy release’ach i kontrola TTL, by nie zaserwować starych assetów.

Po stronie frontu — minifikacja, code‑splitting i preload krytycznych zasobów przyspieszają render. W back-end: optymalizacja zapytań, indeksy bazy i caching wyników (Redis) redukują TTFB. Mobilna optymalizacja i a11y nie są „miłym dodatkiem” — poprawiają konwersję i obniżają współczynnik odrzuceń.

Skalowanie: auto‑scaling plus rezerwacja zasobów na spodziewane szczyty. W serverless ograniczaj cold starts (keep‑warm). Na kampanie stosuj pre‑warming CDN, read‑only mode dla części serwisów i feature flags do stopniowego rolloutu funkcji.

Testy: load testing (k6, Locust, JMeter) przed kampanią i testy regresji po każdym deployu. Symuluj peak i ścieżki krytyczne (checkout, API płatnicze). Po deployu uruchom smoke tests i sanity checks.

Szybkie zwycięstwa, które podniosą konwersję w 2 tygodnie: CDN + cache, optymalizacja głównych obrazów (webp, responsive), usunięcie render‑blocking JS, naprawa krytycznych błędów JS na ścieżkach zakupowych oraz skrócenie TTFB przez cachowanie i indeksy DB. Ustal progi alertów zgodne z ruchem: LCP alert (>2.5s dla 5%), 5xx alert (>0.5% sesji), JS‑error spike (>1% requestów) — i dopasuj je do sezonowości.