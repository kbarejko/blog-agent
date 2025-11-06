#!/bin/bash

# Blog Agent - Setup Script
# Ten skrypt pomoże Ci szybko skonfigurować Blog Agent

echo "=================================="
echo "🤖 Blog Agent - Setup"
echo "=================================="
echo ""

# Sprawdzenie Pythona
echo "🔍 Sprawdzam wersję Pythona..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 nie jest zainstalowany!"
    echo "Zainstaluj Python 3.8 lub nowszy i uruchom ponownie."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION"
echo ""

# Instalacja zależności
echo "📦 Instaluję zależności..."
pip install -r requirements.txt --break-system-packages

if [ $? -ne 0 ]; then
    echo "⚠️  Próbuję bez flagi --break-system-packages..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ Zależności zainstalowane!"
echo ""

# Konfiguracja klucza API
echo "🔑 Konfiguracja klucza API"
echo ""

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Nie znaleziono klucza API w zmiennych środowiskowych."
    echo ""
    echo "Aby uzyskać klucz API:"
    echo "1. Przejdź do: https://console.anthropic.com/"
    echo "2. Zaloguj się / Zarejestruj konto"
    echo "3. Przejdź do Settings > API Keys"
    echo "4. Utwórz nowy klucz API"
    echo ""
    read -p "Czy masz już klucz API? (t/n): " HAS_KEY
    
    if [ "$HAS_KEY" = "t" ] || [ "$HAS_KEY" = "T" ]; then
        echo ""
        read -p "Wklej swój klucz API: " API_KEY
        
        # Dodaj do .bashrc lub .zshrc
        SHELL_RC="$HOME/.bashrc"
        if [ -f "$HOME/.zshrc" ]; then
            SHELL_RC="$HOME/.zshrc"
        fi
        
        echo "" >> "$SHELL_RC"
        echo "# Anthropic API Key for Blog Agent" >> "$SHELL_RC"
        echo "export ANTHROPIC_API_KEY='$API_KEY'" >> "$SHELL_RC"
        
        export ANTHROPIC_API_KEY="$API_KEY"
        
        echo "✅ Klucz API zapisany w $SHELL_RC"
        echo "💡 Uruchom: source $SHELL_RC (lub zrestartuj terminal)"
    else
        echo ""
        echo "Możesz ustawić klucz później:"
        echo "  export ANTHROPIC_API_KEY='twój-klucz'"
    fi
else
    echo "✅ Klucz API już jest ustawiony!"
fi

echo ""
echo "=================================="
echo "✨ Setup zakończony!"
echo "=================================="
echo ""
echo "📚 Następne kroki:"
echo ""
echo "1. Jeśli dodałeś klucz API, zrestartuj terminal lub uruchom:"
echo "   source ~/.bashrc  (lub ~/.zshrc)"
echo ""
echo "2. Uruchom podstawowy przykład:"
echo "   python3 blog_agent.py"
echo ""
echo "3. Lub wypróbuj różne przykłady:"
echo "   python3 examples.py"
echo ""
echo "4. Przeczytaj dokumentację:"
echo "   cat README.md"
echo ""
echo "Miłego pisania artykułów! 🚀"
