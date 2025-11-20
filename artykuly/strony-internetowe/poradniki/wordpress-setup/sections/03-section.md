## Instalacja WordPress - krok po kroku bez stresu

Teraz, gdy macie już hosting i domenę, czas na właściwą instalację. Dobra wiadomość – to prostsze niż myślicie. Większość problemów wynika z tego, że ludzie komplikują sobie życie, wybierając trudniejszą drogę niż potrzeba.

### Automatyczna instalacja przez panel hostingu

Zacznijcie od sprawdzenia, czy wasz hosting oferuje automatyczną instalację WordPress. W 9 przypadkach na 10 będzie dostępna – to standard branży.

W cPanelu szukajcie ikony "WordPress" lub "Softaculous" w sekcji "Autoinstalatory". DirectAdmin ma podobną funkcję w dziale "Extra Features". Kliknięcie przeniesie was do kreatora, który poprowadzi przez cały proces.

Instalacja jednym kliknięciem to nie marketingowy chwyt, a rzeczywistość. System automatycznie tworzy bazę danych, pobiera najnowszą wersję WordPress, konfiguruje pliki i ustawia podstawowe parametry. Wy tylko podajecie nazwę strony, login administratora i hasło.

Przy ustawieniach początkowych zwróćcie uwagę na kilka rzeczy. Katalog instalacji zostawcie pusty, chyba że chcecie blog w podfolderze (np. mojafirma.pl/blog). Login administratora – nigdy "admin", to pierwszy cel hakerów. Hasło powinno mieć minimum 12 znaków z liczbami i znakami specjalnymi.

Cały proces zajmuje 2-3 minuty. Na koniec dostaniecie link do panelu administracyjnego i dane logowania.

### Ręczna instalacja WordPress

Instalacja ręczna ma sens w kilku sytuacjach. Gdy hosting nie oferuje autoinstalatorów (coraz rzadsze), gdy potrzebujecie specyficznej konfiguracji bazy danych, lub gdy chcecie mieć pełną kontrolę nad procesem.

Pobierzcie najnowszą wersję z wordpress.org – zawsze z oficjalnego źródła. Rozpakujcie archiwum i edytujcie plik wp-config-sample.php, wpisując dane dostępu do bazy danych. Te informacje znajdziecie w panelu hostingu.

Upload przez FTP może zająć 10-15 minut, w zależności od prędkości internetu. Wrzucajcie pliki bezpośrednio do katalogu głównego domeny (public_html lub httpdocs). Po uploadzie przejdźcie na waszą domenę – WordPress automatycznie uruchomi kreator instalacji.

### Pierwsze logowanie i orientacja w panelu administracyjnym

Panel administratora WordPress znajduje się zawsze pod adresem wasza-domena.pl/wp-admin. Po pierwszym logowaniu zobaczycie kokpit – centralną deskę rozdzielczą systemu.

Po lewej stronie menu z podstawowymi funkcjami: Wpisy (artykuły na blogu), Strony (statyczne podstrony jak "O nas"), Multimedia (zdjęcia i pliki), Wygląd (motywy i personalizacja), Wtyczki i Ustawienia.

Pierwszą rzeczą, którą zróbcie, to zmiana domyślnego hasła na jeszcze silniejsze. Idźcie do Użytkownicy > Profil i zaktualizujcie swoje dane. Usuńcie też przykładowy wpis "Hello World" i stronę "Sample Page" – to jasny sygnał dla wszystkich, że strona jest świeża z instalacji.

Gratulacje – wasz WordPress działa i czeka na personalizację.