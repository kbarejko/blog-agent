# 📝 Workflow pracy z artykułami w konsoli

## 🚀 Szybki start

### 1. Zainstaluj narzędzia (jednorazowo)

```bash
# Edytor micro (polecany dla początkujących)
curl https://getmic.ro | bash
sudo mv micro /usr/local/bin/

# Narzędzia do podglądu Markdown
pip install glow rich-cli

# Opcjonalnie: bat (lepszy cat)
sudo apt install bat  # Debian/Ubuntu
```

### 2. Aktywuj aliasy (jednorazowo)

Dodaj do `~/.bashrc`:
```bash
source ~/blog-agent/.bash_aliases
```

Następnie:
```bash
source ~/.bashrc
```

## 🎯 Codzienne użycie

### Opcja A: Stwórz artykuł AI (automatycznie)

```bash
blog-ai "Jak zacząć z Docker"
```

AI automatycznie:
- Stworzy konspekt
- Napisze wszystkie sekcje
- Wykona audyt jakości
- Zapisze w `outputs/`

### Opcja B: Stwórz artykuł ręcznie

```bash
# 1. Utwórz nowy artykuł
blog-new "Mój pierwszy artykuł"

# 2. Edytuj
blog-edit articles/drafts/2025-11-06-moj-pierwszy-artykul.md

# 3. Podgląd
blog-preview articles/drafts/2025-11-06-moj-pierwszy-artykul.md

# 4. Opublikuj (przenieś do published)
blog-publish articles/drafts/2025-11-06-moj-pierwszy-artykul.md
```

### Opcja C: Hybrydowa (AI + ręczna edycja)

```bash
# 1. Wygeneruj AI
blog-ai "Temat artykułu"

# 2. Znajdź wygenerowany plik
blog-list

# 3. Skopiuj do drafts i edytuj
cp outputs/article_*.md articles/drafts/2025-11-06-moj-artykul.md
blog-edit articles/drafts/2025-11-06-moj-artykul.md

# 4. Podgląd
blog-preview articles/drafts/2025-11-06-moj-artykul.md

# 5. Opublikuj
blog-publish articles/drafts/2025-11-06-moj-artykul.md
```

## 📋 Wszystkie dostępne komendy

| Komenda | Opis |
|---------|------|
| `blog-new "Tytuł"` | Utwórz nowy pusty artykuł |
| `blog-ai "Temat"` | Wygeneruj artykuł AI |
| `blog-edit plik.md` | Edytuj artykuł |
| `blog-preview plik.md` | Podgląd artykułu |
| `blog-publish plik.md` | Przenieś do published |
| `blog-list` | Lista wszystkich artykułów |
| `blog-drafts` | Pokaż drafty |
| `blog-published` | Pokaż opublikowane |

## 🔧 Edytory - skróty klawiszowe

### Micro (polecany)
- `Ctrl+S` - Zapisz
- `Ctrl+Q` - Wyjdź
- `Ctrl+C/V/X` - Kopiuj/Wklej/Wytnij
- `Ctrl+F` - Szukaj

### Vim
- `i` - Tryb edycji
- `Esc` - Tryb normalny
- `:w` - Zapisz
- `:q` - Wyjdź
- `:wq` - Zapisz i wyjdź

### Nano
- `Ctrl+O` - Zapisz
- `Ctrl+X` - Wyjdź
- `Ctrl+K` - Wytnij linię
- `Ctrl+U` - Wklej

## 🎨 Struktura katalogów

```
blog-agent/
├── articles/
│   ├── drafts/          # Artykuły w trakcie pracy
│   ├── published/       # Gotowe artykuły
│   └── templates/       # Szablony artykułów
├── outputs/             # Wygenerowane przez AI
├── new_article.sh       # Utwórz nowy artykuł
├── preview.sh           # Podgląd artykułu
├── publish.sh           # Opublikuj artykuł
├── list_articles.sh     # Lista artykułów
└── .bash_aliases        # Aliasy do sourcowania
```

## 💡 Dobre praktyki

### Nazewnictwo plików
```bash
# Format: YYYY-MM-DD-slug.md
2025-11-06-wprowadzenie-do-docker.md
2025-11-06-best-practices-react.md
```

### Szablon artykułu
```markdown
# Tytuł Artykułu

**Data:** 2025-11-06
**Status:** Draft/Published
**Autor:** Twoje Imię

---

## Wprowadzenie
[treść]

## Główna część
[treść]

## Podsumowanie
[treść]

---

**Tagi:** docker, devops, tutorial
**Kategoria:** Technologia
```

### Workflow z Git (opcjonalnie)

```bash
# Inicjuj repo (jednorazowo)
git init
git add .
git commit -m "Initial commit"

# Codzienny workflow
git add articles/
git commit -m "Dodaj nowy artykuł: Tytuł"
git push
```

## 🚀 Zaawansowane

### Live preview z watchera

```bash
# Zainstaluj watch
sudo apt install watch

# Auto-refresh podglądu
watch -n 2 'glow articles/drafts/2025-11-06-artykul.md'
```

### Konwersja Markdown → HTML

```bash
# Zainstaluj pandoc
sudo apt install pandoc

# Konwertuj
pandoc article.md -o article.html
```

### Sprawdzanie pisowni

```bash
# Zainstaluj aspell
sudo apt install aspell aspell-pl

# Sprawdź pisownię
aspell check article.md
```

## 🔥 Przykładowy workflow (krok po kroku)

### Poniedziałek - Planowanie
```bash
blog-new "10 narzędzi DevOps na 2025"
blog-edit articles/drafts/2025-11-06-10-narzedzi-devops-na-2025.md
# Napisz konspekt i kluczowe punkty
```

### Wtorek - Pisanie
```bash
blog-edit articles/drafts/2025-11-06-10-narzedzi-devops-na-2025.md
# Napisz główną treść
blog-preview articles/drafts/2025-11-06-10-narzedzi-devops-na-2025.md
```

### Środa - Dopracowanie
```bash
blog-edit articles/drafts/2025-11-06-10-narzedzi-devops-na-2025.md
# Popraw, dodaj przykłady
blog-preview articles/drafts/2025-11-06-10-narzedzi-devops-na-2025.md
```

### Czwartek - Publikacja
```bash
blog-preview articles/drafts/2025-11-06-10-narzedzi-devops-na-2025.md
# Ostateczne sprawdzenie
blog-publish articles/drafts/2025-11-06-10-narzedzi-devops-na-2025.md
# Wgraj na bloga (WordPress, Medium, etc.)
```

## 🆘 Troubleshooting

### "Command not found"
```bash
# Sprawdź czy aliasy są załadowane
source ~/.bashrc
```

### "Glow/micro not found"
```bash
# Zainstaluj brakujące narzędzia
pip install glow rich-cli
curl https://getmic.ro | bash && sudo mv micro /usr/local/bin/
```

### "Permission denied"
```bash
# Uprawnienia do skryptów
chmod +x *.sh
```

---

**Gotowy do pracy?** Zacznij od:
```bash
blog-ai "Mój pierwszy artykuł z AI"
```
