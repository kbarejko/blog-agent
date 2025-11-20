## DNS i domeny - Płynne przekierowanie ruchu

Po przeniesieniu plików przychodzi moment, który budzi największe emocje - przekierowanie ruchu na nowy serwer. To jak przeprowadzka całej firmy z zachowaniem ciągłości działania.

### Zmiana serwerów DNS

Przygotowanie nowych rekordów DNS rozpocznij na kilka dni przed migracją. Zaloguj się do panelu zarządzania domeną i przygotuj wpisy A, które będą wskazywać na nowy adres IP serwera. Nie publikuj ich jeszcze - tylko przygotuj.

Kluczowy krok, o którym wielu zapomina: obniż TTL (Time To Live) dla wszystkich rekordów DNS do minimum, najlepiej 300 sekund. Rób to 24-48 godzin przed migracją. Dzięki temu zmiany będą propagować się znacznie szybciej, gdy nadejdzie właściwy moment.

Gdy wszystko jest gotowe na nowym serwerze, wprowadź nowe rekordy DNS. Nie rób tego wszystkich naraz. Zacznij od subdomen testowych, potem główna domena. Jeśli masz kilka domen wskazujących na tę samą stronę, zmieniaj je stopniowo z odstępem kilku godzin.

Monitorowanie propagacji to prawdziwa sztuka cierpliwości. Użyj narzędzi takich jak whatsmydns.net czy dig, żeby sprawdzać postęp zmian na różnych serwerach DNS na świecie. Proces może trwać od kilku minut do 48 godzin, choć zwykle kończy się w ciągu 4-6 godzin.

W tym czasie będziesz obserwować ruch rozdzielający się między starym a nowym serwerem. To normalne i przewidywalne.

### Zarządzanie subdomenami i przekierowaniami

Przekierowania 301 to Twoja polisa ubezpieczeniowa na wypadek zmian w strukturze URL-i. Skonfiguruj je na nowym serwerze jeszcze przed zmianą DNS. Jeśli zmieniasz strukturę folderów lub nazwy stron, każdy stary adres musi mieć swoje przekierowanie.

Subdomeny często są zapomnianym elementem migracji. Blog na blog.twojadomena.pl, sklep na sklep.twojadomena.pl czy panel klienta - każda wymaga osobnej konfiguracji DNS i może potrzebować oddzielnej migracji.

Sprawdź działanie poczty elektronicznej już pierwszego dnia po zmianie DNS. Rekordy MX często pozostają bez zmian, ale czasem hosting oferuje zintegrowaną pocztę, która również wymaga aktualizacji. Przetestuj wysyłanie i odbieranie wiadomości na wszystkich kontach firmowych.

Jeśli używasz zewnętrznych usług pocztowych jak Gmail czy Outlook, upewnij się, że rekordy SPF, DKIM i DMARC nadal wskazują właściwe serwery.