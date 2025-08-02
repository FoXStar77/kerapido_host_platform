#!/bin/bash

echo "🔧 Desactivando firewalls..."
sudo systemctl stop ufw || echo "UFW no está activo"
sudo systemctl stop firewalld || echo "Firewalld no está activo"
sudo iptables -F && echo "iptables reglas limpiadas"

echo "🔧 Deteniendo servicios auditivos..."
sudo systemctl stop auditd || echo "auditd no está presente"

echo "🔧 Desactivando AppArmor (si aplica)..."
if systemctl is-active apparmor >/dev/null 2>&1; then
  sudo systemctl stop apparmor
  sudo systemctl disable apparmor
  echo "AppArmor desactivado"
else
  echo "AppArmor no está corriendo"
fi

echo "🔧 Reconfigurando Docker con DNS públicos..."
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json > /dev/null <<EOF
{
  "dns": ["8.8.8.8", "1.1.1.1"]
}
EOF
sudo systemctl restart docker

echo "🚀 Iniciando despliegue del contenedor..."
docker-compose down --remove-orphans --volumes --rmi all
docker-compose up --build -d

echo "📋 Mostrando logs en tiempo real:"
docker-compose logs -f --tail=50

