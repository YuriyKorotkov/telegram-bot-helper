import paramiko
from scp import SCPClient
import sqlite3
import pandas as pd
import os
from datetime import timedelta

# === Настройки ===
server_ip = '109.73.193.121'
username = 'root'
password = 'm-QW2zn#CT23V3'
remote_path = '/root/telegram-bot-helper/users.db'
local_path = './users.db'
excel_path = r"C:\Users\150\PycharmProjects\ISUP_bot\users.xlsx"

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

def transform_datetime_column(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce')  # Преобразуем в datetime, ошибки в NaT
    df[column_name] = df[column_name] + timedelta(hours=3)              # Добавляем 3 часа
    # Форматируем: "ЧЧ:ММ ДД.ММ.ГГГГ"
    df[column_name] = df[column_name].dt.strftime('%H:%M %d.%m.%Y')
    return df

def export_to_excel():
    print("📊 Читаем таблицу из базы данных...")
    conn = sqlite3.connect(local_path)
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()

    # Преобразуем нужные столбцы с датой/временем
    for col in ['joined_at', 'last_seen']:
        if col in df.columns:
            df = transform_datetime_column(df, col)
        else:
            print(f"⚠️ Колонка {col} не найдена в таблице")

    print("💾 Сохраняем как Excel с настройкой ширины столбцов...")

    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='users')
        worksheet = writer.sheets['users']

        # Устанавливаем ширину для 2-го, 3-го и 4-го столбцов (индексы 1,2,3)
        for idx in [1, 2, 3, 4]:
            col_letter = chr(ord('A') + idx)
            worksheet.column_dimensions[col_letter].width = 18

    print(f"✅ Файл сохранён как {excel_path}")

if __name__ == "__main__":
    download_db()
    export_to_excel()
    os.startfile(excel_path)
