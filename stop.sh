#!/bin/bash

echo "🛑 Arrêt de REFYAI..."

# Fonction pour tuer un processus sur un port
kill_port() {
    local port=$1
    local name=$2
    local pid=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "  🔸 Arrêt $name (port $port, PID $pid)..."
        kill -9 $pid 2>/dev/null
        sleep 0.5
    fi
}

kill_port 8000 "Backend"
kill_port 3000 "Frontend"

# Tuer tous les processus uvicorn et next
pkill -f "uvicorn app.main" 2>/dev/null
pkill -f "next dev" 2>/dev/null
pkill -f "next-server" 2>/dev/null

echo "✅ Tous les services arrêtés"
