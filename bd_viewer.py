import paramiko
from scp import SCPClient
import sqlite3
import pandas as pd
import os

# === Настройки ===
server_ip = '109.73.193.'
username = ''
password = ''
remote_path = '/root/telegram-bot-helper/users.db'
local_path = './users.db'
excel_path = r"C:\Users\"

# === Подключение и скачивание базы данных ===
def download_db():
    print("🔌 Подключаемся к серверу...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_ip, username=username, password=password)

    print("📥 Загружаем файл базы данных...")
    with SCPClient(ssh.get_transport()) as scp:
        scp.get(remote_path, local_path)
    ssh.close()
    print("✅ Файл загружен!")

# === Чтение и экспорт таблицы из базы данных ===
def export_to_excel():
    print("📊 Читаем таблицу из базы данных...")
    conn = sqlite3.connect(local_path)
    cursor = conn.cursor()

    # Получение всех названий таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("📚 Найдены таблицы:", [t[0] for t in tables])

    # Допустим, таблица называется 'users'
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()

    print("💾 Сохраняем как Excel...")
    df.to_excel(excel_path, index=False)
    print(f"✅ Файл сохранён как {excel_path}")

# === Запуск ===
if __name__ == "__main__":
    download_db()
    export_to_excel()

    # Автоматически открыть файл в Проводнике, можно открыть вручную через PyCharm
    os.startfile(excel_path)  # Работает только на Windows
