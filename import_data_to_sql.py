from sqlalchemy import create_engine, Table, MetaData
import pandas as pd
import sqlite3
import os

# Задаємо шлях до файлу Excel та бази даних
excel_file_path = r"C:\Users\user\Desktop\sales_intex\sales_bd\sales_file.xlsx"
db_file_path = r"C:\Users\user\Desktop\sales_intex\sales_bd\test_database.db"

# Перевіряємо існування бази даних і створюємо нову, якщо потрібно
if not os.path.exists(db_file_path):
    open(db_file_path, 'w').close()

# Створюємо з'єднання з базою даних SQLite
engine = create_engine(f'sqlite:///{db_file_path}')
conn = sqlite3.connect(db_file_path)

# Завантажуємо дані з Excel
try:
    df = pd.read_excel(excel_file_path)
except FileNotFoundError:
    print(f"Файл {excel_file_path} не знайдено. Перевірте шлях до файлу.")
    conn.close()
    exit()

# Обробка даних перед вставкою в базу даних
df['Id'] = pd.to_numeric(df['Id'], errors='coerce')  # Перетворюємо в числовий тип з помилками
df.dropna(subset=['Id'], inplace=True)  # Видаляємо рядки з NaN в колонці 'Id'
df['Id'] = df['Id'].astype(int)  # Переконуємося, що значення Id є цілими числами

# Використовуємо `to_sql` з параметром `if_exists='replace'`, щоб замінити таблицю, якщо вона вже існує
# Можна також використовувати `if_exists='append'` та обробляти конфлікти за допомогою SQL
try:
    df.to_sql('sales_test', con=engine, if_exists='replace', index=False)
    print("Дані успішно імпортовані в базу даних")
except sqlite3.IntegrityError as e:
    print("Помилка цілісності даних:", e)
except Exception as e:
    print("Помилка при імпорті даних:", e)
finally:
    conn.close()
