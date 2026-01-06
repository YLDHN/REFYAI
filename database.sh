#!/bin/bash
# 🗄️ DATABASE - Gestion BDD (PostgreSQL + Migrations)

set -e

echo "🗄️ REFY AI - DATABASE"
echo "======================"

COMMAND=${1:-help}

cd "$(dirname "$0")"

# Vérifier PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL non installé. Installation..."
    brew install postgresql@15
    brew services start postgresql@15
fi

# Configuration BDD
DB_USER="refyai"
DB_PASS="refyai"
DB_NAME="refyai"
DB_HOST="localhost"
DB_PORT="5432"
PG_SUPERUSER=$(whoami)  # Utilisateur système pour macOS

case $COMMAND in
    
    # Créer la base de données
    "create"|"init")
        echo "📦 Création base de données..."
        
        # Créer user si n'existe pas
        psql -U $PG_SUPERUSER -d postgres -tc "SELECT 1 FROM pg_user WHERE usename = '$DB_USER'" | grep -q 1 || \
            psql -U $PG_SUPERUSER -d postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
        
        # Créer database si n'existe pas
        psql -U $PG_SUPERUSER -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
            psql -U $PG_SUPERUSER -d postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
        
        # Grant permissions
        psql -U $PG_SUPERUSER -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
        
        echo "✅ Base de données '$DB_NAME' créée"
        echo "📍 URL: postgresql://$DB_USER:$DB_PASS@$DB_HOST:$DB_PORT/$DB_NAME"
        ;;
    
    # Appliquer migrations Alembic (Backend Python)
    "migrate-backend"|"alembic")
        echo "🔄 Migrations Backend (Alembic)..."
        cd backend
        
        if [ ! -d "venv" ]; then
            python3 -m venv venv
        fi
        
        source venv/bin/activate
        pip install alembic psycopg2-binary -q
        
        alembic upgrade head
        
        echo "✅ Migrations Backend appliquées"
        ;;
    
    # Appliquer migrations Prisma (Frontend)
    "migrate-frontend"|"prisma")
        echo "🔄 Migrations Frontend (Prisma)..."
        cd frontend
        
        if [ ! -d "node_modules" ]; then
            npm install
        fi
        
        # Génerer migration
        if [ "$2" == "generate" ]; then
            npx prisma migrate dev --name "$3"
            echo "✅ Migration générée: $3"
        else
            # Appliquer migrations
            npx prisma migrate deploy
            npx prisma generate
            echo "✅ Migrations Prisma appliquées"
        fi
        ;;
    
    # Appliquer TOUTES les migrations
    "migrate-all"|"migrate")
        echo "🔄 Application de TOUTES les migrations..."
        
        # Backend
        echo ""
        echo "1️⃣ Migrations Backend..."
        cd backend
        if [ ! -d "venv" ]; then
            python3 -m venv venv
        fi
        source venv/bin/activate
        pip install alembic psycopg2-binary -q
        alembic upgrade head
        cd ..
        
        # Frontend
        echo ""
        echo "2️⃣ Migrations Frontend..."
        cd frontend
        if [ ! -d "node_modules" ]; then
            npm install
        fi
        
        # Utiliser db push si schema non vide (première migration après Alembic)
        if npx prisma migrate deploy 2>&1 | grep -q "P3005"; then
            echo "⚠️  Schema non vide, utilisation de db push..."
            npx prisma db push --skip-generate
        fi
        
        npx prisma generate
        cd ..
        
        echo ""
        echo "✅ Toutes les migrations appliquées"
        ;;
    
    # Reset complet BDD
    "reset")
        echo "⚠️  RESET complet de la base de données..."
        read -p "Confirmer ? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            psql -U $PG_SUPERUSER -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
            psql -U $PG_SUPERUSER -d postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
            echo "✅ Base de données réinitialisée"
            echo "💡 Appliquer les migrations avec: ./database.sh migrate"
        fi
        ;;
    
    # Backup BDD
    "backup")
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        echo "💾 Backup base de données..."
        pg_dump -U $DB_USER -h $DB_HOST -p $DB_PORT $DB_NAME > $BACKUP_FILE
        echo "✅ Backup créé: $BACKUP_FILE"
        ;;
    
    # Restore BDD
    "restore")
        if [ -z "$2" ]; then
            echo "❌ Usage: ./database.sh restore <backup_file.sql>"
            exit 1
        fi
        echo "📥 Restore base de données..."
        psql -U $DB_USER -h $DB_HOST -p $DB_PORT $DB_NAME < $2
        echo "✅ Base de données restaurée"
        ;;
    
    # Seed données test
    "seed")
        echo "🌱 Seeding données test..."
        cd frontend
        if [ ! -d "node_modules" ]; then
            npm install
        fi
        npx prisma db seed
        echo "✅ Données test insérées"
        ;;
    
    # Status BDD
    "status")
        echo "📊 Status base de données..."
        echo ""
        echo "PostgreSQL:"
        brew services list | grep postgresql || echo "❌ Non installé"
        echo ""
        echo "Connexion:"
        if psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d $DB_NAME -c "SELECT version();" > /dev/null 2>&1; then
            echo "✅ Connexion OK"
            echo ""
            psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d $DB_NAME -c "SELECT schemaname, tablename FROM pg_tables WHERE schemaname = 'public';"
        else
            echo "❌ Impossible de se connecter"
        fi
        ;;
    
    # Aide
    *)
        echo ""
        echo "Usage: ./database.sh <command>"
        echo ""
        echo "Commands:"
        echo "  create              Créer la base de données"
        echo "  migrate-backend     Appliquer migrations Alembic (Backend)"
        echo "  migrate-frontend    Appliquer migrations Prisma (Frontend)"
        echo "  migrate-all         Appliquer TOUTES les migrations"
        echo "  reset               Reset complet de la BDD"
        echo "  backup              Créer un backup"
        echo "  restore <file>      Restaurer un backup"
        echo "  seed                Insérer données test"
        echo "  status              Voir status BDD"
        echo ""
        echo "Exemples:"
        echo "  ./database.sh create           # Créer BDD initiale"
        echo "  ./database.sh migrate-all      # Appliquer migrations"
        echo "  ./database.sh seed             # Ajouter données test"
        echo ""
        ;;
esac
