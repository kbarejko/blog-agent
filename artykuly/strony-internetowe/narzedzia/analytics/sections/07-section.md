## Od danych do decyzji: dashboardy, rytm pracy i eksperymenty

Masz już wiarygodne sygnały. Teraz potrzebny jest rytm, który zamienia je w decyzje. Zacznij od trzech warstw dashboardów. Executive to jedna strona z North Star i 5–7 wskaźnikami wspierającymi (przychód/marża, LTV:CAC, retencja, cash payback). Growth/Performance schodzi poziom niżej: koszt i wartość per kanał, ROAS/POAS, lejki i drop‑offy, jakość leadów z CRM. Produkt/UX pokazuje aktywację, retencję cohort, ścieżki, szybkość strony i bariery w formularzach.

Kilka zasad porządkowych. Jedno źródło prawdy na każdy KPI (np. przychód z ERP/BI, nie z GA4). Każda karta pokazuje trend, odchylenie od celu i limit (guardrail). Widzisz: wartość, delta vs poprzedni okres i próg alarmu. Bez kontekstu liczby mylą.

Looker Studio wystarczy na start. Przyspiesz pracę szablonami i kontrolą wersji: kopiuj raporty, opisuj zmiany w changelogu, trzymaj definicje metryk w repo jako dokumentację. Dodaj alerty e‑mail/Slack (np. CVR spada o 20% d/d, błędy 5xx > 1%). Dla analiz ad‑hoc używaj GA4 Explorations lub BI.

Ustal rytm spotkań. Cotygodniowy przegląd KPI (30–45 min): czytamy delty, decydujemy o działaniach. Raz w miesiącu deep‑dive: jedna teza, jedno źródło problemu, jeden plan. Kwartalnie rewizja celów i budżetów. Każda decyzja trafia do decision logu: hipoteza → wynik → decyzja → efekt, z datą i właścicielem.

Backlog analityczny też potrzebuje procesu. Priorytetyzuj ICE/PIE (impact, confidence, effort), przydziel właścicieli i SLA. Hipotezy opieraj na insightach, określ minimalny efekt istotny (MDE) i czas trwania testu. Guardrail metrics (CVR, AOV, churn, czas ładowania) chronią przed „wygranymi”, które psują biznes gdzie indziej. Zawsze segmentuj: nowi vs powracający, urządzenie, źródło/medium, region. Sanity checks: czy ruch, CVR i przychód zmieniają się spójnie.

Do eksperymentów: Optimizely, VWO, GrowthBook/Eppo, feature flags (LaunchDarkly, Flagsmith). W aplikacjach mobilnych – Firebase A/B Testing. Jeśli nie testujesz jeszcze A/B, zacznij od zmian quasi‑eksperymentalnych i kontroli w regionach.

Szybkie wygrane:
- przyspieszenie strony (Core Web Vitals),
- klarowniejsze CTA i hierarchia nagłówków,
- skrócenie formularzy i lepsze komunikaty błędów.

Unikaj anty‑wzorów: mierzenia wszystkiego, KPI bez właściciela, raportów bez decyzji.

Ramy 30‑60‑90 dni. 30: porządek definicji, MVP dashboardów, alerty. 60: decyzje tygodniowe, backlog hipotez, pierwsze testy. 90: pełny rytm eksperymentów, value‑based decyzje o budżecie. I najważniejsze pytania na koniec każdego przeglądu: jakie decyzje podejmiemy jutro na bazie tego dashboardu? Które hipotezy zasługują na test w tym kwartale?