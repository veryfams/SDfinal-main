# Etapa 1: Build
FROM node:18 AS builder

WORKDIR /app
COPY . .

# ⚠️ Asegúrate de instalar react-bootstrap-icons antes del build
RUN npm install react-bootstrap-icons
RUN npm install
RUN npm run build

# Etapa 2: Servidor estático
FROM node:18

WORKDIR /app

# Instalar servidor estático globalmente
RUN npm install -g serve

# Copiar solo la carpeta build del paso anterior
COPY --from=builder /app/build ./build

# Exponer el puerto 3000
EXPOSE 3000

# Comando por defecto
CMD ["serve", "-s", "build", "-l", "3000"]
