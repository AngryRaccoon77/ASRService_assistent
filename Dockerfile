# Используем базовый образ Python
FROM python:3.11-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Клонируем репозиторий GigaAM
RUN git clone https://github.com/salute-developers/GigaAM.git

# Переходим в директорию GigaAM и устанавливаем библиотеку
RUN pip install ./GigaAM

# Копируем файлы приложения
COPY . .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Указываем команду запуска
CMD ["python", "gigaAMService.py"]