## Bezpieczeństwo i ciągłość działania: od backupów po disaster recovery

Zasada 3‑2‑1 to fundament: trzy kopie, na dwóch różnych nośnikach, jedna off‑site. Codzienne backupy bazy i plików, tygodniowe snapshoty i retencja dopasowana do wymagań prawnych i biznesowych (np. 30–90 dni dla danych transakcyjnych). Kopie off‑site oraz szyfrowanie w spoczynku i w tranzycie minimalizują ryzyko utraty i wycieku.

Testy odtworzeniowe muszą być rutyną. Co kwartał przeprowadź „fire drill”: przywrócenie backupu na środowisku testowym, weryfikacja integralności danych i pełna dokumentacja. To nie jest luksus — to jedyny sposób, by mieć pewność, że kopie działają.

Patch management obejmuje nie tylko CMS i wtyczki. To także system operacyjny, serwer www i zależności. Plan patchowania z oknami serwisowymi, testami na stagingu i rollback‑planem zmniejsza ryzyko regresji po update’ach.

Security by design: zasada least privilege, izolacja środowisk i rotacja kluczy/sekretów. Dostępy przyznawaj czasowo (temporary access), używaj deploy keys i IAM. Regularna rotacja tokenów i tajnych kluczy ogranicza wewnętrzne ryzyko.

Logi i analiza to oczywistość. Centralny SIEM, agregacja logów, alerty anomalii i korelacja zdarzeń pozwalają wykryć atak szybciej. Warto integrować Sentry dla błędów aplikacji, UptimeRobot dla uptime i Grafana/Prometheus dla metryk wydajności.

WAF, reguły bot management i rate limiting chronią przed DDoS i złośliwym ruchem. Aktualizowane reguły WAF i monitoring botów zmniejszają obciążenie i fałszywe transakcje.

Procedury IR powinny być spisane: identyfikacja, containment, recovery i post‑mortem. Każdy incydent kończy się raportem z wnioskami i planem działań naprawczych.

Aspekty prawne i prywatność: rejestr czynności przetwarzania, umowy powierzenia danych i pseudonimizacja tam, gdzie to możliwe. Minimalizuj zbierane dane i stosuj jasną politykę retencji oraz cookie. Dla sklepów — zgodność z PCI DSS zależna od modelu płatności.

Szybkie liczby: RTO dla P1: 2–4 godziny; RPO dla krytycznych danych: ≤15 minut. Rozważ DR w innej chmurze lub regionie, jeśli ryzyko awarii dostawcy lub wymagania compliance tego uzasadniają — na przykład przy globalnych kampaniach sprzedażowych lub krytycznych SLA dla klientów.