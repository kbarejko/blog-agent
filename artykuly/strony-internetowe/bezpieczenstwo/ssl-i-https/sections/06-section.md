## Implementacja SSL w firmie - praktyczny plan działania

Przejście z teorii do praktyki wymaga systematycznego podejścia. Chaotyczna migracja na HTTPS może kosztować więcej niż cyberattaki, które SSL miał powstrzymać. Plan działania oszczędzi ci bezsennych nocy i wściekłych klientów.

### Audit obecnego stanu zabezpieczeń

Zacznij od inwentaryzacji wszystkich domen i subdomen. Firmy często zapominają o staging.domena.pl, api.domena.pl czy starych mikrosiętach dla kampanii. Narzędzie Sublist3r znajdzie subdomeny, o których istnieniu nie pamiętasz. Certificate Transparency logs pokażą wszystkie certyfikaty wystawione dla twojej domeny w ostatnich latach.

Kolejny krok to identyfikacja mixed content - sytuacji, gdy strona HTTPS ładuje zasoby przez HTTP. Sprawdź obrazki, skrypty, arkusze stylów, API zewnętrzne. Nawet jeden zasób HTTP sprawi, że przeglądarka usunie zieloną kłódkę. Chrome DevTools w zakładce Security wyświetli wszystkie problemy mixed content na konkretnej stronie.

Stwórz arkusz z datami wygaśnięcia wszystkich certyfikatów. Certyfikaty Let's Encrypt wygasają co 90 dni, płatne zazwyczaj po roku lub dwóch. Firma logistyczna, którą obsługiwałem, straciła 200 tysięcy złotych obrotów, bo certyfikat wygasł w weekend, a sklep przestał działać. Excel z alertami to minimum, lepiej zautomatyzować monitoring.

### Proces migracji krok po kroku

Backup to nie opcja, a konieczność. Pełna kopia bazy danych, plików i konfiguracji serwera musi być gotowa przed pierwszym krokiem migracji. Plan awaryjny opisuje, jak w 30 minut wrócić do poprzedniej konfiguracji. Jeden klient z e-commerce miał 6-godzinną awarię, bo backup był uszkodzony.

Przekierowania 301 zachowują pozycje w Google, ale muszą być precyzyjne. Każdy URL http://domena.pl/strona przekieruj na https://domena.pl/strona. Sprawdź canonical URLs, sitemap.xml i robots.txt - wszystkie muszą wskazywać na HTTPS. Google Search Console pozwoli dodać nową właściwość HTTPS i monitorować proces indeksowania.

Aktualizacja internal linków to żmudna robota, ale kluczowa dla wydajności. Każde przekierowanie 301 spowalnia ładowanie o 100-200 milisekund. Narzędzia jak Screaming Frog przeskanują witrynę i wskażą wszystkie linki wymagające zmiany. W dużych systemach pomogą skrypty automatyczne zamiany w bazie danych.

### Zarządzanie certyfikatami w długim terminie

Automatyczne odnawianie eliminuje ludzkie błędy. Let's Encrypt Certbot odnawia certyfikaty co 60 dni. Płatne certyfikaty wymagają integracji z API dostawcy lub przynajmniej alertów 30 dni przed wygaśnięciem. Klient z 50 domenami oszczędził 10 godzin miesięcznej pracy dzięki automatyzacji.

Większe organizacje potrzebują centralnego zarządzania. Narzędzia jak HashiCorp Vault lub AWS Certificate Manager pozwalają kontrolować setki certyfikatów z jednego miejsca. Alert trafia do zespołu IT, nie do prezesa na wakacjach w Tajlandii.