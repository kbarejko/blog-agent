## Przypadki użycia - kiedy Next.js to najlepszy wybór

Nie każdy projekt potrzebuje Next.js, ale gdy pasuje – to idealnie. Po latach pracy z różnymi frameworkami widzę wyraźne wzorce. Niektóre typy projektów wręcz proszą się o Next.js, inne lepiej sprawdzają się w innych technologiach.

### Idealne projekty dla Next.js

E-commerce to naturalne środowisko dla Next.js. Statyczne strony kategorii ładują się błyskawicznie. Dynamiczne strony produktów generują się na żądanie. SEO działa automatycznie – każdy produkt ma poprawne meta tagi i structured data. Koszyk i checkout działają jako Client Components. Integracja z płatnościami? API Routes załatwiają sprawę bez dodatkowego backendu.

Corporate websites kochają Next.js za profesjonalny wygląd w kodzie źródłowym. Landing pages osiągają Lighthouse score 95+ bez wysiłku. A/B testy uruchamiają się przez Middleware. Formularze kontaktowe działają przez API Routes. Multi-language? i18n support jest wbudowany.

SaaS applications to kolejny sweet spot. Dashboard ładuje się przez Server Components. Interaktywne elementy działają po stronie klienta. Authentication przez NextAuth.js. Billing integration przez Stripe. Wszystko w jednym repozytorium, jeden deployment.

Content-heavy sites jak blogi czy portale informacyjne? Next.js może zastąpić WordPress w wielu przypadkach. ISR odświeża artykuły automatycznie. CMS headless integruje się bezproblemowo. SEO na najwyższym poziomie. Komentarze i newsletter przez API Routes.

### Kiedy rozważyć alternatywy

Aplikacje mobilne native to inna liga. React Native ma więcej sensu niż Next.js w PWA. Dostęp do kamer, GPS-a, notyfikacji push – native APIs działają lepiej. Sklepy z aplikacjami wymagają dedykowanych rozwiązań.

Real-time applications potrzebują WebSocket-ów i stałych połączeń. Chat, gry online, collaborative editing – tu sprawdzi się Socket.io z Express.js. Next.js może obsłużyć real-time, ale nie jest do tego zoptymalizowany.

Bardzo proste strony statyczne to overkill dla Next.js. Wizytówka firmy z trzema podstronami? Gatsby, Jekyll czy zwykły HTML będą szybsze do zbudowania. Next.js wnosi kompleksowość, która nie zawsze jest potrzebna.

Legacy systemy mają swoje ograniczenia. Stary backend nie wspiera JSON API? Baza danych bez REST-a? Zespół programistów PHP bez doświadczenia JavaScript? Czasem refactor całego systemu kosztuje więcej niż przynosi korzyści.

Kluczem jest realistyczna ocena projektu i zasobów zespołu.