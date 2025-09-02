# 🚀 Guía de Despliegue de TUNRAG

## 📋 Prerrequisitos

### **Sistema Operativo**
- ✅ **Linux** (Ubuntu 20.04+, CentOS 7+, RHEL 7+)
- ✅ **Windows** (Windows 10+, Windows Server 2016+)
- ✅ **macOS** (10.15+)

### **Software Requerido**
- **Python 3.8+** (recomendado 3.12+)
- **Git** para clonar el repositorio
- **pip** o **conda** para gestión de dependencias

### **Recursos del Sistema**
- **RAM**: Mínimo 2GB, recomendado 4GB+
- **CPU**: Mínimo 2 cores, recomendado 4 cores+
- **Almacenamiento**: Mínimo 5GB libre
- **Red**: Conexión a internet para OpenAI API

## 🏗️ Despliegue Local

### **1. Clonar el Repositorio**
```bash
git clone <repository-url>
cd TUNRAG
```

### **2. Configuración Automática (Recomendado)**
```bash
python setup.py
```

### **3. Configuración Manual**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Linux/macOS)
source venv/bin/activate

# Activar entorno (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp env.example .env
# Editar .env y configurar OPENAI_API_KEY
```

### **4. Ejecutar la Aplicación**
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## 🐳 Despliegue con Docker

### **1. Construir la Imagen**
```bash
docker build -t tunrag .
```

### **2. Ejecutar el Contenedor**
```bash
docker run -d \
  --name tunrag \
  -p 5000:5000 \
  -e OPENAI_API_KEY=tu_api_key \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/input:/app/input \
  tunrag
```

### **3. Usar Docker Compose (Recomendado)**
```bash
# Configurar variables de entorno
export OPENAI_API_KEY=tu_api_key

# Ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f tunrag

# Detener
docker-compose down
```

## ☁️ Despliegue en la Nube

### **AWS (EC2)**

#### **1. Crear Instancia EC2**
```bash
# Conectar a la instancia
ssh -i tu-key.pem ubuntu@tu-ip

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y dependencias
sudo apt install python3 python3-pip python3-venv git -y
```

#### **2. Desplegar TUNRAG**
```bash
# Clonar repositorio
git clone <repository-url>
cd TUNRAG

# Configurar
python3 setup.py

# Configurar variables de entorno
nano .env
# Configurar OPENAI_API_KEY y DEBUG=False
```

#### **3. Configurar Systemd Service**
```bash
sudo nano /etc/systemd/system/tunrag.service
```

```ini
[Unit]
Description=TUNRAG PQRS System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/TUNRAG
Environment=PATH=/home/ubuntu/TUNRAG/venv/bin
ExecStart=/home/ubuntu/TUNRAG/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### **4. Activar y Iniciar Servicio**
```bash
sudo systemctl daemon-reload
sudo systemctl enable tunrag
sudo systemctl start tunrag
sudo systemctl status tunrag
```

#### **5. Configurar Nginx (Opcional)**
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/tunrag
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/tunrag /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### **Google Cloud Platform**

#### **1. Crear Instancia**
```bash
gcloud compute instances create tunrag \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --tags=http-server,https-server
```

#### **2. Configurar Firewall**
```bash
gcloud compute firewall-rules create allow-http \
  --allow tcp:80 \
  --target-tags=http-server \
  --source-ranges=0.0.0.0/0

gcloud compute firewall-rules create allow-https \
  --allow tcp:443 \
  --target-tags=https-server \
  --source-ranges=0.0.0.0/0
```

#### **3. Desplegar Aplicación**
```bash
# Conectar a la instancia
gcloud compute ssh tunrag --zone=us-central1-a

# Seguir pasos similares a AWS
```

### **Azure**

#### **1. Crear VM**
```bash
az vm create \
  --resource-group tunrag-rg \
  --name tunrag-vm \
  --image UbuntuLTS \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys
```

#### **2. Configurar NSG**
```bash
az network nsg rule create \
  --resource-group tunrag-rg \
  --nsg-name tunrag-vmNSG \
  --name allow-http \
  --protocol tcp \
  --priority 1000 \
  --destination-port-range 80
```

#### **3. Desplegar Aplicación**
```bash
# Conectar a la VM
ssh azureuser@tu-ip

# Seguir pasos similares a AWS
```

## 🔒 Configuración de Seguridad

### **Variables de Entorno Críticas**
```bash
# Cambiar en producción
DEBUG=False
SECRET_KEY=clave_secreta_muy_larga_y_compleja
LOG_LEVEL=WARNING

# Configurar CORS apropiadamente
CORS_ORIGINS=https://tudominio.com,https://www.tudominio.com
```

### **Firewall y Red**
```bash
# Solo abrir puertos necesarios
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### **SSL/TLS (Recomendado)**
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com

# Renovar automáticamente
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Monitoreo y Mantenimiento

### **Logs del Sistema**
```bash
# Ver logs en tiempo real
sudo journalctl -u tunrag -f

# Ver logs de la aplicación
tail -f logs/tunrag.log

# Limpiar logs antiguos
python maintenance.py --clean-logs 30
```

### **Estado del Servicio**
```bash
# Verificar estado
sudo systemctl status tunrag

# Reiniciar servicio
sudo systemctl restart tunrag

# Ver logs del servicio
sudo journalctl -u tunrag
```

### **Mantenimiento Automático**
```bash
# Crear cron job para mantenimiento
crontab -e

# Agregar:
0 2 * * 0 python /ruta/a/tunrag/maintenance.py --optimize
0 3 * * 0 python /ruta/a/tunrag/maintenance.py --backup
```

### **Backups**
```bash
# Backup manual
python maintenance.py --backup

# Backup automático con cron
0 4 * * 0 python /ruta/a/tunrag/maintenance.py --backup
```

## 🚨 Solución de Problemas

### **Problemas Comunes**

#### **1. Servicio no inicia**
```bash
# Verificar logs
sudo journalctl -u tunrag -n 50

# Verificar configuración
python test_basic.py

# Verificar permisos
ls -la /ruta/a/tunrag/
```

#### **2. Error de puerto ocupado**
```bash
# Verificar puerto
sudo netstat -tlnp | grep :5000

# Matar proceso
sudo kill -9 PID

# Verificar firewall
sudo ufw status
```

#### **3. Error de memoria**
```bash
# Verificar uso de memoria
free -h

# Verificar logs de memoria
dmesg | grep -i "out of memory"
```

#### **4. Error de API OpenAI**
```bash
# Verificar API key
echo $OPENAI_API_KEY

# Verificar conectividad
curl -I https://api.openai.com

# Verificar límites de API
# Revisar dashboard de OpenAI
```

### **Comandos de Diagnóstico**
```bash
# Estado del sistema
python start.py

# Pruebas básicas
python test_basic.py

# Verificar salud
curl http://localhost:5000/health

# Estado detallado
curl http://localhost:5000/system/status
```

## 📈 Escalabilidad

### **Load Balancer**
```nginx
upstream tunrag_backend {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    listen 80;
    location / {
        proxy_pass http://tunrag_backend;
    }
}
```

### **Múltiples Instancias**
```bash
# Instancia 1
python app.py --port 5000

# Instancia 2
python app.py --port 5001

# Instancia 3
python app.py --port 5002
```

### **Docker Swarm**
```bash
# Inicializar swarm
docker swarm init

# Desplegar stack
docker stack deploy -c docker-compose.yml tunrag

# Escalar servicio
docker service scale tunrag_tunrag=3
```

## 🎯 Checklist de Despliegue

### **Pre-despliegue**
- [ ] Repositorio clonado
- [ ] Dependencias instaladas
- [ ] Variables de entorno configuradas
- [ ] Pruebas básicas pasando
- [ ] API key de OpenAI configurada

### **Despliegue**
- [ ] Aplicación ejecutándose
- [ ] Puerto accesible
- [ ] Logs funcionando
- [ ] Endpoints respondiendo
- [ ] Transcripción de audio funcionando

### **Post-despliegue**
- [ ] SSL/TLS configurado
- [ ] Firewall configurado
- [ ] Monitoreo configurado
- [ ] Backups configurados
- [ ] Documentación actualizada

## 📞 Soporte

### **Recursos de Ayuda**
- **Documentación**: README.md
- **Pruebas**: `python test_basic.py`
- **Mantenimiento**: `python maintenance.py --help`
- **Setup**: `python setup.py`

### **Contacto**
- **Issues**: [GitHub Issues]
- **Documentación**: [Wiki del proyecto]
- **Comunidad**: [Discord/Telegram]

---

**¡TUNRAG está listo para revolucionar la atención al ciudadano!** 🚀
