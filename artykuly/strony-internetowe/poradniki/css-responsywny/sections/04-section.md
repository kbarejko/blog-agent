## Flexbox - elastyczne układy bez bólu głowy

Media queries to fundament, ale to Flexbox sprawia, że elementy naprawdę się adaptują. Wyobraź sobie tradycyjny layout jak meble przykręcone do ściany – żeby je przestawić, musisz odkręcać śruby. Flexbox to meble na kółkach, które same znajdą najlepsze miejsce.

Główna przewaga Flexbox to automatyczne rozdzielanie przestrzeni. Masz trzy elementy w rzędzie? Flexbox sam je wyrówna, niezależnie od szerokości ekranu. Jeden element się zmienia? Pozostałe automatycznie się dostosują. To koniec z obliczaniem procentów i martwymi punktami na średnich rozdzielczościach.

Podstawowe właściwości to trzy linie kodu, które załatwiają 80% problemów z layoutem. `display: flex` włącza tryb elastyczny. `justify-content: space-between` rozdziela elementy równomiernie. `align-items: center` wycentrowuje je pionowo. Nie ma float'ów, clear'ów ani position: absolute.

```css
.navigation {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
```

Responsywne menu to częsty ból głowy. Z Flexbox wystarczy dodać `flex-wrap: wrap`, a elementy same przejdą do następnej linii, gdy zabraknie miejsca. Na dużych ekranach masz poziome menu, na średnich łamie się w logicznych punktach.

Układy kolumnowe zyskują supermoce dzięki `flex-grow`. Główna treść może mieć `flex-grow: 2`, sidebar `flex-grow: 1`. Oznacza to podział 2:1, niezależnie od rozdzielczości. Sidebar zawsze zajmie trzecią część, reszta należy do treści.

### Praktyczne zastosowania Flexbox w biznesie

Galerie produktów przestają być problemem. Karty produktów z różną długością opisów? `align-items: stretch` sprawi, że wszystkie będą tej samej wysokości. Ceny zawsze będą na dole, niezależnie od długości nazwy produktu.

Sekcje "o nas" z profilami zespołu wyglądają profesjonalnie dzięki automatycznemu wyrównaniu. Jeden pracownik ma dłuższy opis doświadczenia? Pozostałe karty dostosują wysokość. `justify-content: space-evenly` rozłoży je równomiernie.

Stopki to klasyczny przykład, gdzie Flexbox błyszczy. `justify-content: space-between` umieści logo z lewej, menu w środku, kontakt z prawej. Na telefonie wszystko może się ułożyć pionowo dzięki `flex-direction: column` w media query. Żadnych float'ów, które się rozjeżdżają.

Flexbox rozwiązuje problemy, o których istnieniu nawet nie wiedziałeś. Centrowanie elementów pionowo, które kiedyś wymagało tricków, teraz to jedna właściwość.