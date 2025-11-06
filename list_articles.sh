#!/bin/bash
# Skrypt do listowania artykułów

echo "📝 ARTYKUŁY - DRAFTS"
echo "===================="
if ls articles/drafts/*.md 1> /dev/null 2>&1; then
    for file in articles/drafts/*.md; do
        title=$(grep -m 1 "^# " "$file" | sed 's/# //')
        words=$(wc -w < "$file")
        echo "  📄 $(basename "$file")"
        echo "     Tytuł: $title"
        echo "     Słowa: $words"
        echo ""
    done
else
    echo "  (brak artykułów)"
fi

echo ""
echo "✅ ARTYKUŁY - PUBLISHED"
echo "===================="
if ls articles/published/*.md 1> /dev/null 2>&1; then
    for file in articles/published/*.md; do
        title=$(grep -m 1 "^# " "$file" | sed 's/# //')
        words=$(wc -w < "$file")
        echo "  📄 $(basename "$file")"
        echo "     Tytuł: $title"
        echo "     Słowa: $words"
        echo ""
    done
else
    echo "  (brak artykułów)"
fi

echo ""
echo "📊 STATYSTYKI"
echo "===================="
draft_count=$(ls -1 articles/drafts/*.md 2>/dev/null | wc -l)
published_count=$(ls -1 articles/published/*.md 2>/dev/null | wc -l)
echo "  Drafts: $draft_count"
echo "  Published: $published_count"
echo "  Razem: $((draft_count + published_count))"
