## Podstawy strategii backup - od czego zacząć

Zanim wybierzesz narzędzia czy dostawcę, musisz wiedzieć, co dokładnie chronisz. To jak budowa domu - najpierw fundamenty, potem ściany.

### Audit aktualnego stanu danych

Zacznij od inwentaryzacji. Które dane są krytyczne dla biznesu? Nie chodzi tylko o bazy klientów czy dokumentację projektową. W firmie produkcyjnej to może być oprogramowanie sterujące maszynami, w biurze prawnym - szablony umów, a w agencji marketingowej - biblioteka zasobów graficznych.

Stwórz prostą tabelę z trzema kolumnami: typ danych, ważność biznesowa (krytyczne/ważne/pomocnicze) i wpływ utraty na działalność. System księgowy? Krytyczny - bez niego nie wystawisz faktury. Archiwum zdjęć firmowych? Pomocnicze - strata nieprzyjemna, ale nie paraliżuje pracy.

Następnie zmapuj lokalizacje. Dane rozprzestrzeniły się wszędzie: serwery lokalne, OneDrive, dyski zewnętrzne, laptopy pracowników, a nawet telefony służbowe z kontaktami klientów. W jednej z firm, z którą pracowałem, kluczowa dokumentacja techniczna leżała na prywatnym Dropboxie głównego inżyniera.

Sprawdź też obecne rozwiązania backupowe. Czy w ogóle istnieją? Kiedy ostatnio ktoś testował przywracanie? Często okazuje się, że "automatyczny backup" nie działa od miesięcy, a nikt tego nie zauważył.

### Określenie RTO i RPO dla biznesu

Recovery Time Objective (RTO) to czas, jaki możesz być offline bez katastrofalnych skutków. Dla sklepu internetowego RTO może wynosić godzinę - dłużej oznacza utracone zamówienia. Dla małego biura rachunkowego - może to być 8 godzin.

Recovery Point Objective (RPO) określa, ile danych możesz stracić. Jeśli robisz backup raz dziennie, RPO wynosi maksymalnie 24 godziny pracy. Czy Twój biznes przetrwa utratę całego dnia transakcji?

Te parametry bezpośrednio wpływają na koszty. RTO 1 godzina wymaga rozwiązań klasy enterprise z replikacją w czasie rzeczywistym. RTO 24 godziny? Wystarczy standardowy backup nocny i procedura przywracania.

Nie zgaduj - porozmawiaj z użytkownikami i właścicielami procesów biznesowych. Ich odpowiedzi determinują całą strategię backup.