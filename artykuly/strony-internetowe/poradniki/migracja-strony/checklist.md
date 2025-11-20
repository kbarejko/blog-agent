## Checklist: Migracja strony internetowej

- [ ] Stwórz kompletną kopię zapasową wszystkich plików strony oraz bazy danych, następnie sprawdź czy możesz z niej skorzystać w przypadku problemów
- [ ] Przeanalizuj dokładnie obecną stronę - zanotuj wszystkie funkcje, dodatki i elementy techniczne, które muszą działać po migracji
- [ ] Sporządź listę wszystkich ważnych adresów URL i przygotuj plan przekierowań 301 dla linków, które zmienią swoją lokalizację
- [ ] Na 24-48 godzin przed migracją zmniejsz TTL rekordów DNS do 300 sekund - dzięki temu zmiany rozprzestrzenią się szybciej
- [ ] Ustaw nowe środowisko hostingowe i przetestuj działanie strony na domenie testowej, na przykład test.twojastrona.pl
- [ ] Prześlij pliki i bazę danych na nowy serwer, a następnie zaktualizuj pliki konfiguracyjne z nowymi parametrami połączenia
- [ ] Przekieruj DNS na nowe serwery i uruchom wszystkie zaplanowane przekierowania 301
- [ ] Sprawdź dokładnie kluczowe funkcje: czy działają formularze kontaktowe, system płatności, logowanie użytkowników oraz wersja mobilna
- [ ] W Google Search Console dodaj nową wersję witryny i prześlij aktualną mapę XML - to pomoże Google szybciej zindeksować zmiany
- [ ] Upewnij się, że wszystkie subdomeny (jak blog.twojastrona.pl) oraz poczta elektroniczna funkcjonują bez zakłóceń
- [ ] W pierwszym tygodniu codziennie monitoruj: ruch z wyszukiwarki, błędy 404, prędkość ładowania i ogólną dostępność witryny
- [ ] Po siedmiu dniach przeanalizuj pozycje w Google Search Console i rozwiąż ewentualne problemy z indeksowaniem stron