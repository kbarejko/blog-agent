## Czym są SSL/TLS i HTTPS - podstawy techniczne dla przedsiębiorcy

SSL i TLS to często mylone pojęcia. SSL (Secure Sockets Layer) to starszy protokół, który praktycznie wyszedł z użycia ze względu na luki bezpieczeństwa. Obecnie używamy TLS (Transport Layer Security) - jego nowszej, bezpieczniejszej wersji. Jednak nazwa "SSL" przyjęła się w branży i nadal tak mówimy o certyfikatach, choć technicznie to TLS. HTTPS to po prostu HTTP z warstwą szyfrowania TLS.

W praktyce biznesowej różnica jest minimalna - kupujesz "certyfikat SSL", ale używasz protokołu TLS. Kluczowe są wersje: TLS 1.2 to minimum dla firm, TLS 1.3 to obecny standard. Starsze wersje blokują już nowoczesne przeglądarki.

Proces szyfrowania działa jak skrytka z dwoma kluczami. Serwer ma klucz prywatny (trzyma go dla siebie) i publiczny (udostępnia wszystkim). Kiedy klient wysyła dane, szyfruje je kluczem publicznym. Odszyfrować może tylko serwer swoim prywatnym kluczem. To asymetryczne szyfrowanie - bezpieczne, ale powolne.

Dlatego po początkowym "uścisku dłoni" strony przełączają się na szyfrowanie symetryczne z jednym, wspólnym kluczem sesji. To kompromis między bezpieczeństwem a szybkością.

Certyfikat SSL to cyfrowy dowód tożsamości twojej firmy. Wystawia go zaufany urząd certyfikacji (CA), który potwierdza, że domain rzeczywiście należy do ciebie. Klienci widzą zieloną kłódkę i czują się bezpieczniej. Bez certyfikatu przeglądarki wyświetlają ostrzeżenie "Połączenie nie jest prywatne".

Proces handshake między przeglądarką a serwerem trwa milisekundy, ale ma kluczowe znaczenie. Przeglądarka sprawdza certyfikat, weryfikuje jego ważność u CA, uzgadnia algorytm szyfrowania i generuje klucze sesji. Każdy błąd w tym procesie kończy się ostrzeżeniem lub brakiem połączenia.

Wpływ na user experience jest ogromny. Strony HTTPS ładują się szybciej dzięki HTTP/2, nie pokazują ostrzeżeń bezpieczeństwa i budują zaufanie. Sklepy bez SSL tracą średnio 40% potencjalnych klientów już na etapie ostrzeżenia przeglądarki. W 2024 roku to nie opcja, a konieczność biznesowa.