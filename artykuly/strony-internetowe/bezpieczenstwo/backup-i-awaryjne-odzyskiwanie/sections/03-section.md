## Rodzaje backup i kiedy każdy z nich stosować

Znasz już swoje dane i wiesz, co chronisz. Teraz czas wybrać metodę. To jak planowanie trasy - możesz jechać autostradą (szybko, ale drogo) lub drogami lokalnymi (wolniej, za to oszczędnie).

### Backup pełny, przyrostowy i różnicowy

Backup pełny kopiuje wszystkie dane za każdym razem. To najprościej, ale i najwolniej. Pełny backup 500 GB może zająć 6 godzin i wypełnić całe okno nocne. Zaleta? Przywracanie z jednej kopii, bez kombinowania z kolejnymi częściami.

Backup przyrostowy kopiuje tylko zmiany od ostatniego backup (nieważne jakiego). W poniedziałek pełny, we wtorek tylko 5 GB zmian, w środę kolejne 3 GB. Oszczędza czas i miejsce, ale przywracanie wymaga pełnej kopii plus wszystkich przyrostowych. Jeden uszkodzony element i tracisz dostęp do danych z całego tygodnia.

Backup różnicowy kopiuje zmiany od ostatniego pełnego backup. We wtorek 5 GB, w środę już 8 GB (5+3 nowe), w czwartek 12 GB. Zajmuje więcej miejsca niż przyrostowy, ale przywracanie wymaga tylko dwóch elementów: pełnego backup i ostatniego różnicowego.

Dla małych firm sprawdza się model: pełny w weekend, różnicowy codziennie. Średnie firmy często wybierają pełny w niedzielę, przyrostowy w tygodniu, różnicowy w piątek. Duże organizacje? Kombinują wszystkie typy w złożonych harmonogramach.

### Strategia 3-2-1: złoty standard bezpieczeństwa

Zasada brzmi prosto: 3 kopie danych, 2 różne technologie, 1 kopia offline lub zdalnie. Brzmi skomplikowanie? W praktyce to może być: dane robocze na serwerze, kopia na dysku zewnętrznym i trzecia w chmurze.

"Różne technologie" oznacza unikanie single point of failure. Nie trzymaj wszystkich kopii na dyskach tego samego producenta czy w tej samej szafie serwerowej. Pożar lub zalanie może zniszczyć obie lokalne kopie jednocześnie.

W małych firmach 3-2-1 wygląda realistycznie: dane na komputerach, backup na NAS w biurze, trzecia kopia w OneDrive. W większych organizacjach: serwery produkcyjne, macierz dyskowa i backup w centrum danych partnera.

Nowoczesne podejście 3-2-1-1-0 dodaje immutable backup - kopię, której nikt nie może zmienić przez określony czas. To ochrona przed ransomware, który próbuje zaszyfrować wszystko, łącznie z kopiami zapasowymi. Ostatnie "0" oznacza zero błędów po weryfikacji - każdy backup musi być przetestowany.