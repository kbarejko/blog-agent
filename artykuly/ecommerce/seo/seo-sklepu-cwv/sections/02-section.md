### Trzy kluczowe metryki Core Web Vitals

**LCP (Largest Contentful Paint)** – czas ładowania największego elementu

W praktyce sklep powinien osiągnąć LCP poniżej 2,5 sekundy. Brzmi prosto, ale rzeczywistość bywa brutalna. Główne zdjęcie produktu w rozdzielczości 4K może samo generować LCP na poziomie 8-10 sekund.

Największymi winowajcami są zwykle hero bannery na stronie głównej, galerie zdjęć produktów i nieoptymalizowane grafiki kategorii. Czasem problem leży głębiej – w wolnym serwerze, który przetwarza zapytania o bazę produktów jak żółw w syropie.

**FID (First Input Delay)** – responsywność na pierwsze działanie użytkownika

Google oczekuje FID poniżej 100 milisekund. To oznacza, że gdy ktoś kliknie „Dodaj do koszyka", reakcja musi nastąpić natychmiast. Problem w tym, że sklepy internetowe są pełne JavaScript – systemy płatności, kalkulatory dostaw, filtry produktów, chatboty.

Każdy skrypt walczy o zasoby przeglądarki. Użytkownik klika przycisk, ale JavaScript jest zajęty ładowaniem widżetu ocen produktu. Rezultat? Frustracja i porzucony koszyk.

**CLS (Cumulative Layout Shift)** – stabilność wizualna podczas ładowania

Wynik poniżej 0,1 to standard. W praktyce sklep ładuje się etapami: najpierw struktura, potem zdjęcia, na końcu reklamy i popupy. Każdy element może przesunąć inne, tworząc chaos na ekranie.

Klasyczny scenariusz: klient czyta opis produktu, nagle pojawia się banner rabatowy i przesuwa cały tekst. Albo jeszcze gorzej – użytkownik celuje w przycisk „Kup", ale w ostatniej chwili ładuje się reklama i klika przypadkowo w nią.

### Jak Google wykorzystuje CWV w procesie indeksacji

Google's Page Experience Update włączył Core Web Vitals do oficjalnych czynników rankingowych. Algorytm nie tylko sprawdza treść – analizuje też jakość doświadczenia użytkownika.

Proces wygląda tak: Googlebot odwiedza stronę, mierzy CWV i zapisuje wyniki. Dane z rzeczywistych użytkowników (Chrome User Experience Report) dopełniają obrazu. Strony z lepszymi metrykami dostają bonus w rankingu, szczególnie przy podobnej jakości treści.

To nie oznacza, że wolny sklep zniknie z wyników. Ale przy równej konkurencji wygra ten, który ładuje się szybciej i działa płynniej.