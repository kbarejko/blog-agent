## Najczęstsze problemy i jak ich unikać

Nawet najlepiej zaplanowana migracja może napotkać komplikacje. Znając typowe problemy z góry, będziesz mógł szybko je rozwiązać zamiast panikować.

Awaria podczas migracji wymaga zimnej krwi i gotowego planu awaryjnego. Jeśli coś idzie nie tak, nie improwizuj - wróć do kopii zapasowej i przywróć działanie starego serwera. Lepiej odłożyć migrację o tydzień niż stracić dostęp do strony na kilka dni. Zawsze miej przygotowane instrukcje cofnięcia zmian DNS i reaktywacji starego hostingu.

Problemy z bazą danych to częsta przyczyna białych stron po migracji. Najczęściej winne są różnice w wersjach MySQL lub błędne dane dostępowe. Sprawdź log błędów serwera - tam znajdziesz konkretny komunikat zamiast zgadywać. Jeśli import bazy się nie powiódł, spróbuj eksportować mniejszymi częściami lub zmień kodowanie na UTF-8.

Konflikt wersji PHP może zepsuć całą stronę. Stare moduły WordPress czy nieaktualne wtyczki często nie działają z nowszymi wersjami PHP. Przed migracją sprawdź kompatybilność wszystkich używanych rozszerzeń. W razie problemów tymczasowo obniż wersję PHP na nowym serwerze, a potem stopniowo aktualizuj komponenty.

Utrata funkcjonalności często wynika z zapomnianej konfiguracji. Integracje z zewnętrznymi API, połączenia z systemami płatności czy ustawienia SMTP dla poczty - każdy element wymaga weryfikacji. Zanotuj wszystkie zewnętrzne usługi jeszcze przed migracją.

Problemy z indeksowaniem w Google mogą pojawić się kilka dni po migracji. Jeśli strony znikają z wyników wyszukiwania, sprawdź czy przekierowania działają poprawnie i czy nowa mapa strony została przyjęta w Search Console. Czasem pomaga ręczne zgłoszenie najważniejszych URL-i do reindeksacji.

Spadek ruchu organicznego w pierwszych dniach to normalny efekt uboczny. Google potrzebuje czasu na ponowne przeskanowanie strony. Jednak spadek większy niż 20-30% może sygnalizować poważne problemy z przekierowaniami lub dostępnością treści.