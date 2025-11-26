## Diagnoza wydajności - Gdzie szukać problemów

Zanim zaczniesz optymalizować, musisz wiedzieć, co dokładnie spowalnia Twoją stronę. To jak leczenie bez diagnozy – możesz trafić, ale równie dobrze możesz zmarnować czas i pieniądze na niewłaściwe działania.

### Narzędzia do testowania prędkości

Google PageSpeed Insights to pierwszy przystanek w diagnozie. Wklejasz adres strony, klikasz "Analizuj" i po chwili dostajesz ocenę od 0 do 100 punktów. Wynik poniżej 50 to czerwona lampka – strona wymaga natychmiastowej interwencji. Ponad 80 punktów oznacza dobrą wydajność. Narzędzie pokazuje konkretne problemy z sugestiami poprawy, ale pamiętaj – niektóre zalecenia są zbyt techniczne dla przeciętnego użytkownika.

GTmetrix i Pingdom oferują głębszą analizę. Widzisz tutaj, które konkretne pliki spowalniają ładowanie i ile czasu zajmuje każdy element. GTmetrix pokazuje "wodospad" – graficzną reprezentację kolejności ładowania zasobów. Jeśli jeden duży obraz blokuje całą stronę, od razu to zauważysz.

Core Web Vitals to nowe metryki Google'a, które bezpośrednio wpływają na pozycję w wyszukiwarce. Largest Contentful Paint mierzy, jak szybko ładuje się główna treść. First Input Delay sprawdza responsywność strony. Cumulative Layout Shift ocenia, czy elementy "skaczą" podczas ładowania. Google Search Console pokazuje te metryki dla całej witryny.

### Najczęstsze przyczyny spowolnień

W 70% przypadków problem leży w obrazach. Zdjęcie produktu o wadze 3 MB, które mogłoby ważyć 300 KB po kompresji, to klasyk gatunku. Format też ma znaczenie – stary PNG zamiast nowoczesnego WebP może zwiększyć czas ładowania o kilka sekund.

Wtyczki to druga plaga współczesnych stron. Każda wtyczka to dodatkowy kod do załadowania. Niektóre motywy WordPress ładują całe biblioteki CSS, żeby wyświetlić jeden przycisk. Sprawdź, czy rzeczywiście potrzebujesz tej wtyczki do sliderów z 47 opcjami, skoro używasz tylko podstawowej funkcji.

Hosting ma kluczowe znaczenie, ale często jest niedoceniany. Tani hosting współdzielony to jak próba jazdy Formula 1 traktorem. Stara wersja PHP czy przepełniona baza danych potrafią zamienić szybką stronę w ślimaka.

Brak cache'owania oznacza, że każde odwiedziny generują stronę od nowa. To jak przepisywanie tej samej książki za każdym razem, gdy ktoś chce ją przeczytać.