#!/bin/bash
# Skrypt instalacyjny środowiska do pracy z artykułami Markdown

echo "🚀 Blog Agent - Instalacja środowiska do pracy z Markdown"
echo "=========================================================="
echo ""

# Kolory
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Funkcja sprawdzająca
check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 jest zainstalowany"
        return 0
    else
        echo -e "${RED}✗${NC} $1 nie jest zainstalowany"
        return 1
    fi
}

# Sprawdź Python i pip
echo "📦 Sprawdzanie podstawowych narzędzi..."
check_command python3
check_command pip3
echo ""

# Instalacja narzędzi Python
echo "📦 Instalacja narzędzi Markdown..."
pip3 install --user glow rich-cli 2>&1 | grep -v "Requirement already satisfied" || true
echo ""

# Instalacja micro editor
echo "📝 Instalacja editora micro..."
if ! check_command micro; then
    echo "   Instaluję micro..."
    curl -s https://getmic.ro | bash
    mkdir -p ~/.local/bin
    mv micro ~/.local/bin/ 2>/dev/null || sudo mv micro /usr/local/bin/
    echo -e "${GREEN}✓${NC} micro zainstalowany"
else
    echo "   micro już zainstalowany"
fi
echo ""

# Tworzenie struktury katalogów
echo "📁 Tworzenie struktury katalogów..."
mkdir -p articles/{drafts,published,templates}
mkdir -p outputs
echo -e "${GREEN}✓${NC} Katalogi utworzone"
echo ""

# Uprawnienia dla skryptów
echo "🔧 Ustawianie uprawnień..."
chmod +x new_article.sh preview.sh publish.sh list_articles.sh setup_environment.sh
echo -e "${GREEN}✓${NC} Uprawnienia ustawione"
echo ""

# Konfiguracja aliasów
echo "⚙️  Konfiguracja aliasów..."
BASHRC="$HOME/.bashrc"
ALIAS_LINE="source $PWD/.bash_aliases"

if grep -q "source.*\.bash_aliases" "$BASHRC" 2>/dev/null; then
    echo -e "${YELLOW}!${NC} Aliasy już skonfigurowane w ~/.bashrc"
else
    echo "" >> "$BASHRC"
    echo "# Blog Agent aliases" >> "$BASHRC"
    echo "$ALIAS_LINE" >> "$BASHRC"
    echo -e "${GREEN}✓${NC} Aliasy dodane do ~/.bashrc"
fi
echo ""

# Stwórz przykładowy szablon
echo "📝 Tworzenie przykładowego szablonu..."
cat > articles/templates/szablon-artykulu.md << 'EOF'
# [Tytuł Artykułu]

**Data:** YYYY-MM-DD
**Status:** Draft
**Autor:** [Twoje Imię]
**Kategoria:** [Technologia/Business/Lifestyle]
**Tagi:** [tag1, tag2, tag3]

---

## 🎯 Kluczowe informacje

- **Dla kogo:** [grupa docelowa]
- **Czas czytania:** [X minut]
- **Poziom:** [Początkujący/Średnio-zaawansowany/Zaawansowany]

---

## Wprowadzenie

[Wprowadzenie - hook, problem, obietnica wartości]

### Co się dowiesz z tego artykułu?

- [Punkt 1]
- [Punkt 2]
- [Punkt 3]

---

## [Sekcja 1]

[Treść sekcji 1...]

### [Podsekcja 1.1]

[Treść...]

**Przykład:**
```
[kod lub przykład]
```

**💡 Wskazówka:** [praktyczna rada]

---

## [Sekcja 2]

[Treść sekcji 2...]

---

## [Sekcja 3]

[Treść sekcji 3...]

---

## Podsumowanie

[Podsumowanie kluczowych punktów]

### Kluczowe wnioski:

1. [Wniosek 1]
2. [Wniosek 2]
3. [Wniosek 3]

### Następne kroki:

- [ ] [Akcja 1]
- [ ] [Akcja 2]
- [ ] [Akcja 3]

---

## Zasoby dodatkowe

- [Link 1](url)
- [Link 2](url)

---

**Autor:** [Twoje Imię]
**Data publikacji:** YYYY-MM-DD
**Ostatnia aktualizacja:** YYYY-MM-DD
EOF
echo -e "${GREEN}✓${NC} Szablon utworzony: articles/templates/szablon-artykulu.md"
echo ""

# Podsumowanie
echo "=================================================="
echo -e "${GREEN}✅ Instalacja zakończona!${NC}"
echo "=================================================="
echo ""
echo "📚 Następne kroki:"
echo ""
echo "1. Załaduj aliasy:"
echo "   source ~/.bashrc"
echo ""
echo "2. Stwórz pierwszy artykuł:"
echo "   blog-new 'Mój pierwszy artykuł'"
echo "   lub"
echo "   blog-ai 'Temat artykułu dla AI'"
echo ""
echo "3. Zobacz wszystkie dostępne komendy:"
echo "   - blog-new       # Nowy artykuł"
echo "   - blog-ai        # Generuj AI"
echo "   - blog-edit      # Edytuj"
echo "   - blog-preview   # Podgląd"
echo "   - blog-list      # Lista artykułów"
echo "   - blog-publish   # Opublikuj"
echo ""
echo "4. Przeczytaj workflow:"
echo "   cat WORKFLOW.md"
echo "   lub"
echo "   glow WORKFLOW.md  (jeśli zainstalowane)"
echo ""
echo "=================================================="
echo "🎉 Powodzenia w pisaniu artykułów!"
echo "=================================================="
