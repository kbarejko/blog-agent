## Case study: transformacja problematycznego flow

Zespół e-commerce zauważył dziwną anomalię. Ich nowy checkout przechodził wszystkie testy automatyczne. Zero błędów technicznych, walidacja działała perfekcyjnie, integracja z płatnościami bez zarzutu. Ale conversion rate spadł o 23%.

Analytics pokazywał, że użytkownicy porzucają koszyki na ostatnim etapie – stronie podsumowania zamówienia. Tam, gdzie technicznie wszystko było OK.

### Identyfikacja problemu w standardowym testing flow

Tradycyjne testy QA sprawdziły każdy scenariusz. Happy path: użytkownik wypełnia dane, wybiera dostawę, płaci – działa. Edge cases: nieprawidłowy kod pocztowy, nieaktywna karta płatnicza – obsłużone poprawnie. Testy obciążeniowe: system wytrzymuje peak traffic.

Ale nikt nie sprawdził, czy strona podsumowania ma sens dla kogoś, kto kupuje prezent o 23:30, jest zmęczony i chce po prostu szybko sfinalizować zamówienie.

Section-by-Section Test ujawnił problem w pierwszych 10 minutach. Sekcja "Podsumowanie zamówienia" wyświetlała 12 różnych pozycji: koszt produktów, rabat, przewidywany podatek, opłata za ekspresową dostawę, ubezpieczenie przesyłki. Matematycznie poprawne, prawnie wymagane. Ale użytkownik widział chaos liczb i nie potrafił odpowiedzieć na podstawowe pytanie: "Ile faktycznie zapłacę?"

### Proces implementacji Section-by-Section testu

Zespół poświęcił jeden dzień na mapowanie sekcji checkout flow z perspektywy trzech personas: młody klient kupujący dla siebie, rodzic zamawiający prezent, starszy użytkownik robiący pierwsze zakupy online.

Każdą sekcję testowali z pytaniem: "Co ta persona próbuje tutaj zrozumieć i czy ma szansę to osiągnąć w 30 sekund?"

Odkryli kolejne problemy. Przycisk "Zatwierdź zamówienie" wyglądał identycznie jak "Wróć do edycji". Informacja o czasie dostawy była schowana pod rozwijalnym menu. Pole na kod rabatowy pojawiało się dopiero po kliknięciu małego linka.

### Wyniki: metryki przed i po zmianach

Po trzech tygodniach implementacji zmian metryki mówiły same za siebie. Conversion rate wrócił do poprzedniego poziomu i wzrósł o dodatkowe 8%. Średni czas spędzony na stronie podsumowania spadł z 2 minut 40 sekund do 45 sekund.

Co ważniejsze – liczba tickets do customer service związanych z "niezrozumiałymi opłatami" spadła o 60%. Klienci przestali dzwonić z pytaniami o "dodatkowe koszty", które i tak były wyświetlone, ale w nieczytelny sposób.