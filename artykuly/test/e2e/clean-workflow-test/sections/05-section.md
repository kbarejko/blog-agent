## Patterns & best practices z prawdziwego życia

Teoria to jedno, a praktyka to drugie. W realnych projektach napotykasz problemy, których nie ma w dokumentacji. Timeout issues, które pojawiają się tylko w piątki po 15:00. Element, który czasem ładuje się w 200ms, a czasem potrzebuje 3 sekund. Database lock, który blokuje test setup.

Te problemy mają rozwiązania. Trzeba tylko wiedzieć gdzie szukać.

### Timing issues - koniec z flaky tests

Większość niestabilnych testów to problem z czekaniem. Developer dodaje `sleep(5000)` i mówi "teraz działa". Problem w tym, że aplikacja raz potrzebuje 2 sekundy, a raz 8.

**Explicit waits** to podstawa. Czekaj na konkretny stan, nie na czas. Element visible, request completed, spinner disappeared. Framework powinien checkować condition co kilkaset milisekund.

```javascript
// Źle
await page.waitForTimeout(5000);

// Dobrze  
await page.waitForSelector('[data-testid="results"]');
```

**Custom wait conditions** handle complex scenarios. API response plus DOM update plus CSS animation. One liner zamiast chain of separate waits.

Anti-pattern numer jeden? Fixed timeouts everywhere. Drugi? Implicit waits mixed z explicit waits. To recipe for confusion i random failures.

### Smart retry mechanisms

Retry logic brzmi jak duct tape solution. Ale w E2E testing ma sens. Network hiccups happen. Database locks occur. Third party services mają bad day.

Kluczowe pytanie: kiedy retry jest OK? Infrastructure issues - yes. Application bugs - never. Test powinien rozróżniać te scenariusze.

**Retry strategies** różnią się complexity. Simple: próbuj 3 razy z 1-second delay. Smart: exponential backoff z jitter. Advanced: różne strategie dla different error types.

Monitor retry frequency w CI. Jeden test retry'uje się 50% runs? To signal dla investigation, nie accepted behavior.

### Debugging kiedy wszystko się sypie

Dobry debugging tool może save hours of frustration. Screenshot z moment of failure. Video recording z 30 sekund before crash. Browser console logs z error details.

**Artifact collection** powinno być automatic. Test fails = artifacts collected. No manual intervention needed. CI job stores files, notification contains links.

Performance profiling reveals bottlenecks. Memory leaks, slow queries, heavy DOM operations. Sometimes test failure pokazuje real application problems.

Best investment? Custom error messages. "Login failed" vs "Login failed - email field not found, user database returned empty set, auth service timeout after 10s". Second one saves debug time.