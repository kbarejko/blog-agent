## Media queries - fundament responsywnego CSS

Media queries to instrukcje CSS, które mówią przeglądarce: "jeśli ekran ma taką szerokość, zastosuj te style". To jak mieć różne zestawy reguł dla różnych sytuacji. Gdy klient odwiedza stronę na telefonie, aktywują się style mobilne. Na tablecie – style tabletowe.

Podstawowa składnia wygląda tak:

```css
@media screen and (max-width: 768px) {
    .menu {
        display: block;
    }
}
```

Ta reguła oznacza: "dla ekranów do 768px szerokości, pokaż menu jako blok". `max-width` oznacza "maksymalnie tyle", a `min-width` to "co najmniej tyle". Większość projektów używa 3-4 głównych punktów kontrolnych.

W praktyce biznesowej sprawdzają się breakpoints oparte na rzeczywistych urządzeniach: 576px (duże telefony), 768px (tablety), 992px (laptopy), 1200px (desktopy). Te wartości pokrywają 90% urządzeń Twoich klientów.

Mobile-first oznacza pisanie stylów najpierw dla telefonów, potem rozszerzanie na większe ekrany. Desktop-first to odwrotnie. Dla biznesu mobile-first jest lepszy – zaczynasz od tego, co widzi większość klientów. Łatwiej też optymalizować wydajność.

### Praktyczne przykłady media queries

Dla tabletów (768px-1024px) typowy przykład to dwukolumnowy layout:

```css
@media (min-width: 768px) and (max-width: 1024px) {
    .product-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
    }
}
```

Smartfony (do 767px) wymagają pojedynczej kolumny i większych przycisków:

```css
@media (max-width: 767px) {
    .button {
        padding: 15px 30px;
        font-size: 18px;
    }
}
```

Duże ekrany (powyżej 1200px) pozwalają na więcej kolumn:

```css
@media (min-width: 1200px) {
    .services {
        grid-template-columns: repeat(4, 1fr);
    }
}
```

### Typowe błędy przy używaniu media queries

Największy błąd to zbyt wiele punktów kontrolnych. Niektórzy dodają breakpoint co 50px, co komplikuje kod i utrudnia utrzymanie. Trzech dobrze przemyślanych punktów wystarczy dla 95% projektów.

Ignorowanie orientacji urządzenia powoduje problemy z tabletami obróconymi poziomo. Telefon w poziomie może mieć szerokość tabletu w pionie. Użyj `orientation: landscape` lub `orientation: portrait` gdy potrzeba.

Testowanie tylko w narzędziach deweloperskich to pułapka. Prawdziwe urządzenia zachowują się inaczej – różne gęstości pikseli, różne przeglądarki. Przetestuj na fizycznym telefonie i tablecie przed publikacją.