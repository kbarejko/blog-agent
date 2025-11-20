## Checklist: Implementacja SSL/HTTPS w firmie

- [ ] Wykonaj szczegółowy przegląd wszystkich istniejących certyfikatów SSL w obrębie Twoich domen i subdomen
- [ ] Zweryfikuj poziom zabezpieczeń swoich witryn używając SSL Labs (https://www.ssllabs.com/ssltest/) - ocena A to minimum, do którego warto dążyć
- [ ] Określ właściwy rodzaj certyfikatu: certyfikat DV sprawdzi się w małych przedsiębiorstwach, OV to dobry wybór dla firm średniej wielkości, natomiast EV może być konieczny w korporacjach
- [ ] Pozyskaj i wdróż certyfikat SSL u zaufanego dostawcy - warto porównać oferty kilku firm
- [ ] Wprowadź automatyczne przekierowania 301 z protokołu HTTP na HTTPS dla wszystkich stron
- [ ] Przeprowadź aktualizację wszystkich wewnętrznych odnośników, zmieniając je z HTTP na HTTPS
- [ ] Wyeliminuj problemy z mixed content - każdy zasób (obrazy, skrypty JavaScript, pliki CSS) musi używać protokołu HTTPS
- [ ] Uaktualnij pliki sitemap.xml oraz robots.txt, uwzględniając nowe adresy HTTPS
- [ ] Zaktualizuj ustawienia adresów URL w Google Search Console i Google Analytics - ten krok często jest pomijany
- [ ] Skonfiguruj system monitorowania terminów ważności certyfikatów z powiadomieniami wysyłanymi 30 dni przed wygaśnięciem
- [ ] Przetestuj dokładnie całą funkcjonalność witryny po zakończeniu migracji na HTTPS - szczególnie formularze i płatności
- [ ] Zaplanuj cykliczne przeglądy bezpieczeństwa SSL co pół roku, aby utrzymać najwyższe standardy ochrony