# Используйте официальный образ Python
FROM python:3.9

# Установите рабочую директорию в контейнере
WORKDIR /app

# Скопируйте файлы проекта в контейнер
COPY . /app

# Установите зависимости из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Запустите сервер на порту 8080
CMD ["python", "server.py"]
