## Obsługa błędów i scenariuszy awaryjnych

Idealny workflow test to mit. W rzeczywistości użytkownicy klikają nie tam gdzie trzeba, internet się zacina, a zewnętrzne API odpowiadają błędem. Właśnie te scenariusze odróżniają dobry system od przeciętnego.

### Negative scenarios – serce workflow testingu

Większość zespołów testuje tylko happy path. Użytkownik wchodzi, kupuje, wychodzi zadowolony. Real world jest bezlitosny. Karta płatnicza odrzucona, timeout podczas płatności, server error w trakcie checkout.

Zacznij od symulacji network issues. Dodaj delay w API calls – 5 sekund zamiast 500 milisekund. Sprawdź czy loading indicator się pojawia. Czy user dostaje feedback o tym, co się dzieje? A może siedzi przed pustym ekranem?

Timeout scenarios ujawniają prawdę o aplikacji. Payment gateway nie odpowiada przez 30 sekund. Czy system gracefully wraca do poprzedniego kroku? Czy pokazuje zrozumiały komunikat? Czy użytkownik może spróbować ponownie bez tracenia danych?

### Błędy serwera w środku procesu

Server error 500 podczas kroku 3 z 7-krokarowego workflow to koszmarz. Użytkownik już zainwestował czas, może wprowadził dane karty. Co teraz?

Test powinien sprawdzić recovery path. Czy dane zostały zapisane? Czy po powrocie użytkownik może kontynuować od tego miejsca? Czy musi zaczynać od nowa? Te detale decydują o user experience.

Database connection issues zdarzają się częściej niż chcielibyśmy. W środku transakcji połączenie się zrywa. Proper error handling oznacza rollback zmian i jasny komunikat. Poor handling to corrupted data i confused users.

### Resilience mechanisms w praktyce

Retry logic to standard w modern applications. Ale czy działa poprawnie? Test powinien sprawdzić ile razy system próbuje ponownie. Czy implementuje exponential backoff? Czy eventually gives up?

Circuit breaker pattern chroni przed cascade failures. Gdy payment service nie odpowiada, system powinien szybko zwrócić error zamiast czekać na timeout. To lepsze user experience niż długie loading.

Fallback strategies ratują sytuację. Primary payment provider down? Przełącz na backup. Email service unavailable? Pokaż potwierdzenie na stronie i wyślij email później. Test powinien weryfikować te alternate paths.

Graceful degradation oznacza, że core functionality działa nawet gdy auxiliary services failują. Rekomendacje produktów nie działają? Pokaż popular items. Personalization down? Use defaults. System should degrade gracefully, not crash completely.

Human-readable error messages to podstawa. "Error 500" nic nie mówi użytkownikowi. "Payment temporary unavailable, please try again in a few minutes" już tak. Test powinien sprawdzać quality komunikatów błędów w każdym kroku workflow.