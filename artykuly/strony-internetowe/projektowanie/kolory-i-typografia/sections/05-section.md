## Techniczne aspekty implementacji - od teorii do praktyki

Piękna typografia to jedno, ale czy Twoja strona załaduje się w rozsądnym czasie? Najelegantsza czcionka świata nie pomoże, jeśli klient odejdzie przed jej wyświetleniem. Google'owi potrzeba 3 sekund, żeby użytkownicy zaczęli uciekać ze strony.

### Optymalizacja czcionek dla szybkości strony

Web fonts dają pełną kontrolę nad wyglądem, ale kosztują prędkość. Każdy dodatkowy plik czcionki to kolejne zapytanie do serwera i kilkadziesiąt kilobajtów do pobrania. System fonts są błyskawiczne – już są na urządzeniu użytkownika. Arial, Times New Roman, Helvetica ładują się natychmiast.

Google Fonts to kompromis między pięknem a wydajnością. Serwery Google są szybkie, fonty zoptymalizowane, a cache'owanie sprawia, że kolejne wizyty są błyskawiczne. Wybierasz tylko potrzebne warianty – Regular i Bold zamiast całej rodziny o 12 wagach. Link rel="preconnect" w head'zie przyspiesza połączenie z fonts.googleapis.com.

Preloading najważniejszej czcionki to strzał w dziesiątkę. `<link rel="preload">` mówi przeglądarce: "pobierz to od razu". Fallback fonts to siatka bezpieczeństwa – jeśli custom font się nie załaduje, Arial wyświetli się natychmiast. Stack typograficzny `font-family: 'Open Sans', Arial, sans-serif` to standard.

### Responsywność kolorów i typografii

Twój gradient wygląda zjawiskowo na MacBooku, ale jak sprawuje się na tannim Androidzie w słońcu? Ekrany OLED pokazują kolory intensywniej niż LCD. Jasny tekst na ciemnym tle może "krwawić" na niektórych panelach.

Czcionki na mobile'u to osobny świat. 16px to minimum – mniejsze teksty zmuszają do powiększania. Palce są grubsze niż kursory myszy, więc przyciski potrzebują co najmniej 44px wysokości. iOS i Android różnie renderują te same fonty.

Dark mode zyskuje na popularności, ale czy firmy powinny go implementować? Zależy od branży. Netflix i Spotify – tak, oszczędza baterię i lepiej prezentuje treści. Kancelaria prawna czy klinika? Niekoniecznie. Ciemny motyw może podświadomie kojarzyć się z mniej poważnym podejściem. Jeśli decydujesz się na dark mode, przetestuj, czy Twoje kolory firmowe nadal budują zaufanie w ciemnej wersji.