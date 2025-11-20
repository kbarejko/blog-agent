## Najczęstsze błędy i jak ich unikać

Właściciel salonu kosmetycznego próbował samodzielnie dodać cennik. Po godzinie strona wyglądała jak pole bitwy – tekst się nakładał, obrazy znikały, nawigacja przestała działać. Winne były podstawowe błędy HTML.

### Błędy początkujących

Niepoprawne zagnieżdżanie tagów to najczęstsza pułapka. Otwierasz `<div>`, potem `<p>`, ale zamykasz `</div>` przed `</p>`. Przeglądarka się myli, struktura się rozpada. Złota zasada: ostatni otwarty, pierwszy zamknięty.

Pomijanie atrybutów `alt` w obrazkach krzywdzi biznes. Google nie widzi obrazu bez opisu, osoby niewidome słyszą tylko "obrazek". Zamiast `<img src="salon.jpg">` napisz `<img src="salon.jpg" alt="wnętrze salonu fryzjerskiego - fotel i lustro">`.

Nadużywanie `<br>` zamiast właściwej struktury to jak budowanie domu z taśmy klejącej. Pięć znaczników `<br>` dla odstępu między sekcjami? Użyj tagów `<section>` i CSS. HTML określa strukturę, nie wygląd.

### Problemy biznesowe wynikające ze złego HTML

Chaos w kodzie to spadek w Google. Wyszukiwarki nie potrafią zrozumieć źle zbudowanej strony. Brakujące nagłówki `<h1>`, przeskakiwanie z `<h2>` na `<h5>` – algorytmy gubią się w treści.

Niedostępność dla osób niepełnosprawnych to utraceni klienci i potencjalne problemy prawne. Czytniki ekranu nie obsłużą strony bez semantycznych tagów. Tag `<button>` zamiast `<div>` z napisem "kliknij" – drobna różnica o wielkich konsekwencjach.

Źle napisany HTML to koszmar dla przyszłych zmian. Programista potrzebuje dwukrotnie więcej czasu na przepisanie chaosu niż na budowę od nowa. To wprost przekłada się na rachunki.