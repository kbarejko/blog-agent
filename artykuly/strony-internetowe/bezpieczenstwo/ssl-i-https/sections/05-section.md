## Bezpieczeństwo danych klientów i zgodność z przepisami

Pozycje w Google to jedno, ale prawdziwe konsekwencje braku SSL dotykają portfela przez regulacje prawne. W 2024 roku przepisy nie wybaczają - każde naruszenie to kary liczone w milionach złotych lub euro.

### RODO i ochrona danych osobowych

Rozporządzenie RODO wymaga od firm "odpowiednich środków technicznych" do ochrony danych osobowych. Choć nie wymienia SSL wprost, brak szyfrowania oznacza łamanie art. 32 - obowiązku zabezpieczenia danych. W praktyce to automatyczna przegrana w przypadku kontroli UODO.

Prawniczka specjalizująca się w RODO wyjaśniła mi to podczas audytu u klienta: "Przesyłanie formularzy kontaktowych przez HTTP to jak wysyłanie listów na otwartych kartkach. UODO nie przyjmie argumentu o braku środków".

Dokumentowanie środków technicznych to kluczowa część compliance. Musisz prowadzić rejestr certyfikatów SSL, ich dat wygaśnięcia i konfiguracji szyfrowania. W przypadku kontroli to pierwszy dokument, jakiego żądają inspektorzy. Szablon znajdziesz w wytycznych UODO, ale podstawowe elementy to: typ certyfikatu, siła szyfrowania, daty ważności i odpowiedzialni pracownicy.

Kary potrafią zrujnować firmę. French data protection authority nałożyła 60 milionów euro kary na Google za nieprawidłowe zabezpieczenia. W Polsce rekordzistą jest kara 220 tysięcy złotych dla firmy telekomunikacyjnej. Większość dotyczy dużych korporacji, ale UODO coraz częściej kontroluje małe firmy - szczególnie te obsługujące płatności online.

### Standardy branżowe (PCI DSS, ISO 27001)

PCI DSS to obowiązkowy standard dla każdej firmy przetwarzającej płatności kartami. Wymóg 4.1 jasno stwierdza: "Użyj silnego szyfrowania i protokołów bezpieczeństwa". Bez certyfikatu SSL nawet nie rozpoczniesz procesu certyfikacji. TLS 1.2 to minimum, ale od 2025 roku będzie wymagany TLS 1.3.

Sklepy internetowe mają dodatkowe wymagania. Wszystkie formularze płatności muszą używać HTTPS, a dane kart nie mogą przechodzić przez nieszyfrowane połączenia. Acquirer (firma obsługująca płatności) może zablokować konto za naruszenie PCI DSS. Bez prawa do przyjmowania kart online sklep praktycznie przestaje istnieć.

Certyfikacja ISO 27001 daje przewagę w przetargach publicznych i kontraktach B2B. Wymaga ona "kryptograficznych zabezpieczeń" dla wszystkich systemów IT. SSL to fundament - bez niego audytorzy nie przejdą do kolejnych punktów.

Audyty bezpieczeństwa przeprowadzane przez zewnętrzne firmy kosztują 10-50 tysięcy złotych, ale chronią przed karami sięgającymi milionów. Klient z branży logistycznej zyskał kontrakt wart 2 miliony złotych, bo jako jedyny spełniał wymagania ISO 27001. Inwestycja w certyfikację zwróciła się już przy pierwszym zleceniu.