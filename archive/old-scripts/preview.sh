#!/bin/bash
# Skrypt do podglądu artykułu Markdown

if [ -z "$1" ]; then
    echo "Użycie: ./preview.sh plik.md"
    echo ""
    echo "Dostępne artykuły w drafts:"
    ls -1 articles/drafts/*.md 2>/dev/null | tail -5
    exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "❌ Plik nie istnieje: $FILE"
    exit 1
fi

# Sprawdź dostępne narzędzia i użyj pierwszego dostępnego
if command -v glow &> /dev/null; then
    glow "$FILE"
elif command -v rich &> /dev/null; then
    rich "$FILE" --markdown
elif command -v bat &> /dev/null; then
    bat "$FILE" --language markdown
else
    cat "$FILE"
fi

# Statystyki
echo ""
echo "📊 Statystyki:"
echo "   Słowa: $(wc -w < "$FILE")"
echo "   Linie: $(wc -l < "$FILE")"
echo "   Znaki: $(wc -m < "$FILE")"
