# 📋 Blog Agent - Ściągawka komend

## 🚀 Szybki start (jednorazowo)

```bash
./setup_environment.sh  # Zainstaluj wszystko
source ~/.bashrc        # Załaduj aliasy
```

---

## 📝 Podstawowe komendy

| Komenda | Opis | Przykład |
|---------|------|----------|
| `blog-new "Tytuł"` | Nowy artykuł (pusty szablon) | `blog-new "Docker w 2025"` |
| `blog-ai "Temat"` | Wygeneruj artykuł AI | `blog-ai "Wprowadzenie do Kubernetes"` |
| `blog-edit plik.md` | Edytuj artykuł | `blog-edit articles/drafts/2025-11-06-moj-artykul.md` |
| `blog-preview plik.md` | Podgląd Markdown | `blog-preview articles/drafts/2025-11-06-moj-artykul.md` |
| `blog-publish plik.md` | Przenieś draft→published | `blog-publish articles/drafts/2025-11-06-moj-artykul.md` |
| `blog-list` | Lista wszystkich artykułów | `blog-list` |
| `blog-drafts` | Pokaż drafty | `blog-drafts` |
| `blog-published` | Pokaż opublikowane | `blog-published` |

---

## 📂 Struktura plików

```
blog-agent/
├── articles/
│   ├── drafts/          ← Artykuły w trakcie pracy
│   ├── published/       ← Gotowe artykuły
│   └── templates/       ← Szablony
├── outputs/             ← Wygenerowane przez AI
└── *.sh                 ← Skrypty pomocnicze
```

---

## ⌨️ Skróty klawiszowe (Micro editor)

| Skrót | Akcja |
|-------|-------|
| `Ctrl+S` | Zapisz |
| `Ctrl+Q` | Wyjdź |
| `Ctrl+C` | Kopiuj |
| `Ctrl+V` | Wklej |
| `Ctrl+X` | Wytnij |
| `Ctrl+F` | Szukaj |
| `Ctrl+Z` | Cofnij |
| `Ctrl+Y` | Ponów |

---

## 🔄 Typowy workflow

### Opcja 1: 100% AI
```bash
blog-ai "Temat artykułu"
# Gotowe! Artykuł w outputs/
```

### Opcja 2: Ręczne pisanie
```bash
blog-new "Tytuł"                    # 1. Utwórz
blog-edit articles/drafts/...       # 2. Pisz
blog-preview articles/drafts/...    # 3. Podgląd
blog-publish articles/drafts/...    # 4. Opublikuj
```

### Opcja 3: AI + edycja
```bash
blog-ai "Temat"                     # 1. Wygeneruj AI
cp outputs/article_*.md articles/drafts/moj.md  # 2. Skopiuj
blog-edit articles/drafts/moj.md    # 3. Dopracuj
blog-publish articles/drafts/moj.md # 4. Opublikuj
```

---

## 🎯 Szybkie akcje

```bash
# Lista ostatnich 5 draftów
ls -lt articles/drafts/*.md | head -5

# Podgląd ostatniego draftu
blog-preview $(ls -t articles/drafts/*.md | head -1)

# Statystyki artykułu
wc -w articles/drafts/moj-artykul.md  # Liczba słów

# Konwersja Markdown → HTML
pandoc article.md -o article.html

# Sprawdzanie pisowni (PL)
aspell check -l pl article.md
```

---

## 🛠️ Zaawansowane

### Masowa konwersja
```bash
for file in articles/published/*.md; do
    pandoc "$file" -o "${file%.md}.html"
done
```

### Auto-refresh podglądu
```bash
watch -n 2 'glow articles/drafts/2025-11-06-artykul.md'
```

### Backup wszystkich artykułów
```bash
tar -czf articles-backup-$(date +%Y%m%d).tar.gz articles/
```

### Git workflow
```bash
git add articles/
git commit -m "Dodaj nowy artykuł"
git push
```

---

## 🔍 Wyszukiwanie

```bash
# Znajdź artykuły z frazą
grep -r "Docker" articles/

# Znajdź artykuły z tagiem
grep -r "Tag: docker" articles/

# Największe artykuły
wc -w articles/**/*.md | sort -n | tail -5
```

---

## 💡 Pro tips

- **Nazewnictwo:** `YYYY-MM-DD-slug.md` (np. `2025-11-06-docker-tutorial.md`)
- **Szablon:** Użyj `articles/templates/szablon-artykulu.md` jako punkt startowy
- **Backup:** Regularnie commituj do Git
- **Preview:** Zawsze sprawdź `blog-preview` przed publikacją
- **SEO:** Dodawaj tagi i kategorie do każdego artykułu

---

## 🆘 Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| `command not found` | `source ~/.bashrc` |
| Brak uprawnień | `chmod +x *.sh` |
| Glow nie działa | `pip install glow` lub użyj `cat` |
| Micro nie działa | Użyj `nano` lub `vim` |

---

## 📞 Pomoc

```bash
cat WORKFLOW.md          # Szczegółowy workflow
cat QUICKSTART.md        # Szybki start z Blog Agent
python3 examples.py      # Przykłady użycia AI
```

---

**Ostatnia aktualizacja:** 2025-11-06
**Wersja:** 1.0
