import os
import subprocess
import datetime
import time
import tarfile
import threading

LOG_DIR = "/var/log/docker_logs"  
ARCHIVE_DIR = os.path.join(LOG_DIR, "archive")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

today = datetime.date.today()
start_of_week = today - datetime.timedelta(days=today.weekday() + 4)  
end_of_week = start_of_week + datetime.timedelta(days=6)  
archive_name = f"{start_of_week}_{end_of_week}.tar.gz"

def archive_old_logs():
    old_logs = [f for f in os.listdir(LOG_DIR) if f.endswith(".log")]
    if old_logs:
        archive_path = os.path.join(ARCHIVE_DIR, archive_name)
        with tarfile.open(archive_path, "w:gz") as tar:
            for log_file in old_logs:
                full_path = os.path.join(LOG_DIR, log_file)
                tar.add(full_path, arcname=log_file)
        print(f"Архивация завершена: {archive_path}")

archive_old_logs()

def get_containers():
    result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
    return result.stdout.strip().split("\n") if result.stdout else []

def log_container(container_name):
    log_file = os.path.join(LOG_DIR, f"{container_name}_{today}.log")
    with open(log_file, "a") as f:
        process = subprocess.Popen(["docker", "logs", "-f", container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in iter(process.stdout.readline, ""):
            f.write(line)
            f.flush()

containers = get_containers()
if not containers:
    print("Нет запущенных контейнеров")
else:
    print(f"Записываем логи для контейнеров: {containers}")
    threads = []
    for container in containers:
        thread = threading.Thread(target=log_container, args=(container,), daemon=True)
        thread.start()
        threads.append(thread)

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nОстановка логирования...")
