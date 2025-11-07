### Obsługa elementów UI i asynchroniczności

Największym wyzwaniem w testach E2E nie są selektory czy kliki. To czas. Aplikacje webowe są asynchroniczne z natury. Dane ładują się z API. Animacje trwają sekundy. JavaScript renderuje komponenty stopniowo.

Twój test jest niecierpliwy. Chce kliknąć przycisk natychmiast. A przycisk jeszcze nie istnieje.

**Strategie oczekiwania** dzielą się na dwa obozy. Implicit waits to globalne timeouty. Ustawisz 10 sekund i każdy element będzie czekał maksymalnie tyle. Proste, ale nieefektywne.

Explicit waits są inteligentniejsze. Czekasz konkretnie na to, czego potrzebujesz. Element ma być visible? Czekasz na visibility. API ma zwrócić dane? Czekasz na network response.

Cypress robi to elegancko. `cy.contains('Submit')` automatycznie retry'uje przez 4 sekundy. Nie musisz myśleć o czekaniu. Playwright oferuje `page.waitForSelector()` z różnymi opcjami. Selenium wymaga więcej manual work, ale daje większą kontrolę.

**Dynamic content** to drugi poziom trudności. Komponenty pojawiają się i znikają. Loading spinnery zastępują prawdziwe dane. Dropdown menu ładuje opcje z backend.

Najgorszy błąd to hardcoded sleep. `cy.wait(5000)` w kodzie testowym to code smell. Test będzie czekał 5 sekund, nawet gdy dane załadują się w 100 milisekund. Albo gorsze - czasem 5 sekund nie wystarczy.

Lepsze podejście: czekaj na konkretny signal. Loading spinner zniknął? Perfect. Error message pojawił się? Też dobry znak. Element ma specific text content? Excellent.

**AJAX requests** potrafią wykiwać nawet doświadczonych testerów. Strona wygląda na załadowaną, ale w background leci jeszcze pięć API calls. Klikniesz przycisk i... nic. Albo error.

Network monitoring przychodzi z pomocą. Cypress ma `cy.intercept()`. Playwright oferuje `page.waitForResponse()`. Możesz powiedzieć testowi: czekaj, aż ten konkretny endpoint odpowie. Dopiero wtedy kontynuuj.

**Animacje i transitions** to ostatnia kategoria problemów. CSS animations mogą trwać sekundy. Element jest już w DOM, ale jeszcze się animuje. Selenium może próbować kliknąć w punkt, gdzie element będzie za 2 sekundy.

Niektóre zespoły wyłączają animacje w test environment. `* { transition: none !important; }` w CSS i po problemie. Inne preferują czekanie na animation completion.

Tu nie ma uniwersalnej recepty. Zależy od aplikacji i wymagań biznesowych. Ważne, żeby być świadomym problemu i mieć consistent approach w całym zespole.