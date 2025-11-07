### Przygotowanie środowiska testowego

Masz plan, wiesz co testować. Teraz potrzebujesz miejsca, gdzie te testy będą działać niezawodnie. Tu zaczyna się prawdziwa zabawa.

Środowisko testowe to nie kopia produkcji. To specjalnie zaprojektowana przestrzeń, która musi spełniać inne wymagania. Produkcja optymalizuje wydajność. Środowisko testowe optymalizuje przewidywalność.

Największy błąd? Założenie, że wystarczy sklonować prod i gotowe. W produkcji dane się zmieniają. Użytkownicy zachowują się nieprzewidywalnie. Systemy zewnętrzne czasem nie odpowiadają. W testach potrzebujesz kontroli nad każdym z tych elementów.

### Wymagania infrastrukturalne

Workflow testy są żarłoczne. Potrzebują więcej mocy obliczeniowej niż testy jednostkowe, ale inaczej niż myślisz.

Ważniejsza od surowej wydajności jest stabilność. Lepiej wolniejszy serwer, który zawsze odpowiada w tym samym czasie, niż szybki ale nieprzewidywalny.

Izolacja to klucz. Jeden test nie może wpływać na drugi. Oznacza to osobne bazy danych, oddzielne przestrzenie na plikach, niezależne instancje usług.

Rozważ konteneryzację. Docker pozwala szybko stawiać i burzyć środowiska. Kubernetes daje kontrolę nad zasobami. To inwestycja, która zwraca się przy pierwszym większym refactoringu testów.

### Konfiguracja danych testowych

Tu większość projektów popełnia kardynalny błąd. Używają tych samych danych do wszystkich testów.

Workflow test dla procesu zakupowego potrzebuje: użytkownika z kontem, produktów w magazynie, działającej metody płatności, aktualnej tabeli cen i poprawnie skonfigurowanej dostawy. Jeden niepoprawny rekord i test pada.

Najlepsza strategia to generowanie świeżych danych na początku każdego testu. Tak, to trwa dłużej. Ale eliminuje 90% problemów z niestabilnymi testami.

Jeśli generowanie trwa za długo, przygotuj zestawy seedów. Osobne dla każdego scenariusza. Pamiętaj o cleanup - dane po skończonym teście powinny zniknąć bez śladu.

### Zarządzanie zależnościami zewnętrznymi

Płatności, powiadomienia email, API pogodowe - workflow testy uwielbiają systemy zewnętrzne. Te systemy nie zawsze odwzajemniają tę miłość.

Mock to oczywiste rozwiązanie, ale nie jedyne. Czasem potrzebujesz prawdziwej integracji żeby złapać edge case'y. Wtedy przydają się sandboxi i środowiska developerskie zewnętrznych dostawców.

Service virtualization pozwala symulować różne odpowiedzi systemów zewnętrznych. Możesz testować scenariusze, które w prawdziwym świecie zdarzają się raz na miesiąc.

Najgorsze co możesz zrobić to uzależnić testy od produkcyjnych API. Testy mają być przewidywalne, nie losowe.