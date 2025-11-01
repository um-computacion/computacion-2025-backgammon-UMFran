# Dockerfile
# Imagen base de Python
FROM python:3.12-slim

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:0

# Instalar dependencias del sistema para pygame y X11
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libfreetype6 \
    fontconfig \
    fonts-dejavu-core \
    fonts-liberation \
    fonts-noto \
    libportmidi0 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxrandr2 \
    libxi6 \
    libxcursor1 \
    libxinerama1 \
    libxxf86vm1 \
    && fc-cache -fv \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
COPY . .

# Comando por defecto (se puede sobrescribir)
CMD ["python", "-m", "cli.cli"]