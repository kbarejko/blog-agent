#!/bin/bash
#
# Generate SEO headers alternatives for all articles in the tree
#
# Usage:
#   ./generate_headers_alternatives_all.sh [directory]
#
# Examples:
#   ./generate_headers_alternatives_all.sh                    # Process all articles
#   ./generate_headers_alternatives_all.sh artykuly/ecommerce # Process only ecommerce series
#

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default directory
SEARCH_DIR="${1:-artykuly}"

# Activate virtual environment
source .venv/bin/activate

echo -e "${BLUE}🔍 Searching for articles in: ${SEARCH_DIR}${NC}"
echo ""

# Find all config.yaml files
configs=$(find "$SEARCH_DIR" -name "config.yaml" -type f | sort)

# Count articles
total=$(echo "$configs" | wc -l)
current=0
success=0
failed=0

echo -e "${BLUE}📊 Found ${total} articles${NC}"
echo ""

# Process each article
while IFS= read -r config_path; do
    current=$((current + 1))

    # Extract article path (directory containing config.yaml)
    article_dir=$(dirname "$config_path")

    # Extract article name from config
    article_name=$(grep "^title:" "$config_path" | sed 's/title: *//' | tr -d '"' || echo "Unknown")

    echo -e "${BLUE}[${current}/${total}] Processing: ${article_name}${NC}"
    echo -e "   Path: ${article_dir}"

    # Check if article.md exists (required for headers_alternatives)
    if [ ! -f "${article_dir}/article.md" ]; then
        echo -e "   ${YELLOW}⚠️  Skipping - article.md not found${NC}"
        echo ""
        continue
    fi

    # Run headers_alternatives step
    if python -m blog_agent create --config "$config_path" --only headers_alternatives 2>&1 | grep -q "✅ Headers alternatives saved"; then
        success=$((success + 1))
        echo -e "   ${GREEN}✅ Generated headers_alternatives.md${NC}"
    else
        failed=$((failed + 1))
        echo -e "   ${RED}❌ Failed to generate alternatives${NC}"
    fi

    echo ""
done <<< "$configs"

# Summary
echo ""
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}📊 Summary${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "Total articles:    ${total}"
echo -e "${GREEN}Successful:        ${success}${NC}"
if [ $failed -gt 0 ]; then
    echo -e "${RED}Failed:            ${failed}${NC}"
fi
echo -e "${BLUE}════════════════════════════════════════${NC}"
