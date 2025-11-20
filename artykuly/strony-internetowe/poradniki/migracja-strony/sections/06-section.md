## SEO podczas migracji - Zachowanie pozycji w wyszukiwarkach

Migracja strony to moment, gdy latami budowane pozycje w Google mogą się rozpaść w ciągu kilku dni. Jednak przy odpowiednim podejściu możesz przejść przez ten proces bez strat, a czasem nawet z zyskiem.

### Mapa przekierowań URL

Zacznij od sporządzenia kompletnej listy wszystkich ważnych adresów URL. Nie ograniczaj się do głównych stron - uwzględnij wpisy na blogu, strony produktów, kategorie i wszystkie podstrony, które generują ruch organiczny. Google Analytics w sekcji "Behavior > Site Content > All Pages" pokaże ci najważniejsze URL-e z ostatnich 12 miesięcy.

Przygotowanie przekierowań 301 to żmudna, ale kluczowa robota. Każdy stary adres musi mieć swoje nowe miejsce docelowe. Jeśli zmieniasz struktur URL-i podczas migracji, stwórz mapę w arkuszu kalkulacyjnym: stary URL w pierwszej kolumnie, nowy w drugiej.

Zachowaj dotychczasową strukturę URL tam, gdzie to tylko możliwe. Jeśli Twoja strona produktu była pod adresem `/produkty/nazwa-produktu`, utrzymaj ten schemat na nowym serwerze. Google traktuje zmianę URL-a jako sygnał, że to nowa strona - bez potrzeby nie komplikuj sobie życia.

Przygotuj przekierowania przed zmianą DNS, ale aktywuj je dopiero gdy ruch zacznie trafiać na nowy serwer. W Apache używaj pliku .htaccess, w Nginx konfiguruj przekierowania w pliku konfiguracyjnym serwera.

Aktualizacja mapy strony XML powinna nastąpić już pierwszego dnia po migracji. Usuń stare URL-e, dodaj nowe. Jeśli zmieniasz strukturę, stwórz całkowicie nową mapę strony odzwierciedlającą aktualną hierarchię.

### Komunikacja z Google

Google Search Console to Twój bezpośredni kanał komunikacji z wyszukiwarką. Jeśli zmieniasz domenę, użyj funkcji "Change of Address" w starym profilu Search Console. Dla migracji w obrębie tej samej domeny wystarczy przesłać nową mapę strony.

Utwórz nowy profil w Search Console dla nowej wersji strony już w dniu migracji. Prześlij świeżą mapę XML i monitoruj raporty błędów 404. Każdy taki błąd to potencjalnie utracone pozycje.

Indeksowanie po migracji może potrwać od kilku dni do kilku tygodni. Używaj narzędzia "URL Inspection" do sprawdzania czy kluczowe strony są już zindeksowane. Możesz też poprosić o ponowne przeskanowanie najważniejszych URL-i.

Śledź pozycje kluczowych fraz codziennie przez pierwsze dwa tygodnie. Niewielkie spadki są normalne, ale drastyczne zmiany mogą sygnalizować problemy z przekierowaniami lub indeksowaniem. Narzędzia takie jak SEMrush czy Ahrefs pomogą monitorować zmiany pozycji w czasie rzeczywistym.

---