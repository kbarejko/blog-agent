## Błędy SSL/TLS - jak je identyfikować i naprawiać

Nawet najlepiej skonfigurowany certyfikat może sprawiać problemy. Błędy SSL frustrują użytkowników i kosztują sprzedawców miliony złotych rocznie. Kluczem jest szybka identyfikacja i naprawa zanim straty staną się nieodwracalne.

"Twoje połączenie nie jest prywatne" to najczęstszy komunikat, który widzi użytkownik. Przyczyny? Wygasły certyfikat, niewłaściwa konfiguracja lub problem z zegarem systemowym. "NET::ERR_CERT_AUTHORITY_INVALID" oznacza, że przeglądarka nie rozpoznaje wystawcy certyfikatu - częsty problem z tanimi dostawcami spoza listy zaufanych CA.

"SSL_ERROR_BAD_CERT_DOMAIN" pojawia się, gdy certyfikat wystawiono dla innej domeny. Przykład: certyfikat dla "www.sklep.pl" nie zadziała na "sklep.pl" bez przedrostka. Certyfikaty wildcard (*.sklep.pl) rozwiązują ten problem dla wszystkich subdomen jednocześnie.

### Mixed content - największy problem migracji

Mixed content to sytuacja, gdy strona HTTPS ładuje zasoby przez HTTP. Przeglądarka blokuje "niebezpieczne" elementy jak skrypty czy iframe'y, ale obrazki tylko oznacza ostrzeżeniem. Rezultat? Brak zielonej kłódki i spadek zaufania klientów.

Chrome DevTools w zakładce Console wyświetli wszystkie zablokowane zasoby. Typowe źródła problemów to stare API płatności, widgety social media, systemy analityczne czy CDN-y obrazków. Rozwiązanie wydaje się proste - zamień HTTP na HTTPS, ale nie wszystkie zewnętrzne serwisy obsługują szyfrowanie.

### Problemy z łańcuchem certyfikatów

Łańcuch certyfikatów to hierarchia zaufania od twojego certyfikatu do root CA. Brakujące ogniwo oznacza błąd weryfikacji w niektórych przeglądarkach lub na urządzeniach mobilnych. Serwer musi dostarczyć cały łańcuch - twój certyfikat plus certyfikaty pośrednie.

SSL Labs to darmowe narzędzie, które przeskanuje konfigurację w 30 sekund. Ocena A+ oznacza perfekcję, B to ostrzeżenie, poniżej C wymaga natychmiastowej interwencji. SSLyze dla bardziej technicznych audytów sprawdzi wszystkie obsługiwane cipher suites i protokoły.

Koszt błędów SSL może być dramatyczny. E-sklep z elektroniką stracił 60% konwersji przez błąd mixed content w koszyku. Problem trwał weekend, bo nikt nie monitorował alertów. Platforma B2B straciła kontrakt wart milion złotych, gdy certyfikat wygasł podczas prezentacji dla kluczowego klienta.

Monitoring w czasie rzeczywistym to jedyna obrona przed takimi scenariuszami.