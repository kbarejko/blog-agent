## Analytics w biznesie: czym naprawdę jest i jakie pytania pomaga odpowiadać

Analytics to nie jedno narzędzie, tylko kilka warstw patrzenia na biznes. Web analytics mówi, skąd przychodzą użytkownicy i co robią na stronie. Product analytics pokazuje, jak korzystają z funkcji i gdzie blokuje ich przepływ. Marketing analytics ocenia skuteczność kampanii i kreacji. Revenue analytics spina to z przychodem, marżą i LTV, by pokazać realny zwrot z budżetu.

Słownik pojęć, który warto mieć wspólny:
- Zdarzenie (event) – atomowa akcja, np. view_item, add_to_cart, generate_lead.
- Użytkownik – osoba/ID korzystająca z produktu w czasie.
- Sesja – wygodna paczka zdarzeń w przedziale czasu, ale nie „prawda absolutna”.
- Konwersja – zdarzenie o wartości biznesowej (zakup, kwalifikowany lead).
- Cohorty – grupy startujące w tym samym momencie/warunku, użyte do retencji.
- LTV – łączna wartość klienta w czasie; CAC – koszt jego pozyskania.

GA4 opiera się na modelu zdarzeniowym. To elastyczniejsze niż Universal Analytics (sesje + kategorie akcji), bo każde działanie jest eventem z parametrami. Sesje nadal istnieją, ale są wtórne. Dzięki temu precyzyjniej zdefiniujesz konwersje, lejki i segmenty.

Pytania, które realnie rozwiążesz:
- Które kanały dowożą zysk, nie tylko kliknięcia? Porównaj CAC per kanał i segment z LTV na marży, użyj atrybucji data‑driven, by uwzględnić wsparcie górnego lejka.
- Gdzie hamuje wzrost w lejku? Mierz drop‑off: odsłona → klik CTA → start formularza → wysyłka → SQL/zakup. W e‑commerce dodaj add_to_cart → checkout → purchase z kompletnymi danymi koszyka (item_id, quantity, price).
- Jaki jest LTV:CAC w segmentach? Nowi vs powracający, kanał, kampania, kategoria produktu. Próg 3:1 brzmi zdrowo, ale licz na marży i z uwzględnieniem zwrotów.
- Ile sprzedaży generuje „góra lejka”? Po modelowaniu atrybucji sprawdź udział view‑through i wzrost zapytań brandowych. Weryfikuj testami wyłączeniowymi, gdy to możliwe.
- Co z długim cyklem sprzedaży? Połącz GA4 z CRM. Importuj statusy (MQL → SQL → Won), deduplikuj leady po stabilnym ID i dopinaj offline touchpointy (rozmowy, spotkania).
- Jak poprawić strony i ofertę? Analizuj scroll depth, click maps i time‑to‑interact. Często wygrywa prosty ruch: przesunięcie social proof wyżej, skrócenie formularza, jaśniejsze CTA.
- Gdzie przenieść budżet? Zidentyfikuj kampanie o niskim ROAS i niskiej inkrementalności. Przenieś środki do kanałów z lepszym dopasowaniem i sygnałami wartości (np. value‑based bidding, retencja/e‑mail, PMax z poprawnym feedem).

Efekt? Zamiast patrzeć na same kliknięcia, widzisz pełny obraz: koszt pozyskania, wartość w czasie i konkretne miejsca, w które warto włożyć kolejną złotówkę.