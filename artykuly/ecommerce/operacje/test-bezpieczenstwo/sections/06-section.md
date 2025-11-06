#### Zasady tworzenia haseł

"Admin123!" to nie hasło - to zaproszenie dla hakera. Słabe hasła to najczęstsza przyczyna włamań. Lista najpopularniejszych haseł w 2024 roku wygląda żałośnie: "password", "123456", "admin". Każde z nich można złamać w kilka sekund.

Generatory haseł tworzą prawdziwie losowe kombinacje. "K7$mP9#xQ2wE" to przykład silnego hasła - długie, nieprzewidywalne, niemożliwe do odgadnięcia. Problem w tym, że również niemożliwe do zapamiętania.

Menedżery haseł rozwiązują ten dylemat. Bitwarden, 1Password czy LastPass pamiętają wszystkie hasła za ciebie. Ty musisz znać tylko jedno - master password do menedżera. Wszystkie pozostałe mogą być tak skomplikowane, jak to możliwe.

Polityka rotacji haseł to kontrowersyjny temat. Dawniej zalecano zmianę co 90 dni. Teraz eksperci mówią: lepsze długie, stałe hasło niż częsta zmiana na słabe. Ludzie zmuszeni do rotacji tworzą przewidywalne wzorce: "Hasło1", "Hasło2", "Hasło3".

Hasła jednorazowe dla kontrahentów to praktyczna kwestia. Deweloper kończy projekt - natychmiast zmieniasz wszystkie hasła. Freelancer robi audyt SEO - dostaję tymczasowy dostęp z datą ważności. Po terminie konto blokuje się automatycznie.

### Kontrola uprawnień zespołu

Każdy pracownik potrzebuje dostępu, ale nie każdy do wszystkiego. Junior od social mediów nie musi widzieć raportów finansowych. Magazynier nie potrzebuje dostępu do ustawień płatności.

Role-based access control (RBAC) organizuje uprawnienia w logiczne grupy. Administrator ma pełny dostęp. Redaktor zarządza treścią, ale nie może zmieniać ustawień. Sprzedawca widzi zamówienia, ale nie dane finansowe.

Zasada minimalnych uprawnień brzmi prosto: każdy dostaje minimum potrzebne do pracy. W praktyce oznacza to regularne przeglądy i zadawanie niewygodnych pytań. Dlaczego praktykant ma uprawnienia admina? Czy kierownik marketingu naprawdę musi widzieć bazę klientów?

Audyt uprawnień powinien być miesięczną rutyną. Kto ma dostęp do panelu administracyjnego? Kiedy ostatnio logowali się poszczególni użytkownicy? Nieaktywne konta to potencjalne backdoory dla byłych pracowników.

Procedury przy zmianie personelu to test prawdziwej kultury bezpieczeństwa. Pracownik odchodzi w złej atmosferze? Zmiana haseł musi nastąpić przed jego ostatnim dniem pracy. Zwolnienie dyscyplinarne? Dostępy blokujesz natychmiast, nie czekasz do końca wypowiedzenia.