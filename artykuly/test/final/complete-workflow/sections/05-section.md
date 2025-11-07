### Zarządzanie danymi testowymi

Dane to fundament każdego workflow testu. Bez poprawnych danych nawet najlepiej napisany test zawiedzie. Problem w tym, że większość zespołów traktuje dane jako dodatek, nie jako kluczowy element strategii.

Typowy błąd? Używanie tych samych danych do wszystkich testów. Jeden test modyfikuje użytkownika, drugi próbuje go utworzyć ponownie - i masz konflikt. Albo gorszy scenariusz: dane "przypadkowo" znikają z bazy i połowa testów pada.

### Strategie generowania danych testowych

Świeże dane na początku każdego testu to złoty standard. Tak, trwa to dłużej. Ale eliminuje 90% problemów z niestabilnymi testami.

Factory pattern sprawdzi się idealnie. Tworzysz UserFactory, ProductFactory, OrderFactory. Każdy generuje obiekt z losowymi, ale poprawnymi danymi. Potrzebujesz użytkownika premium? `UserFactory.createPremium()`. Produkt w promocji? `ProductFactory.createDiscounted()`.

Dla złożonych scenariuszy przydają się scenariusze danych. Test procesu zwrotu potrzebuje: użytkownika z historią zamówień, produktu z polityką zwrotów i aktywnej metody płatności. Jeden zestaw danych, jedno wywołanie setup.

### Cleanup i izolacja

Każdy test powinien zostawić środowisko w stanie początkowym. To znaczy usunąć wszystkie dane, które utworzył. Transaction rollback działa dla baz danych. Ale workflow testy często modyfikują pliki, cache, systemy zewnętrzne.

Najlepsza praktyka: lista cleanup actions w każdym teście. Po zakończeniu wykonaj je wszystkie, niezależnie od wyniku testu. Failed assertions nie mogą blokować sprzątania.

Izolacja namespace również pomaga. Każdy test dostaje unikalny prefiks - timestamp plus random string. Wszystkie obiekty tworzone z tym prefiksem można łatwo wyczyścić po zakończeniu.

### Projektowanie stabilnych testów workflow

Stabilność to największe wyzwanie workflow testów. Dziś przechodzi, jutro pada - bez żadnej zmiany w kodzie. Frustrujące, ale możliwe do opanowania.

Główny winowajca? Timing issues. Aplikacja jeszcze ładuje dane, a test już próbuje kliknąć przycisk. Albo async operacja trwa dłużej niż zwykle i test timeout'uje.

Smart wait strategies rozwiązują większość problemów. Zamiast `sleep(5000)` użyj `waitForElementVisible()`. Zamiast fixed timeout zastosuj exponential backoff. Test poczeka tyle, ile potrzeba - nie więcej, nie mniej.

Dynamic elements wymagają szczególnej uwagi. ID generowane po stronie serwera, listy ładowane asynchronicznie, modalne okna z animacjami. Każdy element musi mieć niezawodny selektor i odpowiednią strategię oczekiwania.