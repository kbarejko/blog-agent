#!/bin/bash
# Skrypt do publikacji artykułu (przeniesienie z drafts do published)

if [ -z "$1" ]; then
    echo "Użycie: ./publish.sh plik.md"
    echo ""
    echo "Dostępne drafty:"
    ls -1 articles/drafts/*.md 2>/dev/null | tail -5
    exit 1
fi

SOURCE="$1"
BASENAME=$(basename "$SOURCE")
DEST="articles/published/$BASENAME"

if [ ! -f "$SOURCE" ]; then
    echo "❌ Plik nie istnieje: $SOURCE"
    exit 1
fi

# Przenieś do published
mv "$SOURCE" "$DEST"

echo "✅ Artykuł opublikowany: $DEST"
echo "📝 Teraz możesz wgrać go na swoją platformę blogową"
