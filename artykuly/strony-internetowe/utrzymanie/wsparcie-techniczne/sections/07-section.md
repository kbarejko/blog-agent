## Jak wybrać dostawcę wsparcia technicznego i przygotować onboarding

Po ustaleniu, co musi działać bez przerwy i jak reagować przy awarii, pora wybrać partnera, który to wszystko dostarczy. Zacznij od dopasowania doświadczenia technicznego do Twojego stacku — nie pytaj ogólnikowo „znacie WordPressa?”, poproś o konkretne case’y z WooCommerce, Shopify, headless (React/Vue + API) lub systemami custom. Ważne: porównaj skale — czy partner ogarnia sklep z 10 tysięcy zapytań/dzień, czy tylko małe strony.

Sprawdź skład i dyspozycyjność zespołu. Idealny dostawca ma rotację on‑call, dokumentowane SLAs dyspozycyjności (24/7, strefy czasowe pokryte), oraz profilowane role: SRE/DevOps, backend dev, security engineer. Zapytaj o czas reakcji na P1 (np. acknowledgment <30 min) i dostępność zasobów w czasie kampanii.

Referencje i transparentność narzędzi to nie opcja — to wymóg. Proś o case studies i dostęp do przykładowych dashboardów (Grafana, StatusPage) oraz sposobu raportowania (Jira, Datadog). Transparentny partner daje dostęp do changelogów, ticketów i miesięcznych raportów.

Kwestie prawne muszą być domknięte przed przekazywaniem dostępu: NDA, DPA/umowa powierzenia danych, zapisy o własności kodu i warunkach przekazania repo. Zasada: klient zachowuje prawa do kodu; dostawca otrzymuje jedynie niezbędne role (deploy keys, scoped IAM) i obowiązek rotacji kluczy.

Onboarding zaczyna się od audytu technicznego: inwentaryzacja zasobów, diagramy architektury, lista dostępów, analiza CI/CD, pipeline’ów i polityki release’ów. Oczekuj raportu z ryzykami i planem 30/90 dni: naprawy krytyczne, stabilizacja, optymalizacje.

Ustalcie SLA i matrycę priorytetów, kontakty i ścieżki eskalacji — kto jest escalation ownerem poza on‑call. KPI do monitorowania: MTTR, MTTD, First Contact Resolution, pokrycie SLA (%), liczba incydentów oraz trend ich powtarzalności. Umów health score aplikacji (wartości składowe: uptime, LCP, 5xx rate, krytyczne security findings) i miesięczne rekomendacje.

OKR‑y utrzymaniowe stawiaj mierzalnie: np. zmniejszyć MTTR P1 o 50% w 90 dni, zmniejszyć 5xx o 30%. Przy przejmowaniu wsparcia wymaga się checklisty transferowej: pełny eksport repo, lista kont, runbooki, backupy, shadowing dotychczasowego dostawcy i test restore przed cut‑over.

Co otrzymasz co miesiąc: SLA report, changelog release’ów, lista incydentów z post‑mortem, health score i backlog rekomendacji. Na „exit” wymuś prawo do pełnego eksportu kodu, dokumentacji, backupów i przekazania kluczy oraz finalnego handoveru zgodnie z umową.