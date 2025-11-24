## CSS Grid - zaawansowane układy grid'owe

Flexbox świetnie sprawdza się w jednym wymiarze, ale co jeśli potrzebujesz kontrolować zarówno wiersze, jak i kolumny? CSS Grid to odpowiedź na kompleksowe layouty, które wcześniej wymagały frameworków lub skomplikowanych tricków.

Grid używaj, gdy planujesz dwuwymiarowy układ. Portfolio produktów w siatce? Grid. Strona główna z headerem, sidebar'em, treścią i stopką? Zdecydowanie Grid. Flexbox pozostaje lepszy do nawigacji, przycisków w rzędzie czy prostych sekcji.

Podstawowa siatka wymaga dwóch właściwości. `grid-template-columns: repeat(3, 1fr)` tworzy trzy równe kolumny. `grid-gap: 20px` dodaje odstępy między elementami. `1fr` oznacza jedną część dostępnej przestrzeni – trzy kolumny `1fr` to podział 1:1:1.

```css
.product-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 20px;
}
```

Na mniejszych ekranach wystarczy zmienić liczbę kolumn w media query:

```css
@media (max-width: 768px) {
    .product-grid {
        grid-template-columns: 1fr;
    }
}
```

Różnica między `auto-fit` a `auto-fill` to subtelność z dużym wpływem na wygląd. `Auto-fit` rozciąga istniejące elementy, żeby wypełnić przestrzeń. `Auto-fill` tworzy puste kolumny, nawet gdy nie ma elementów. W praktyce `auto-fit` daje lepszy efekt wizualny.

### Przykłady użycia Grid w projektach komercyjnych

Portfolio usług zyskuje na przejrzystości dzięki Grid. Każda usługa w osobnej karcie, automatyczny podział na kolumny w zależności od ekranu. `grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))` zapewnia, że karty mają minimum 300px, ale rozciągają się proporcjonalnie.

Układy blogowe z sidebarami przestają być utrapieniem. Główna treść i sidebar w Grid to dwie linie kodu:

```css
.blog-layout {
    display: grid;
    grid-template-columns: 2fr 1fr;
    grid-gap: 40px;
}
```

Galerie zespołu automatycznie się reorganizują. Na desktop'ie cztery osoby w rzędzie, na tablecie dwie, na telefonie jedna. Grid sam liczy optymalne rozmiary bez JavaScript'u czy skomplikowanych obliczeń.