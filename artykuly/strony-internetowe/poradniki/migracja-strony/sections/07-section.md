## Testing i weryfikacja po migracji

Zmiana DNS się propaguje, ruch płynie na nowy serwer. Jednak dopiero teraz zaczyna się prawdziwy test - czy wszystko działa tak, jak powinno.

### Lista kontrolna funkcjonalności

Pierwszego dnia po migracji przejdź przez stronę jak najbardziej wymagający klient. Wypełnij każdy formularz kontaktowy i sprawdź, czy wiadomości docierają na właściwe adresy. Często okazuje się, że skrypt wysyłający maile wymaga dodatkowej konfiguracji na nowym serwerze.

Jeśli prowadzisz sklep internetowy, przetestuj cały proces zakupowy. Dodaj produkty do koszyka, przejdź przez checkout, sprawdź czy generują się faktury. Szczególną uwagę poświęć systemowi płatności - błąd tutaj może kosztować utracone zamówienia zanim go zauważysz.

System płatności wymaga osobnego testu na małej kwocie. Bramki płatnicze często mają różne ustawienia środowiska produkcyjnego i testowego. Upewnij się, że płatności trafiają na właściwe konto bankowe.

Responsywność na urządzeniach mobilnych może się zmienić po migracji. Różnice w konfiguracji serwera czasem wpływają na sposób ładowania CSS czy JavaScript. Przetestuj stronę na telefonie i tablecie - szczególnie formularze i menu nawigacyjne.

Sprawdź też funkcje, które używa niewielu odwiedzających, ale są krytyczne - newsletter, logowanie do panelu klienta, download plików. Te elementy łatwo pominąć w rutynowych testach.

### Monitorowanie wydajności

Szybkość ładowania strony może dramatycznie się zmienić po migracji. Użyj narzędzi takich jak GTmetrix lub PageSpeed Insights, żeby porównać wyniki z poprzednimi pomiarami. Nowy serwer może być szybszy, ale źle skonfigurowany cache potrafi wszystko zepsuć.

Uptime to kluczowa metryka pierwszych tygodni. Ustaw monitoring w UptimeRobot czy podobnym narzędziu. Będziesz wiedzieć o problemach często szybciej niż hosting, który może potrzebować czasu na wykrycie i rozwiązanie awarii.

Obciążenie serwera pokazuje, czy nowy hosting radzi sobie z Twoim ruchem. W panelu hostingowym śledź zużycie CPU i RAM, szczególnie w godzinach szczytu. Gwałtowne skoki mogą oznaczać nieoptymalne ustawienia lub niekompatybilność z nowym środowiskiem.

Optymalizacja wydajności może wymagać dostosowania do specyfiki nowego serwera. Cache może potrzebować rekonfiguracji, obrazki - kompresji, a baza danych - optymalizacji. Pierwszych kilka dni to idealna okazja na fine-tuning.