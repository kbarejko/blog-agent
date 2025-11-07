## Optymalizacja wydajności i niezawodności

### Minimalizowanie flaky tests

Flaky tests to plaga każdego zespołu pracującego z automatyzacją E2E. Test, który dziś przechodzi zielony, jutro pada czerwony – bez żadnych zmian w kodzie. Po miesiącu nikt nie ufa testom, bo "znowu coś pada bez powodu".

Większość niestabilności ma swoje źródła w timing issues. Element ładuje się 2 sekundy, ale czasem 3. API odpowiada zwykle w 500ms, ale pod obciążeniem potrzebuje sekundy. Network hiccup powoduje timeout. Te scenariusze są przewidywalne, jeśli wiesz, gdzie szukać.

**Race conditions** są najczęstszym sprawcą problemów. JavaScript event handlers nie zdążyli się zarejestrować. CSS animation jeszcze trwa. Background process modyfikuje dane w trakcie testu. Identyfikacja tych sytuacji wymaga patience i detective work.

Analiza failed tests powinna być systematic. Czy test pada zawsze w tym samym miejscu? O konkretnej porze? Na specific environment? Pattern recognition pomoże ci znaleźć root cause szybciej niż random debugging.

**Retry mechanisms** to double-edged sword. Intelligent retry może uratować test od sporadycznego network glitch. Ale może też maskować prawdziwe problemy z aplikacją. Dobrą praktyką jest retry na poziomie operacji, nie całego testu.

Zamiast retry'ować cały 10-minutowy test suite, retry'uj konkretny click czy API call. Cypress robi to automatically w wielu przypadkach. Playwright pozwala na fine-grained control. Custom retry logic powinna logować attempts i reasons for failure.

**Monitoring failed tests** daje ci data-driven approach do stability. Który test pada najczęściej? O jakiej porze? W którym environment? Metryki pomagają priorytetyzować effort - lepiej naprawić jeden test, który pada w 20% przypadków, niż pisać pięć nowych.

Niektóre zespoły wprowadzają "flakiness threshold". Test, który pada częściej niż 5% runs, automatycznie ląduje w quarantine. Przestaje blokować deployment, ale nadal zbiera metryki. To practical compromise między ideałem a rzeczywistością production systems.

Kluczem jest treating test code jak production code. Code review, refactoring, monitoring i maintenance. Flaky tests nie są natural disaster - to debt, którą można systematycznie spłacać.