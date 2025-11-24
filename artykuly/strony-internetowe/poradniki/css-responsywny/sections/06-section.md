## Responsywne obrazy i media - optymalizacja dla wszystkich urządzeń

Obrazy mogą zapewnić sukces lub zrujnować responsywną stronę. Duży banner, który świetnie wygląda na desktop'ie, zamienia telefon w tartę z powodu długiego ładowania. Z drugiej strony zbyt mała grafika na dużym ekranie wygląda amatorsko i psuje wizerunek firmy.

Technika srcset rozwiązuje ten problem elegancko. Przygotowujesz kilka wersji tego samego obrazu w różnych rozmiarach, a przeglądarka wybiera odpowiednią:

```html
<img src="product-400.jpg" 
     srcset="product-400.jpg 400w, 
             product-800.jpg 800w, 
             product-1200.jpg 1200w"
     sizes="(max-width: 768px) 100vw, 50vw">
```

Atrybut sizes informuje przeglądarkę, jak duży będzie obraz na danym ekranie. Na telefonie zajmie całą szerokość (100vw), na desktop'ie połowę (50vw). Przeglądarka sama wybiera optymalny rozmiar.

Responsywne wideo wymaga podobnego podejścia. YouTube i Vimeo dają responsywne embed'y, ale iframe'y trzeba opakowywać:

```css
.video-wrapper {
    position: relative;
    padding-bottom: 56.25%; /* 16:9 */
    height: 0;
}
.video-wrapper iframe {
    position: absolute;
    width: 100%;
    height: 100%;
}
```

### Narzędzia do optymalizacji obrazów

WebP i AVIF to nowoczesne formaty, które ważą 30-50% mniej niż JPEG przy tej samej jakości. WebP obsługuje 95% przeglądarek, AVIF zyskuje popularność. Użyj elementu `<picture>` do fallback'u:

```html
<picture>
    <source srcset="hero.avif" type="image/avif">
    <source srcset="hero.webp" type="image/webp">
    <img src="hero.jpg" alt="Opis">
</picture>
```

Automatyczne generowanie rozmiarów oszczędza czas. Narzędzia jak ImageMagick lub online'owe serwisy tworzą wszystkie potrzebne wersje jednym kliknięciem.

CDN (Content Delivery Network) przyspiesza ładowanie obrazów o 40-60%. Serwisy jak Cloudflare lub Amazon CloudFront dostarczają obrazy z serwerów najbliżej użytkownika. Klient z Warszawy pobiera zdjęcia z polskiego serwera, nie amerykańskiego.