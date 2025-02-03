import os
import subprocess
from datetime import datetime

# Файл с контейнерами
CONFIG_FILE = "/var/log/docker_logs/config.txt"
LOG_DIR = "/var/log/docker_logs"

# Функция загрузки контейнеров из файла
def load_containers_from_file(filename):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return []

# Загружаем контейнеры
containers = load_containers_from_file(CONFIG_FILE)

# Создаем папку для логов, если ее нет
os.makedirs(LOG_DIR, exist_ok=True)

# Записываем логи
for container in containers:
    log_file = os.path.join(LOG_DIR, f"{container}.log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, "a") as f:
        f.write(f"\n[{timestamp}] Запись логов контейнера {container}...\n")
        try:
            logs = subprocess.run(["docker", "logs", container], capture_output=True, text=True)
            f.write(logs.stdout + "\n")
        except Exception as e:
            f.write(f"Ошибка при получении логов: {e}\n")

print("Сбор логов завершен.")
