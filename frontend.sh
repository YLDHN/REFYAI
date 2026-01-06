#!/bin/bash
# 🎨 FRONTEND - Démarrage Next.js

set -e

echo "🎨 REFY AI - FRONTEND"
echo "====================="

cd "$(dirname "$0")/frontend"

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js non installé"
    exit 1
fi

echo "✅ Node: $(node --version)"
echo "✅ NPM: $(npm --version)"

# Installer dépendances
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.package-lock.json" ]; then
    echo "📦 Installation dépendances..."
    npm install
else
    echo "✅ Dépendances déjà installées"
fi

# Vérifier .env
if [ ! -f .env ]; then
    echo "⚠️  Création fichier .env..."
    cat > .env << 'EOF'
DATABASE_URL="postgresql://refyai:refyai@localhost:5432/refyai?schema=public"
NEXTAUTH_SECRET="your-secret-key-change-in-production"
NEXTAUTH_URL="http://localhost:3000"
NEXT_PUBLIC_API_URL="http://localhost:8000/api/v1"
EOF
fi

# Générer Prisma Client
if [ ! -d "node_modules/.prisma" ]; then
    echo "🔧 Génération Prisma Client..."
    npx prisma generate
fi

# Build si nécessaire (pour production)
if [ "$1" == "build" ]; then
    echo "🔨 Build production..."
    npm run build
    echo "✅ Build terminé"
    exit 0
fi

# Démarrer dev server
echo ""
echo "🚀 Démarrage Frontend Next.js..."
echo "📍 App: http://localhost:3000"
echo ""
echo "💡 Ctrl+C pour arrêter"
echo ""

npm run dev
