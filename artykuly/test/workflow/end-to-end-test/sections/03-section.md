## Projektowanie stabilnych testów E2E

### Architektura testów - Page Object Model i inne wzorce

Gdy masz już narzędzia i strategię, przychodzi czas na architekturę. Kod testowy różni się od application code, ale to nie znaczy, że może być chaotyczny. Bez przemyślanej struktury, po roku będziesz mieć setki plików z copy-paste'owanymi selektorami i duplikowaną logiką.

**Page Object Model** to wzorzec, który sprawdził się w tysiącach projektów. Zamiast pisać `cy.get('[data-testid="login-button"]')` w każdym teście, tworzysz klasę `LoginPage` z metodą `clickLoginButton()`. Brzmi banalnie? W praktyce to różnica między kodem, który żyje lata, a kodem do wyrzucenia po trzech miesiącach.

Przykład z życia: masz formularz logowania na pięciu różnych stronach. Designer zmienia placeholder w polu email. Bez POM edytujesz 15 plików testowych. Z POM? Jedna linia w `LoginForm` class.

Nie ograniczaj się tylko do pages. Komponenty wielokrotnego użytku, jak modalne okna czy dropdown menu, zasługują na własne klasy. Navigation bar, który pojawia się na każdej stronie, powinien mieć swój `NavigationComponent` z metodami `goToProfile()`, `logout()`, `searchFor(term)`.

**Custom commands** to kolejny level organizacji. Zamiast trzech linijek setupujących użytkownika w każdym teście, masz `cy.loginAsUser('admin')`. Playwright oferuje podobny mechanizm przez fixtures i custom methods.

Każdy framework ma swoje best practices. Cypress preferuje chainable commands, Playwright stawia na async/await pattern. Nie walcz z narzędziem – wykorzystaj jego strengths.

**Zarządzanie danymi testowymi** często bywa afterthought, a to błąd. Hardcoded strings w testach to maintenance nightmare. Test data powinny żyć w osobnych plikach – JSON, YAML, albo nawet prostych objektach JavaScript.

Lepiej mieć `userData.validAdmin` niż `email: 'admin@test.com'` rozrzucone po całym codebase. Gdy przyjdzie czas na zmianę domeny email, podzięku jesz sobie za tę decyzję.

Niektóre zespoły idą dalej i generują test data dynamicznie. `faker.js` potrafi stworzyć realistic user data on-the-fly. Ma to swoje plusy – każdy test run używa fresh data. Ale ma też minusy – debugging staje się trudniejszy, gdy nie wiesz dokładnie, jakie dane były użyte w failed test.