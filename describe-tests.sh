#!/bin/bash

# Script pour afficher le détail de chaque fichier de tests E2E

cd "$(dirname "$0")/frontend/tests/e2e"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo "📚 DESCRIPTION DÉTAILLÉE DES TESTS E2E"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

count=0
for file in *.spec.ts; do
    if [ -f "$file" ]; then
        count=$((count + 1))
        echo -e "${BLUE}[$count] $file${NC}"
        echo ""
        
        # Extraire tous les test.describe
        describes=$(grep "test\.describe\|describe(" "$file" | sed "s/.*['\"]//; s/['\"].*//" | head -5)
        
        if [ -n "$describes" ]; then
            echo -e "  ${CYAN}📦 Groupes de tests:${NC}"
            echo "$describes" | while read -r line; do
                if [ -n "$line" ]; then
                    echo "    • $line"
                fi
            done
            echo ""
        fi
        
        # Extraire les premiers test()
        tests=$(grep "test(" "$file" | sed "s/.*test(['\"]//; s/['\"].*//" | head -10)
        
        if [ -n "$tests" ]; then
            echo -e "  ${GREEN}✓ Tests individuels:${NC}"
            echo "$tests" | while read -r line; do
                if [ -n "$line" ]; then
                    echo "    ✓ $line"
                fi
            done
        fi
        
        # Compter le total
        total=$(grep -c "test(" "$file")
        echo ""
        echo -e "  ${YELLOW}📊 Total: $total test(s)${NC}"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
    fi
done

echo ""
echo "✨ Total: $count fichiers de tests"
echo ""
echo "💡 Pour exécuter un test en mode visible:"
echo "   ./view-tests.sh"
echo ""
