## Konfiguracja domeny i hostingu

Po przygotowaniu technicznym przychodzi czas na połączenie wszystkich elementów infrastruktury. To moment, w którym twoja strona przestaje być projektem deweloperskim, a staje się rzeczywistością dostępną dla użytkowników.

Proces połączenia domeny z serwerem zaczyna się od panelu zarządzania domeną. Większość firm hostingowych udostępnia szczegółowe instrukcje, ale podstawy pozostają takie same: musisz wskazać domenie, na którym serwerze znajdą się pliki twojej strony.

### Ustawienie rekordów DNS

Rekordy DNS to instrukcje mówiące internetowi, gdzie znajdzie twoją stronę. Rekord A kieruje domenę na adres IP serwera – to podstawowy rekord, bez którego nic nie zadziała. Jeśli używasz subdomen (np. blog.twojadomena.pl), potrzebne będą rekordy CNAME.

Rekordy MX dotyczą poczty elektronicznej. Nawet jeśli nie planujesz używać skrzynek na domenie od razu, warto je skonfigurować. Dzięki temu unikniesz problemów z odbieraniem wiadomości od formularzy kontaktowych.

Większość paneli hostingowych oferuje kreatory DNS-ów. Korzystaj z nich, szczególnie jeśli to twoja pierwsza publikacja. Błąd w rekordach może oznaczać kilkugodzinną przerwę w dostępności strony.

### Instalacja certyfikatu SSL i wymuszenie HTTPS

Certyfikat SSL to już nie opcja, ale wymóg. Google penalizuje strony bez szyfrowania, a użytkownicy widzą ostrzeżenia o braku bezpieczeństwa. Większość hostingów oferuje darmowe certyfikaty Let's Encrypt.

Po instalacji certyfikatu ważne jest wymuszenie przekierowań z HTTP na HTTPS. Bez tego część ruchu może trafiać na nieszyfrowaną wersję strony. Skonfiguruj przekierowania na poziomie serwera lub w pliku .htaccess.

Sprawdzenie propagacji DNS na świecie potrwa od 15 minut do 48 godzin. Narzędzia jak DNS Checker pokazują, czy zmiany dotarły już do serwerów na różnych kontynentach. Nie panikuj, jeśli w niektórych lokalizacjach strona jeszcze nie działa.

Najczęstsze problemy to źle skonfigurowane rekordy NS (name server) i konflikt między starymi a nowymi ustawieniami DNS. Jeśli po 6 godzinach strona nadal nie działa, sprawdź konfigurację od początku. Często błąd kryje się w literówce w adresie IP lub nazwie serwera.