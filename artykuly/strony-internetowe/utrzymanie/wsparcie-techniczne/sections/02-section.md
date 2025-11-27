## Co obejmuje profesjonalne wsparcie techniczne strony internetowej

Profesjonalne wsparcie to zestaw konkretnych usług, nie pojedynczych reakcji na awarie. Na poziomie podstawowym zaczyna się od zarządzania aktualizacjami — rdzeń i wtyczki (WordPress/WooCommerce), sklepy Shopify czy komponenty w stackach headless muszą być regularnie patchowane. Do tego dochodzi obsługa konfliktów między pluginami i zapewnienie kompatybilności z wersją PHP/Node, bo to najczęstsza przyczyna nagłych błędów po update’ach.

Środowiska dev/stage/prod i wersjonowanie Git to standard: deployy powinny iść przez pipeline, z testami na stagingu i kontrolą wersji. Dobre wsparcie utrzymuje spójne workflow CI/CD i rollback‑plany. Hosting, serwery, CDN, DNS i certyfikaty SSL/TLS są zarządzane operacyjnie — nie wystarczy je skonfigurować raz, trzeba monitorować ich zdrowie i odnowienia certyfikatów.

Monitoring uptime 24/7 z jasnymi progami alertów i ścieżkami eskalacji to konieczność. Do tego zarządzanie domenami i rekordami DNS — błędny rekord TTL potrafi skasować ruch przez godziny. Security obejmuje regularne skany podatności, WAF, ochronę przed DDoS i rate limiting. Polityki haseł, MFA, granularne role i logowanie zdarzeń (audit logs) zmniejszają ryzyko wycieku dostępu.

Kopie zapasowe plus testy odtworzeniowe (o nich szerzej w sekcji DR) powinny być wykonywane automatycznie i okresowo weryfikowane. Na wydajność pracuje się optymalizacjami Core Web Vitals, tuningiem bazy danych i warstw cache — to bezpośrednio wpływa na konwersję. Małe prace rozwojowe — bugfixy, poprawki UX czy techniczne SEO — zwykle mieszczą się w abonamencie do pewnego limitu.

Co w abonamencie? Typowo pakiet obejmuje stałą liczbę godzin miesięcznie (np. 8–40 h) albo określoną liczbę zgłoszeń priorytetowych i secundarnych. Ważne, by w SOW było jasno napisane, co jest „sporadyczną poprawką”, a co wymaga osobnego projektu. Wsparcie może obejmować marketing/SEO jako moduł dodatkowy — techniczne SEO zwykle jest standardem, strategia treści i kampanie to często osobna usługa.

Kto jest właścicielem kodu i dostępów? Zasadniczo klient zachowuje prawa do kodu. Dostawca dostaje niezbędne dostępowe role (najlepiej przez mechanizmy tymczasowego dostępu, deploy keys, IAM) i dokumentuje wszelkie zmiany. Jasne reguły własności i przekazania dostępów przy zakończeniu współpracy to fundament bezpiecznego utrzymania.