### Zarządzanie stanem aplikacji między testami

Izolacja testów brzmi teoretycznie, ale w praktyce okazuje się jednym z najtrudniejszych wyzwań. Każdy test powinien startować z czystym stanem, wykonywać swoje zadanie i zostawiać środowisko gotowe dla następnego. W rzeczywistości testy wpływają na siebie nawzajem przez shared database, cached data, localStorage czy session storage.

**Setup i teardown procedures** to fundament stabilnych testów. Before hook tworzy potrzebne dane. After hook sprząta po sobie. Brzmi prosto, ale diabeł tkwi w szczegółach. Jeśli setup pada, czy teardown się wykonuje? Co jeśli test przerywa się w połowie i zostawia aplikację w inconsistent state?

Robust approach wymaga defensive programming. Każdy test powinien móc wystartować niezależnie od stanu poprzedników. Oznacza to czasem redundantne cleanup operations na początku, nie tylko na końcu.

**Clean slate approach** idzie o krok dalej. Zamiast polegać na cleanup, każdy test dostaje fresh environment. Nowa baza danych, nowe user accounts, reset application state. Docker containers sprawdzają się tu doskonale - każdy test run dostaje własny kontener.

Koszt tego podejścia to czas wykonania. Spinowanie fresh environment zajmuje sekundy lub minuty. Dla smoke testów może być akceptowalne. Dla comprehensive suite z setkami testów - problematyczne.

**Database seeding strategies** wymagają przemyślenia architektury danych. Jedne zespoły preferują database snapshots - backup'owany stan przed każdym testem, restore po zakończeniu. Inne budują seed data od zera przez API calls.

Snapshot approach jest szybszy, ale mniej flexible. Gdy zmieni się struktura bazy, wszystkie snapshots wymagają update. API seeding trwa dłużej, ale adapts automatically do schema changes.

**Transaction rollbacks** oferują eleganckie rozwiązanie dla niektórych scenariuszy. Test startuje database transaction, wykonuje operacje, a na końcu robi rollback. Wszystkie zmiany znikają automatycznie. Nie działa jednak z testami, które sprawdzają multiple database connections albo external integrations.

Kluczowe jest testowanie samych procedures. Jeśli setup pada w 1% przypadków, cały test suite staje się unreliable. Monitoring i alerting powinny obejmować również infrastructure operations, nie tylko business logic.