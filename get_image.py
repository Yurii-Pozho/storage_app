import zipfile
import os
from PIL import Image
from io import BytesIO

# Шлях до вашого Excel файлу
excel_file = r"C:\Users\user\Desktop\Дані склад 2024.xlsx"

# Створюємо папку для збереження зображень
image_folder = r"C:\Users\user\Desktop\sales_intex\sales_bd\img"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# Відкриваємо .xlsx як архів ZIP
with zipfile.ZipFile(excel_file, 'r') as z:
    # Проходимо по всім файлам у ZIP архіві
    for file in z.namelist():
        # Шукаємо файли, що містять зображення
        if file.startswith('xl/media/'):
            # Витягуємо зображення
            image_data = z.read(file)
            # Визначаємо ім'я файлу
            image_filename = os.path.join(image_folder, os.path.basename(file))
            # Зберігаємо зображення
            with open(image_filename, 'wb') as img_file:
                img_file.write(image_data)
            print(f'Зображення збережено як {image_filename}')
