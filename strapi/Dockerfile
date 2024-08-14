# Utiliser l'image de base node
FROM node:18-alpine

# Définir le répertoire de travail dans le conteneur
WORKDIR /usr/src/app

# Copier les fichiers package.json et package-lock.json
COPY ./music-data/package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste de l'application Strapi dans le conteneur
COPY ./music-data/ ./

# Exposer le port par défaut de Strapi
EXPOSE 1337

# Lancer l'application Strapi
CMD ["npm", "run", "develop"]
#CMD ["tail", "-f", "/dev/null"]
