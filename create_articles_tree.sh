#!/bin/bash
# Create Article Directory Structure from YAML
# Tworzy strukturę katalogów artykułów na podstawie pliku YAML

# set -e

# Kolory
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Domyślne wartości
YAML_FILE="article_structure.yaml"
BASE_DIR="artykuly"
DRY_RUN=false
CREATE_FILES=false

# Parsowanie argumentów
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--file)
            YAML_FILE="$2"
            shift 2
            ;;
        -o|--output)
            BASE_DIR="$2"
            shift 2
            ;;
        -n|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -c|--create-files)
            CREATE_FILES=true
            shift
            ;;
        -h|--help)
            echo "Użycie: $0 [opcje]"
            echo ""
            echo "Opcje:"
            echo "  -f, --file FILE       Plik YAML z definicją struktury (domyślnie: article_structure.yaml)"
            echo "  -o, --output DIR      Katalog docelowy (domyślnie: artykuly)"
            echo "  -n, --dry-run         Tylko wyświetl co zostanie utworzone, bez tworzenia"
            echo "  -c, --create-files    Utwórz domyślne pliki (config.yaml, outline.md)"
            echo "  -h, --help            Pokaż tę pomoc"
            echo ""
            echo "Przykłady:"
            echo "  $0                              # Użyj domyślnych wartości"
            echo "  $0 -n                           # Tryb dry-run (podgląd)"
            echo "  $0 -c                           # Twórz z domyślnymi plikami"
            echo "  $0 -f custom.yaml -o output     # Własny plik i katalog"
            exit 0
            ;;
        *)
            echo -e "${RED}Nieznana opcja: $1${NC}"
            echo "Użyj -h lub --help aby zobaczyć pomoc"
            exit 1
            ;;
    esac
done

# Sprawdź czy plik YAML istnieje
if [ ! -f "$YAML_FILE" ]; then
    echo -e "${RED}❌ Plik $YAML_FILE nie istnieje!${NC}"
    exit 1
fi

# Parser YAML - używa Pythona (dostępny w projekcie)
parse_yaml() {
    local yaml_file="$1"
    python3 -c "
import sys
import yaml

try:
    with open('$yaml_file', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    structure = data.get('structure', {})
    default_files = data.get('default_files', [])

    def process_item(key, value, series='', silo=''):
        '''Rekurencyjnie przetwarza strukturę YAML'''
        if isinstance(value, list):
            # Lista artykułów
            for article in value:
                if series:
                    # Hierarchiczne: series/silo/article
                    print(f'{series}|{silo or key}|{article}')
                else:
                    # Płaskie: silo/article (silo = key)
                    print(f'{key}|{article}|')
        elif isinstance(value, dict):
            # Zagnieżdżona struktura (series z silosami)
            for sub_key, sub_value in value.items():
                process_item(sub_key, sub_value, series=key, silo=sub_key)
        elif isinstance(value, str):
            # Pojedynczy artykuł (string)
            if series:
                print(f'{series}|{key}|{value}')
            else:
                # Artykuł w głównym katalogu
                print(f'{key}||')

    # Przetwórz strukturę
    for key, value in structure.items():
        process_item(key, value)

    # Wypisz domyślne pliki (z prefiksem FILES:)
    if default_files:
        print(f\"FILES:{','.join(default_files)}\")

except Exception as e:
    print(f'ERROR: {str(e)}', file=sys.stderr)
    sys.exit(1)
"
}

# Nagłówek
echo "======================================================================"
echo -e "${BLUE}📁 Tworzenie struktury katalogów artykułów${NC}"
echo "======================================================================"
echo ""
echo -e "  Plik YAML:   ${YELLOW}$YAML_FILE${NC}"
echo -e "  Katalog:     ${YELLOW}$BASE_DIR${NC}"
echo -e "  Tryb:        ${YELLOW}$([ "$DRY_RUN" = true ] && echo "DRY RUN (podgląd)" || echo "TWORZENIE")${NC}"
echo -e "  Pliki:       ${YELLOW}$([ "$CREATE_FILES" = true ] && echo "TAK" || echo "NIE")${NC}"
echo ""
echo "======================================================================"
echo ""

# Parsuj YAML
echo -e "${BLUE}📖 Parsowanie pliku YAML...${NC}"
parsed_output=$(parse_yaml "$YAML_FILE") || {
    echo -e "${RED}❌ Błąd parsowania YAML!${NC}"
    exit 1
}

# Wyciągnij domyślne pliki
default_files=""
while IFS= read -r line; do
    if [[ $line == FILES:* ]]; then
        default_files="${line#FILES:}"
    fi
done <<< "$parsed_output"

# Statystyki
series_count=0
silo_count=0
article_count=0

# Przetwórz każdą linię
declare -A series_seen
declare -A silo_seen

while IFS='|' read -r series silo article; do
    # Pomiń linie FILES:
    if [[ $series == FILES:* ]]; then
        continue
    fi

    # Określ ścieżkę w zależności od struktury
    if [[ -z $article ]]; then
        # Format: silo|article| (płaska struktura)
        article_path="$BASE_DIR/$series/$silo"
        actual_silo="$series"
        actual_article="$silo"
    elif [[ -z $silo ]]; then
        # Format: article|| (pojedynczy artykuł)
        article_path="$BASE_DIR/$series"
        actual_article="$series"
        actual_silo=""
    else
        # Format: series|silo|article (hierarchiczna struktura)
        article_path="$BASE_DIR/$series/$silo/$article"
        actual_silo="$series/$silo"
        actual_article="$article"
    fi

    # Statystyki
    if [[ -n $series && -z $silo && -z $article ]]; then
        # Pojedynczy artykuł w głównym katalogu
        :
    elif [[ -n $series && -n $silo && -z $article ]]; then
        # Płaska struktura silo/article
        if [[ ! ${silo_seen[$series]} ]]; then
            silo_seen[$series]=1
            ((silo_count++))
        fi
    else
        # Hierarchiczna struktura
        if [[ ! ${series_seen[$series]} && -n $silo && -n $article ]]; then
            series_seen[$series]=1
            ((series_count++))
        fi

        if [[ -n $actual_silo && ! ${silo_seen[$actual_silo]} ]]; then
            silo_seen[$actual_silo]=1
            ((silo_count++))
        fi
    fi

    ((article_count++))

    # Wyświetl
    if [ "$DRY_RUN" = true ]; then
        echo -e "  ${GREEN}✓${NC} $article_path"
    else
        # Utwórz katalog
        mkdir -p "$article_path"
        echo -e "  ${GREEN}✓${NC} Utworzono: $article_path"

        # Utwórz domyślne pliki jeśli włączone
        if [ "$CREATE_FILES" = true ] && [ -n "$default_files" ]; then
            IFS=',' read -ra files_array <<< "$default_files"
            for file in "${files_array[@]}"; do
                file_path="$article_path/$file"
                if [ ! -f "$file_path" ]; then
                    touch "$file_path"
                    echo -e "    ${BLUE}→${NC} Utworzono plik: $file"
                fi
            done
        fi
    fi

done <<< "$parsed_output"

# Podsumowanie
echo ""
echo "======================================================================"
echo -e "${BLUE}📊 Podsumowanie:${NC}"
echo ""
echo -e "  Series:      ${GREEN}$series_count${NC}"
echo -e "  Silosy:      ${GREEN}$silo_count${NC}"
echo -e "  Artykuły:    ${GREEN}$article_count${NC}"

if [ "$DRY_RUN" = true ]; then
    echo ""
    echo -e "${YELLOW}ℹ️  Tryb dry-run - nic nie zostało utworzone${NC}"
    echo -e "${YELLOW}   Uruchom bez -n aby faktycznie utworzyć katalogi${NC}"
fi

echo "======================================================================"
