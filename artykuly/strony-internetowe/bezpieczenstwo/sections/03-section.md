## Certyfikaty SSL i szyfrowanie połączeń

HTTP to dziś cyfrowy odpowiednik wysyłania karty pocztowej z hasłem do banku. Wszystko widać w przesyłanych danych - loginy, hasła, dane osobowe klientów. Google od 2017 roku oznacza strony HTTP jako "niezabezpieczone" w przeglądarce Chrome. Firefox i inne przeglądarki poszły tym samym śladem.

Algorytm Google od 2014 roku faworyzuje strony HTTPS. To nie jest ogromny boost rankingowy, ale w konkurencyjnych branżach każdy czynnik ma znaczenie. Ważniejsze jest zaufanie użytkowników. Badania pokazują, że 85% konsumentów sprawdza czy strona używa HTTPS przed podaniem danych karty płatniczej.

Masz do wyboru trzy podstawowe rodzaje certyfikatów SSL. Domain Validated (DV) weryfikuje tylko własność domeny - tani i szybki w uzyskaniu. Organization Validated (OV) sprawdza dodatkowo dane firmy w rejestrze. Extended Validation (EV) to najwyższy poziom weryfikacji, pokazujący nazwę firmy w pasku adresu przeglądarki.

Dla większości firm wystarczy certyfikat DV od Let's Encrypt - darmowy i automatycznie odnawialny. Sklepy internetowe powinny rozważyć OV lub EV dla zwiększenia zaufania klientów.

Kompletny przewodnik po SSL i HTTPS: [SSL i HTTPS - przewodnik](/ssl-i-https)

Migracja z HTTP na HTTPS wymaga systematycznego podejścia. Najpierw zainstaluj certyfikat i przetestuj działanie na subdomeinie testowej. Następnie przekieruj cały ruch z HTTP na HTTPS za pomocą kodu 301. Zaktualizuj linki wewnętrzne w treściach i menu. Zmień adresy w Google Search Console i Google Analytics.

Najczęstszy problem to mixed content - sytuacja gdy strona HTTPS ładuje elementy przez niezabezpieczone HTTP. Przeglądarki blokują takie zasoby lub pokazują ostrzeżenia. Drugi problem to nieprawidłowe przekierowania powodujące pętle lub błędy 404.

Automatyczne odnowienie certyfikatów to konieczność. Certyfikat Let's Encrypt wygasa po 90 dniach. Ręczne odnawianie oznacza ryzyko przestoju strony. Większość hostingów oferuje automatyzację tego procesu. Jeśli używasz dedykowanego serwera, skonfiguruj CRON job do automatycznego odnawiania i restartowania serwera web.