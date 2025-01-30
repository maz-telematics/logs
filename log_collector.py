import os
import subprocess
import datetime
import time

LOG_DIR = "/var/log/docker_logs"

# Функция для получения списка контейнеров
def get_containers():
    result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
    return result.stdout.strip().split("\n") if result.stdout else []

# Функция для записи логов каждого контейнера
def log_container(container_name):
    today = datetime.date.today()
    log_file = os.path.join(LOG_DIR, f"{container_name}_{today}.log")
    with open(log_file, "a") as f:  # Открытие с флагом 'a' для добавления
        process = subprocess.Popen(["docker", "logs", "-f", container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in iter(process.stdout.readline, ""):
            f.write(line)
            f.flush()

containers = get_containers()
if containers:
    print(f"Записываем логи для контейнеров: {containers}")
    for container in containers:
        log_container(container)
else:
    print("Нет запущенных контейнеров.")
