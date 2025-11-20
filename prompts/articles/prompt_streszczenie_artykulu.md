# 📌 Streszczenie artykułu - "Co znajdziesz w artykule?"

**Zadanie:**
Na podstawie gotowego konspektu artykułu, stwórz krótką sekcję wprowadzającą "Co znajdziesz w artykule?", która pomoże czytelnikowi szybko zdecydować, czy warto czytać cały materiał.

## 🔖 Dane wejściowe
- **Tytuł artykułu:** `{{TYTUL_ARTYKULU}}`
- **Konspekt artykułu:** `{{KONSPEKT_TRESC}}`
- **Grupa docelowa:** `{{TARGET_AUDIENCE}}`

## ✍️ Wymagania

### 1. Format i struktura
```markdown
## Co znajdziesz w artykule?

- **Punkt 1** - Zwięzły opis pierwszej kluczowej wartości/wniosku (1 zdanie)
- **Punkt 2** - Kolejna kluczowa wartość/wniosek (1 zdanie)
- **Punkt 3** - Następna wartość/wniosek (1 zdanie)
- **Punkt 4** - Opcjonalnie (jeśli artykuł ma więcej kluczowych punktów)
- **Punkt 5** - Opcjonalnie (maksymalnie 5 punktów)
```

### 2. Zasady tworzenia

**TO NIE JEST spis treści!**
- ❌ NIE wymieniaj tytułów sekcji
- ❌ NIE kopiuj nagłówków z konspektu
- ❌ NIE używaj fraz typu "W artykule omówimy...", "Dowiesz się o..."

**TO JEST streszczenie wartości:**
- ✅ Konkretne wnioski i praktyczne wskazówki
- ✅ Najważniejsze informacje, które czytelnik zyska
- ✅ Kluczowe insights lub rozwiązania problemów
- ✅ Rzeczywista wartość, którą artykuł dostarcza

### 3. Charakterystyka punktów

Każdy punkt powinien:
- Być **konkretny** - nie ogólniki typu "poznasz metody", ale "SSL/TLS chroni dane klientów przed przechwyceniem"
- Być **actionable** lub **informacyjny** - wartość praktyczna lub wiedza
- Mieć **1-2 zdania maksymalnie** (preferowane: 1 zdanie)
- Zaczynać się od **pogrubionej frazy kluczowej** (2-4 słowa) + rozwinięcie
- Być napisany w sposób **bezpośredni** - bez "dowiesz się", "poznasz"

### 4. Ton i styl
- **Ekspercki, ale przystępny** - profesjonalna wiedza, zrozumiały język
- **Konkretny** - liczby, fakty, rozwiązania
- **Wartościowy** - każdy punkt to realna korzyść dla czytelnika
- **Bez clickbait** - nie obiecuj więcej niż artykuł dostarcza
- **Spójny z resztą artykułu** - zachowaj ton określony w `{{TARGET_AUDIENCE}}`

### 5. Umiejscowienie
Sekcja "Co znajdziesz w artykule?" pojawia się:
- **PO** tytule H1
- **PRZED** wprowadzeniem
- Na samym początku artykułu

```markdown
# Tytuł artykułu

## ⚠️ Częste błędy - UNIKAJ

1. **Duplikowanie wprowadzenia** - streszczenie ≠ pierwsze akapity artykułu
2. **Zbyt ogólne stwierdzenia** - "dowiesz się o metodach optymalizacji" (jakich?)
3. **Za długie punkty** - powyżej 2 zdań to już nie streszczenie
4. **Brak konkretów** - liczby, fakty, narzędzia sprawiają że punkt jest wartościowy
5. **Ton akademicki** - "artykuł omawia kwestie..." zamiast "RODO wymaga 5 działań..."
6. **Spis treści w przebraniu** - jeśli punkty = tytuły sekcji, robisz to źle

**Pamiętaj:** To pierwsze co przeczyta użytkownik po tytule. Decyduje czy scrolluje dalej, czy zamyka kartę.
