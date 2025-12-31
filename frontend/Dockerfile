FROM node:20-alpine AS builder

WORKDIR /app

# Installation des dépendances
COPY package*.json ./
RUN npm ci

# Copie du code et build
COPY . .
RUN npm run build

# Image de production
FROM node:20-alpine

WORKDIR /app

# Copie des fichiers nécessaires
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.ts ./

# Installation des dépendances de production uniquement
RUN npm ci --production

EXPOSE 3000

CMD ["npm", "start"]
