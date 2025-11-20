## Proces techniczny migracji krok po kroku

Nadszedł moment prawdy. Masz gotową kopię zapasową i plan działania. Teraz czas na faktyczne przeniesienie strony na nowy serwer.

### Przeniesienie plików i baz danych

Rozpocznij od transferu plików przez FTP lub SFTP. Większość nowoczesnych paneli hostingowych oferuje menedżery plików, ale narzędzia takie jak FileZilla dają lepszą kontrolę nad procesem. Szczególnie ważne przy dużych stronach, gdzie transfer może trwać godziny.

Zacznij od przesłania najważniejszych plików - główny folder aplikacji, obrazki i dokumenty. Pozostaw na końcu elementy, które można łatwo przywrócić z kopii zapasowej, gdyby coś poszło nie tak.

Export bazy danych wymaga szczególnej ostrożności. W phpMyAdmin użyj opcji "Export" z ustawieniem "Custom". Zaznacz opcję "Add DROP TABLE" - zaoszczędzi ci problemów, jeśli będziesz musiał powtórzyć import. Dla dużych baz danych rozważ eksport fragmentami lub użycie narzędzi wiersza poleceń.

Import na nowym serwerze może nie przebiec gładko za pierwszym razem. Różnice w wersjach MySQL czasem powodują błędy składni. Jeśli napotkasz problemy, sprawdź log błędów serwera - często zawiera wskazówki do rozwiązania.

Konfiguracja środowiska na nowym serwerze to więcej niż kopiowanie plików. Sprawdź wersję PHP - musi być zgodna lub nowsza niż na starym hostingu. Upewnij się, że wszystkie wymagane rozszerzenia PHP są zainstalowane. Szczególnie ważne dla stron e-commerce czy zaawansowanych CMS-ów.

Po przeniesieniu danych wykonaj podstawową weryfikację. Sprawdź, czy główne pliki są na miejscu i czy baza danych zawiera wszystkie tabele. Porównaj rozmiary - drastyczne różnice mogą oznaczać niepełny transfer.

### Aktualizacja konfiguracji

Pierwsze, co musisz zmienić to ustawienia połączenia z bazą danych. W WordPress znajdziesz je w pliku wp-config.php, w Joomla w configuration.php. Wprowadź dane dostępowe do nowej bazy - nazwę serwera, login, hasło i nazwę bazy.

Sprawdź też ścieżki w plikach konfiguracyjnych. Jeśli nowy hosting ma inną strukturę katalogów, aplikacja może szukać plików w złych miejscach. Szczególnie często dotyczy to ścieżek do folderów z uploadami czy cache'em.

Uprawnienia plików to częsta przyczyna problemów po migracji. Większość plików powinna mieć uprawnienia 644, a katalogi 755. Jednak niektóre aplikacje wymagają specjalnych ustawień. Jeśli strona wyświetla błędy 500, zacznij sprawdzanie od uprawnień.

Nie zapomnij o plikach .htaccess - często zawierają ważne przekierowania i ustawienia bezpieczeństwa. Czasem trzeba je dostosować do nowego środowiska serwera.

Przetestuj wszystkie kluczowe funkcjonalności przed ogłoszeniem sukcesu. Sprawdź formularze kontaktowe, systemy płatności, logowanie użytkowników. Błąd w konfiguracji może nie być widoczny od razu, ale ujawni się dopiero przy konkretnej akcji użytkownika.