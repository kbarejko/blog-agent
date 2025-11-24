## Checklist: Wdrożenie Responsywnego CSS w Twojej Firmie

- [ ] Sprawdź obecny poziom responsywności swojej strony za pomocą narzędzi deweloperskich (klawisz F12) i przetestuj, jak wygląda na różnych rozmiarach ekranu
- [ ] Dodaj meta tag viewport do sekcji `<head>` strony: `<meta name="viewport" content="width=device-width, initial-scale=1">` - to podstawa każdej responsywnej witryny
- [ ] Określ 3 główne breakpointy dla swojej branży: urządzenia mobilne (do 768px), tablety (768px-1024px) oraz komputery (od 1200px wzwyż)
- [ ] Napisz pierwsze media queries dla menu nawigacyjnego, najlepiej wykorzystując podejście mobile-first, które wydaje się bardziej praktyczne
- [ ] Zamień sztywne układy na Flexbox w przynajmniej jednej sekcji - może to być galeria produktów, sekcja referencji czy obszar "o nas"
- [ ] Zoptymalizuj kluczowe obrazy używając atrybutu `srcset`, który automatycznie dobierze odpowiedni rozmiar do konkretnego ekranu
- [ ] Dostosuj wielkości czcionek poprzez jednostki `rem` zamiast sztywnych pikseli i ustaw elastyczne rozmiary dla nagłówków H1-H3
- [ ] Przetestuj działanie strony na rzeczywistych urządzeniach - smartfonie, tablecie i komputerze stacjonarnym. Emulator to jedno, prawdziwe urządzenie to drugie
- [ ] Zmierz wydajność ładowania przed i po wprowadzonych zmianach za pomocą Google PageSpeed Insights - różnice mogą być zaskakujące
- [ ] Skonfiguruj Google Analytics tak, aby śledzić konwersje z urządzeń mobilnych i porównywać je z desktopem
- [ ] Stwórz listę najważniejszych podstron do przeprojektowania - prawdopodobnie będą to strona główna, oferta oraz kontakt
- [ ] Zaplanuj realny budżet i harmonogram wdrażania responsywności na pozostałych stronach witryny