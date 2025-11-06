## Monitoring i wykrywanie zagrożeń

### Systemy wykrywania włamań (IDS/IPS)

Najlepsze zabezpieczenia niewiele znaczą, jeśli nie wiesz, kiedy ktoś próbuje je przełamać. Systemy wykrywania włamań działają jak czujny strażnik - obserwują ruch, rozpoznają wzorce ataków i alarmują o zagrożeniach w czasie rzeczywistym.

#### Monitorowanie ruchu w czasie rzeczywistym

IDS (Intrusion Detection System) to cyfrowy detektyw. Analizuje każdy pakiet danych, porównuje z bazą znanych ataków i wykrywa anomalie. Setki prób logowania na konto admin w ciągu minuty? To nie pomyłka, to atak brute force.

IPS (Intrusion Prevention System) idzie krok dalej - nie tylko wykrywa, ale też blokuje zagrożenia. Automatycznie dodaje podejrzane IP do czarnej listy, przerywa połączenia z malware'em, blokuje próby SQL injection.

Rozpoznawanie wzorców to serce systemu. Baza sygnatur zawiera "odciski palców" tysięcy znanych ataków. Bot skanujący popularne ścieżki jak "/wp-admin/", "/admin/", "/login.php" zostanie złapany w kilka sekund.

Automatyczne blokowanie IP wymaga delikatnej równowagi. Zbyt agresywne ustawienia zablokują prawdziwych klientów. Zbyt liberalne przepuszczą atakujących. Większość systemów używa progów: 5 nieudanych logowań w ciągu 15 minut = block na godzinę.

#### Analiza logów i anomalii

Logi to kronika życia twojego sklepu. Każde kliknięcie, każda transakcja, każda próba dostępu - wszystko jest zapisywane. Problem w tym, że dziennie powstają gigabajty danych. Przeanalizowanie ich ręcznie to misja niemożliwa.

Narzędzia jak ELK Stack (Elasticsearch, Logstash, Kibana) lub Splunk automatyzują analizę. Wyszukują wzorce, tworzą wizualizacje, wysyłają alerty o niepokojących trendach. Nagły wzrost błędów 404? Ktoś prawdopodobnie skanuje twoją stronę.

Baseline normalnej aktywności to punkt odniesienia dla anomalii. Twój sklep ma zwykle 1000 odwiedzin dziennie, a nagle pojawia się 50 tysięcy? To albo świetna promocja, albo atak DDoS. System powinien rozróżnić prawdziwy ruch od sztucznego.

### Web Application Firewall (WAF)

WAF to specjalistyczna ochrona dla aplikacji webowych. Tradycyjny firewall operuje na poziomie sieci - sprawdza porty i protokoły. WAF zagląda w treść żądań HTTP, rozumie strukturę stron internetowych.

Różnica jest kluczowa dla e-commerce. Normalny firewall przepuści żądanie POST do formularza kontaktowego. WAF sprawdzi, czy w polu "imię" nie próbuje się wykonać kodu JavaScript. To właśnie chroni przed atakami XSS (Cross-Site Scripting).

Reguły filtrowania można dostosować do specyfiki sklepu. Blokowanie żądań z określonych krajów, ograniczenia częstotliwości zapytań do API, ochrona przed automatami próbującymi tworzyć fałszywe konta.