## Typografia responsywna - czytelność na każdym ekranie

Dobra typografia na telefonie to różnica między klientem, który przeczyta o Twojej ofercie, a tym, który zrezygnuje po pierwszym akapicie. Obrazy można zmniejszyć, menu schować, ale tekst musi pozostać czytelny. To podstawa komunikacji z użytkownikiem.

Jednostka px to sztywny rozmiar – 16px ma zawsze 16 pikseli. Rem to rozmiar względny do głównej czcionki strony. Jeśli użytkownik powiększy czcionki w przeglądarce, rem się dostosuje, px nie. Em odnosi się do czcionki elementu rodzica i może prowadzić do nieprzewidywalnych efektów. Dla biznesu rem to bezpieczny wybór.

Viewport units skalują czcionkę z rozmiarem ekranu. `font-size: 4vw` oznacza 4% szerokości viewport'u. Na telefonie 400px to 16px czcionki, na desktop'ie 1200px to 48px. Działa świetnie dla nagłówków, gorzej dla tekstu głównego:

```css
h1 {
    font-size: clamp(24px, 4vw, 48px);
}
```

Optymalne rozmiary to 14-16px na telefonie, 16-18px na desktop'ie dla tekstu głównego. Nagłówki mogą być 1.5-2 razy większe. Mniejsze czcionki męczą wzrok na małych ekranach, większe marnują przestrzeń.

Line-height między 1.4-1.6 zapewnia czytelność na wszystkich urządzeniach. Za mało miejsca sprawia, że linie się zlewają. Za dużo powoduje gubienie się w tekście. Spacing między akapitami powinien być większy na telefonie – 1.5-2em zamiast 1em z desktop'a.

### Hierarchia typograficzna na urządzeniach mobilnych

Nagłówki na telefonie wymagają przeproporcjonowania. Desktop'owy H1 60px na telefonie zajmuje połowę ekranu. Skala 1.25-1.5 między poziomami nagłówków sprawdza się lepiej niż tradycyjna 1.618.

Kontrast czarnego tekstu na białym tle wynosi 21:1, ale 4.5:1 to minimum dla dostępności. Szary tekst #666 na białym daje 5.74:1 – wystarczy dla większości użytkowników, łagodniejszy dla oka niż czysty czarny.