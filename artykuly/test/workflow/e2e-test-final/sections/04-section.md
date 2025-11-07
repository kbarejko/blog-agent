## Testowanie automatyzacji i schedulingu

Scheduler to puls blog-agenta. Gdy przestaje bić, cały system zamiera. A problemy z harmonogramem publikacji ujawniają się często w najgorszych momentach - o 6 rano w piątek, gdy planowałeś spokojny weekend.

### Cron jobs i task queues

Testowanie harmonogramów publikacji to więcej niż sprawdzenie, czy artykuł pojawi się o czasie. Musisz przewidzieć scenariusze jak zmiana czasu na letni, restart serwera w środku wykonywania zadania czy konflikt przy próbie publikacji dwóch artykułów jednocześnie.

Jeden z moich ulubionych testów sprawdza, co się dzieje gdy zadanie trwa dłużej niż interwał między uruchomieniami. Czy system uruchomi drugie zadanie równolegle? A może zacznie się bardzo nieładny race condition?

Retry logic wymaga szczególnej uwagi. Za mało prób i stracisz treść przez chwilowy błąd API. Za dużo i system będzie się dławił niepotrzebnym ruchem. Sweet spot to zwykle 3-5 prób z exponential backoff.

Error states są często pomijanym aspektem. Co robi twój agent, gdy external API zwraca 500? A gdy zabraknie miejsca na dysku? Dobre testy sprawdzają nie tylko happy path, ale przede wszystkim scenariusze awaryjne.

Monitoring długotrwałych procesów to sztuka sama w sobie. Process może wisieć godzinami bez żadnego komunikatu. Heartbeat monitoring i timeout'y powinny być integralną częścią każdego zadania.

### API integrations i webhooks

Mockowanie zewnętrznych serwisów pozwala kontrolować chaos. Twitter API może być niestabilny, WordPress czasem zwraca dziwne błędy. Mocki dają ci przewidywalność w testach i kontrolę nad edge cases.

Szczególnie przydatne są scenariuze partial failure. Co się dzieje, gdy publikacja na Facebooku się udaje, ale Twitter zwraca błąd? Czy system spróbuje ponownie tylko failed operations, czy zacznie od początku?

Rate limiting to pułapka czająca się na każdym kroku. Większość APIs ma limity, ale różnie je implementuje. GitHub liczy na godzinę, Twitter na 15-minutowe okna. Testy powinny symulować hitting these limits i sprawdzać graceful handling.

Error handling to nie tylko kwestia techniczna - to user experience. Gdy coś pójdzie źle, użytkownik powinien dostać sensowny komunikat, nie cryptic stack trace. Graceful degradation oznacza, że system kontynuuje pracę nawet gdy niektóre komponenty failują.