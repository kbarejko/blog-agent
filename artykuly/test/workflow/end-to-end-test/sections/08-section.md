### Debugging i troubleshooting workflow

Gdy test pada, zaczyna się prawdziwa praca. Czerwony status w CI/CD pipeline oznacza jedno – ktoś musi ustalić, co poszło nie tak. Dobrze zaprojektowany workflow debugowania różni się od chaotycznego grzebania w logach tym, że ma system.

**Skuteczne logowanie** zaczyna się od odpowiednich poziomów szczegółowości. Debug logs powinny mówić, co test robi w każdym kroku. Info logs pokazują kluczowe decision points. Error logs wskazują exact failure reason.

Większość frameworków oferuje built-in logging. Cypress wyświetla każdą komendę w real-time. Playwright ma verbose mode z network requests. Selenium wymaga własnej implementacji, ale daje pełną kontrolę.

Nie loguj wszystkiego. Zbyt dużo informacji to równie złe jak za mało. Focus na decision points i state changes. User login? Log success lub failure. API call? Log request i response status. Form submission? Log validation results.

**Screenshots i video recording** są worth more than thousand log lines. Obraz pokazuje, co test "widział" w momencie failure. Czy element był visible? Czy modal się otworzył? Czy loading spinner nadal kręcił?

Auto-screenshots przy failure to must-have feature. Cypress robi to automatically. Playwright również. Custom implementation w Selenium zajmuje pięć minut, ale saves hours of debugging.

Video recording idzie dalej. Zobacz cały flow wykonywania testu. Czasem problem nie leży w ostatnim kroku, ale w setup operations kilka minut wcześniej.

**Root cause analysis** wymaga systematic approach. First question: czy to application bug, czy test issue? Network timeout może oznaczać performance problem. Missing element często wskazuje na race condition.

Pattern recognition pomoże priorytetyzować effort. Test pada tylko o piątej rano? Database backup może blokować operations. Failure rate wzrasta w piątki? Deployment process może wprowadzać issues.

Nie wszystkie failed tests wymagają immediate action. Occasional network glitch to cost of doing business. Systematic pattern failures wymagają investigation.

Documentation każdego major debugging session będzie pomocna później. Known issues, workarounds i lessons learned saves time when similar problems appear.