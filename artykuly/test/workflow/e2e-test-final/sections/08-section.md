## Troubleshooting częstych problemów

Każdy developer przeżył ten moment. Testy działają lokalnie, ale failują na CI. Albo przechodzą dziesięć razy z rzędu, a potem nagle czerwienieją bez widocznego powodu. W świecie blog-agentów takie sytuacje są jeszcze bardziej frustrujące.

### Flaky tests i jak ich unikać

Race conditions w async code to klasyk gatunku. Blog-agent wysyła request do OpenAI, ale test sprawdza wynik zanim odpowiedź zdąży wrócić. Albo dwa procesy próbują jednocześnie zapisać do tej samej tabeli.

Rozwiązanie? Proper synchronization. Zamiast `setTimeout(1000)` użyj `waitFor()` z sensownymi warunkami. Sprawdź czy element rzeczywiście się pojawił, a nie czy minęła określona liczba milisekund.

Environment inconsistencies to kolejny zabójca stabilności. Na lokalnej maszynie masz SSD, na CI slow disk. Lokalnie używasz najnowszego Node.js, CI ma starszą wersję. Te różnice kumulują się i prowadzą do nieprzewidywalnych błędów.

Data cleanup między testami wymaga szczególnej uwagi. Jeden test generuje artykuł "Test Article", następny próbuje zrobić to samo i dostaje constraint violation. Database seeding i teardown muszą być bulletproof.

Najgorsze są testy, które failują sporadycznie. Raz na dziesięć uruchomień, zawsze w piątek po 17:00. Te wymagają cierpliwości i systematycznego podejścia.

### Debug'owanie complex failures

Log analysis to sztuka czytania między wierszami. Error "Database connection failed" może oznaczać problem z siecią, przekroczony pool limit albo po prostu source system restart.

Structured logging pomaga enormnie. Correlation IDs pozwalają śledzić jeden request przez wszystkie serwisy. Timestamp'y z mikrosekundami ujawniają timing issues.

Reproducing production issues lokalnie to często największe wyzwanie. Production ma inne dane, inny load, inne network conditions. Czasem musisz stworzyć synthetic scenarios żeby złapać problem.

Postmortem best practices to nie tylko analiza co poszło źle, ale przede wszystkim jak temu zapobiec. Root cause analysis, timeline reconstruction, action items z ownerami. I najważniejsze - follow-up żeby sprawdzić czy fixes rzeczywiście działają.

Dokumentuj wszystko. Następny developer (albo ty za pół roku) będzie wdzięczny za szczegółowy opis problemu i rozwiązania.