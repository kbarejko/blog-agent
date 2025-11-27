### Jak szybko mój sklep może wrócić do działania przy incydencie P1?

Przy incydencie P1 (brak sprzedaży/awaria produkcji) typowe RTO to 2–4 godziny w ramach SLA; zespół najpierw identyfikuje i izoluje przyczynę, uruchamia tryb degradacji i przywraca kluczowe usługi, prawdopodobnie przełączając ruch na zapasowy serwer lub wyłączając moduły.  
Miej kanały eskalacji, backupy i procedury DR, plus regularne testy odtworzeniowe — to zmniejszy straty i pozwoli szybciej informować klientów przez Status Page; praktyczne ćwiczenia, np. symulacja awarii bazy, zwykle skracają czas naprawy.

### Czy wsparcie techniczne obejmuje SEO i działania marketingowe?

Podstawowe wsparcie techniczne zazwyczaj obejmuje SEO techniczne — np. optymalizację nagłówków, mapę strony, poprawę szybkości i usuwanie błędów crawl — oraz drobne poprawki UX, ale nie zastępuje pełnej strategii marketingowej; ta leży po stronie działu marketingu lub zewnętrznej agencji. Można jednak umówić pakiet rozszerzony łączący utrzymanie z pracami SEO i kampaniami (np. content, analityka konwersji), który powinien w umowie precyzować zakres i limity godzin — to wydaje się najlepsze rozwiązanie przy większych projektach.

### Ile zadań mieści standardowy abonament wsparcia?

Liczba zadań zależy od planu — zwykle to pula godzin miesięcznie na utrzymanie, krytyczne poprawki i drobne zmiany, z limitem na większe prace. Dobrze jasno określić SLA, zasady "fair use" i priorytety, bo to może sugerować sposób rozliczania nadmiaru; prosty mechanizm zatwierdzania dodatkowych prac (np. taryfa godzinowa) pomaga uniknąć nieporozumień.

### Jak często robić testy odtworzeniowe kopii zapasowych?

Zaleca się przeprowadzać testy odtworzeniowe co kwartał, przynajmniej dla krytycznych systemów; to najszybszy sposób, by potwierdzić integralność kopii i poprawność procedur przywracania — backupy powinny prawdopodobnie spełniać zasadę 3‑2‑1, być szyfrowane i przechowywane off‑site. Testy warto dokumentować, mierzyć RPO i RTO, wyciągać wnioski z ćwiczeń (np. odtworzenie bazy produkcyjnej na środowisku testowym) i raportować wyniki do właściciela oraz zespołu DR; taka praktyka może sugerować obniżenie ryzyka i szybsze przywracanie usług.

### Jakie metryki monitorować, by widzieć wpływ wsparcia na biznes?

Kluczowe metryki to uptime, MTTR, MTTD, liczba incydentów, Core Web Vitals (LCP, CLS, INP), TTFB oraz konwersje i porzucenia koszyka — łącząc techniczne i biznesowe KPI zobaczysz zwrot z inwestycji. Raporty miesięczne powinny pokazywać trendy, przyczyny i rekomendacje; ustaw progi alertów według sezonowości i ruchu — np. spadek LCP o 400 ms może sugerować optymalizację obrazów, a wydłużony MTTR prawdopodobnie wymaga automatyzacji.

### Jak zabezpieczyć przejęcie wsparcia od poprzedniego dostawcy?

Przy przejęciu wykonaj audit repozytorium, dostępów, backupów, diagramów i CI/CD oraz zapewnij transfer haseł, kluczy, umów z podwykonawcami i dokumentacji incydentów — może sugerować to sporządzenie krótkiej listy kontrolnej. Zawrzyj klauzule exitowe i harmonogram, potwierdź integralność backupów, przeprowadź test przejęcia (np. przywrócenie backupu i uruchomienie krytycznego serwisu) i potwierdź dostępność środowisk przed zakończeniem transferu; wydaje się, że to prawdopodobnie minimalizuje ryzyko.