#!/bin/bash
# 🗄️ PRISMA STUDIO - Interface BDD visuelle

set -e

echo "🗄️ PRISMA STUDIO"
echo "================"

cd "$(dirname "$0")/frontend"

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js non installé"
    exit 1
fi

echo "✅ Node: $(node --version)"
echo "✅ NPM: $(npm --version)"

# Installer dépendances si nécessaire
if [ ! -d "node_modules" ]; then
    echo "📦 Installation dépendances..."
    npm install
fi

# Vérifier fichier .env
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env absent. Création..."
    cat > .env << 'EOF'
DATABASE_URL="postgresql://refyai:refyai@localhost:5432/refyai?schema=public"
NEXTAUTH_SECRET="your-secret-key-here"
NEXTAUTH_URL="http://localhost:3000"
NEXT_PUBLIC_API_URL="http://localhost:8000/api/v1"
EOF
fi

# Générer Prisma Client si nécessaire
if [ ! -d "node_modules/.prisma" ]; then
    echo "🔧 Génération Prisma Client..."
    npx prisma generate
fi

echo ""
echo "🚀 Démarrage Prisma Studio..."
echo "📍 Interface: http://localhost:5555"
echo ""
echo "💡 Ctrl+C pour arrêter"
echo ""

npx prisma studio
