## Checklist: Migracja strony internetowej

- [ ] Zrób szczegółową inwentaryzację wszystkich plików, baz danych i funkcji obecnej witryny. Może wydawać się to oczywiste, ale właśnie ten krok najczęściej jest przeoczany
- [ ] Przeanalizuj statystyki w Google Analytics i zidentyfikuj kluczowe strony generujące największy ruch - to one będą wymagały szczególnej uwagi
- [ ] Wykonaj kompletną kopię zapasową plików (przez FTP) oraz całej bazy danych, a następnie koniecznie przetestuj, czy backup rzeczywiście się odtworzy
- [ ] Obniż TTL rekordów DNS do 300 sekund, najlepiej 24-48 godzin przed planowaną migracją - pozwoli to na szybszą propagację zmian
- [ ] Przenieś wszystkie pliki na nowy serwer używając FTP lub SFTP, następnie zaimportuj bazę danych do nowego środowiska
- [ ] Zaktualizuj pliki konfiguracyjne - szczególnie parametry połączenia z bazą danych i ścieżki do katalogów, a także ustaw właściwe uprawnienia do folderów
- [ ] Przygotuj kompletną listę krytycznych URL-i i skonfiguruj przekierowania 301 dla wszystkich zmienionych adresów - to prawdopodobnie najważniejszy element z punktu widzenia SEO
- [ ] Zmień wskazania DNS na nowy serwer i systematycznie monitoruj propagację zmian w różnych regionach
- [ ] Dokładnie przetestuj wszystkie kluczowe funkcjonalności: formularze kontaktowe, system płatności, logowanie użytkowników oraz responsywność na różnych urządzeniach
- [ ] Wygeneruj aktualną mapę strony XML i prześlij ją do Google Search Console - pomoże to przyspieszyć reindeksację
- [ ] Jeśli zmieniasz domenę, powiadom Google Search Console o zmianie adresu witryny korzystając z dedykowanego narzędzia
- [ ] Intensywnie monitoruj przez pierwszy tydzień: ruch organiczny, proces indeksowania, potencjalne błędy 404 oraz ogólną wydajność strony