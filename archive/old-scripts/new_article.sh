#!/bin/bash
# Skrypt do szybkiego tworzenia nowego artykułu

if [ -z "$1" ]; then
    echo "Użycie: ./new_article.sh 'Tytuł artykułu'"
    exit 1
fi

TITLE="$1"
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
DATE=$(date +%Y-%m-%d)
FILENAME="articles/drafts/${DATE}-${SLUG}.md"

cat > "$FILENAME" << EOF
# $TITLE

**Data:** $DATE
**Status:** Draft
**Autor:**

---

## Wprowadzenie

[Wprowadzenie do artykułu...]

## Główna treść

[Główna treść artykułu...]

## Podsumowanie

[Podsumowanie...]

---

**Tagi:**
**Kategoria:**
EOF

echo "✅ Utworzono nowy artykuł: $FILENAME"
echo "📝 Otwórz go za pomocą: micro $FILENAME"
