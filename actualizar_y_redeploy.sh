#!/bin/bash

# 1. Verifica si hay cambios
echo "🔍 Verificando cambios en el repositorio..."
if git diff --quiet && git diff --cached --quiet; then
  echo "✅ No hay cambios nuevos en el repositorio. Saliendo."
  exit 0
fi

# 2. Agrega y comitea cambios
echo "📦 Añadiendo y comiteando cambios..."
git add .
COMMIT_MSG="Auto-actualización: $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MSG"

# 3. Pushea a GitHub
echo "🚀 Pusheando a GitHub..."
git push origin main

# 4. Comprueba si requirements.txt cambió (y por tanto reinstalar)
if git diff --name-only HEAD@{1} HEAD | grep -q "requirements.txt"; then
  echo "📦 Cambios detectados en requirements.txt. Reconstruyendo contenedor..."
  docker-compose build --no-cache
else
  echo "🐳 No hay cambios en dependencias. Solo reiniciando contenedor..."
fi

# 5. Re-despliega el contenedor
echo "🔄 Re-deploying con Docker Compose..."
docker-compose down --remove-orphans --volumes --rmi all
docker-compose up --build -d
docker-compose logs -f --tail=50

echo "✅ Proceso completado con éxito."

