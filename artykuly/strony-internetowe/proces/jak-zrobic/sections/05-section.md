## Etap 4: Implementacja techniczna - od kodu do działającej strony

Masz gotowy design i wybraną technologię. Teraz przychodzi moment, którego większość przedsiębiorców obawia się najbardziej - przekształcenie wizji w działającą stronę. To wcale nie musi być skomplikowane, jeśli podzielisz proces na logiczne etapy.

### Struktura HTML i CSS

Semantyczny HTML to fundament, który większość osób ignoruje na własną szkodę. Zamiast `<div class="menu">` użyj `<nav>`, zamiast `<div class="article">` - `<article>`. Google i inne wyszukiwarki lepiej rozumieją strukturę strony, co bezpośrednio przekłada się na pozycje w wynikach wyszukiwania.

Nagłówki H1, H2, H3 to nie tylko elementy wizualne. To hierarchia treści dla robotów Google. Jeden H1 na stronę (główny tytuł), H2 dla głównych sekcji, H3 dla podpunktów. Taka struktura pomaga użytkownikom korzystającym z czytników ekranu i poprawia SEO.

Responsywne CSS oznacza, że strona dostosowuje się do każdego ekranu. Media queries to narzędzia, które pozwalają definiować różne style dla telefonów, tabletów i komputerów. Zamiast sztywnych szerokości w pikselach, używaj jednostek relatywnych - procenty, em, rem. Flexbox i CSS Grid eliminują problemy z układami, które nie działają na różnych rozdzielczościach.

Optymalizacja obrazów ma ogromny wpływ na szybkość ładowania. Kompresuj zdjęcia do 80-90% jakości oryginalnej - różnica wizualna będzie niezauważalna, a rozmiar pliku spadnie o połowę. Formaty WebP oferują lepszą kompresję niż JPEG, ale zachowaj JPEG jako backup dla starszych przeglądarek.

### Funkcjonalności JavaScript

Interaktywne elementy sprawiają, że strona staje się żywa. Responsywne menu na telefonach, slider z opiniami klientów, formularze kontaktowe z walidacją w czasie rzeczywistym. Każda z tych funkcji wymaga kilku linii JavaScript, ale efekt jest natychmiastowy.

Formularze to kluczowy punkt kontaktu z klientami. Walidacja po stronie przeglądarki oszczędza czas użytkownikom - nie muszą wysyłać formularza, żeby dowiedzieć się, że źle wpisali email. Dodaj komunikaty pomocy przy polach, które mogą sprawiać problemy.

Integracje z zewnętrznymi API rozszerzają możliwości strony. Google Maps dla lokalizacji firmy, system płatności PayU dla sklepu internetowego, Google Analytics do śledzenia ruchu. Większość usług oferuje gotowe kody do wklejenia - nie musisz programować od zera.

Podstawowe zabezpieczenia to przede wszystkim walidacja danych wejściowych i HTTPS. Każdy formularz na stronie może być bramą dla ataków. Sprawdzaj długość przesyłanych danych, filtruj potencjalnie niebezpieczne znaki, używaj CAPTCHA przy formularzach kontaktowych.

### Testowanie na różnych urządzeniach

Cross-browser testing sprawdza, czy strona działa identycznie w Chrome, Firefox, Safari i Edge. Narzędzia jak BrowserStack pozwalają testować stronę na dziesiątkach kombinacji przeglądarek i systemów operacyjnych bez instalowania ich lokalnie.

PageSpeed Insights i Core Web Vitals to metryki, które Google bezpośrednio uwzględnia w rankingach. Największy wpływ na wyniki mają: rozmiar obrazów, ilość JavaScript i czas odpowiedzi serwera. Cel: wynik powyżej 90 punktów na urządzeniach mobilnych.

Najczęstsze problemy to formularz, który nie działa na iPhone'ach, menu rozwijane zasłaniające treść na tabletach, czy przyciski za małe na dotyk. Testuj na prawdziwych urządzeniach, nie tylko w symulatorze przeglądarki.