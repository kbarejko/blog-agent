Najpopularniejsze ataki na sklepy internetowe to SQL injection i Cross-Site Scripting (XSS). WAF rozpoznaje te wzorce i blokuje je automatycznie. Próba wstrzyknięcia kodu `'; DROP TABLE users; --` do formularza zostanie zatrzymana na poziomie firewalla, zanim dotrze do bazy danych.

Konfiguracja wymaga znajomości swojego sklepu. Jeśli sprzedajesz tylko w Polsce, możesz zablokować ruch z krajów wysokiego ryzyka. Ale uwaga na VPN-y i proxy - legitymni klienci też ich używają. Lepiej monitorować niż ślepo blokować.

CloudFlare oferuje WAF w przystępnej cenie. Podstawowa ochrona kosztuje 20 dolarów miesięcznie i obejmuje większość sklepów. AWS WAF jest potężniejszy, ale wymaga więcej konfiguracji. Wybór zależy od budżetu i kompetencji zespołu.

## Kopie zapasowe i plan odzyskiwania

Najlepsze zabezpieczenia czasem zawodzą. Hakerzy wymyślają nowe techniki, zero-day exploity omijają wszystkie filtry, ludzie popełniają błędy. Kiedy wszystko inne zawiedzie, kopie zapasowe są ostatnią deską ratunku.

### Strategia backupów dla e-commerce

#### Rodzaje kopii zapasowych

Pełne backup-y to kompletna kopia wszystkich danych. Bezpieczne, ale czasochłonne i zajmują dużo miejsca. Sklep z 50 GB danych potrzebuje 50 GB na każdą kopię. Tygodniowe pełne backupy to rozsądny kompromis dla większości biznesów.

Kopie przyrostowe zapisują tylko zmiany od ostatniego backup-u. Znacznie szybsze i mniejsze, ale przywracanie wymaga całego łańcucha kopii. Jedna uszkodzona kopia może zepsuć cały proces.

Kopie różnicowe to środek między pełnymi a przyrostowymi. Zapisują wszystkie zmiany od ostatniej pełnej kopii. Przywracanie wymaga tylko dwóch plików: ostatniego pełnego backup-u i najnowszej kopii różnicowej.

Częstotliwość zależy od dynamiki sklepu. Dziesiątki zamówień dziennie oznaczają, że strata nawet kilku godzin danych to poważny problem. Automatyczne kopie co 6 godzin to minimum. Bazy danych można backup-ować częściej niż pliki - zmieniają się rzadziej.

Geograficzne rozproszenie chroni przed katastrofami. Pożar w serwerowni, powódź, awaria dysku - kopie w tym samym miejscu też przepadną. Cloud storage jak AWS S3 czy Google Drive automatycznie replikuje dane między kontynentami.