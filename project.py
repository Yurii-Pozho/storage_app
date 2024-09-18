import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from PIL import Image
from io import BytesIO
import requests
import os
import plotly.express as px

# Вкажіть шлях до вашої SQLite бази даних у форматі URI
database_path = 'sqlite:///test_database.db'

# Створення SQLAlchemy engine
engine = create_engine(database_path)

# Завантаження таблиці в DataFrame
df = pd.read_sql_table('sales_test', engine)

# Перейменування колонки 'Nomenclature' на 'Номенклатура'
df.rename(columns={
    'Id': 'id',
    'Nomenclature': 'Номенклатура',
    'Category': 'Категорія',
    'Type': 'Тип',
    'Main supplier': 'Основний постачальник',
    'Code ODC': 'Код ODC',
    'Item': 'Артикул',
    'Remaining pieces': 'Залишок штук',
    'Remaining cases': 'Залишок ящиків',
    'All cases': 'Всього ящиків',
    'Order 2024 cases': 'Замовлення 2024 ящиків',
    'Area': 'Зона',
    'Drawer height': 'Ящиків у висоту',
    'Depth of the drawer area': 'Глибина зони ящиків',
    'Rows': 'Рядів',
    'Width': 'Ширина',
    'Pieces per box': 'Штук у ящику',
    'Box weight': 'Ящик вага',
    'Box volume': 'Ящик об\'єм',
    'Box length (to the wall)': 'Ящик довжина (до стіни)',
    'Box width (along depth)': 'Ящик ширина (вздовж глибини)',
    'Box height': 'Ящик висота',
    'Piece weight': 'Штук вага',
    'Piece volume': 'Штук об\'єм',
    'Piece length': 'Штук довжина',
    'Piece width': 'Штук ширина',
    'Piece height': 'Штук висота'
}, inplace=True)

# Функція для завантаження зображень
def load_image(img_path):
    """Завантаження зображення з локального файлу або URL."""
    img_path = img_path.strip('"')  # Видалення лапок, якщо є
    if img_path.startswith('http'):
        try:
            response = requests.get(img_path)
            if response.status_code == 200:
                return Image.open(BytesIO(response.content))
            else:
                st.write(f"Не вдалося завантажити зображення з URL: {img_path}")
        except Exception as e:
            st.write(f"Помилка при завантаженні зображення з URL: {e}")
    else:
        try:
            img_path = os.path.normpath(img_path)  # Нормалізація шляху
            return Image.open(img_path)
        except Exception as e:
            st.write(f"Помилка при обробці локального зображення: {e}")
    return None

# Функція для стилізованого роздільника
def styled_line(color='#8bbdd9', height='1px'):
    line_html = f"""
    <hr style="border: {height} solid {color}; margin: 20px 0;">
    """
    st.markdown(line_html, unsafe_allow_html=True)

# Блок 1: Фільтрація даних за введеним ID
def load_image(img_path):
    """Завантаження зображення з локального файлу або URL."""
    img_path = img_path.strip('"')  # Видалення лапок, якщо є
    if img_path.startswith('http'):
        try:
            response = requests.get(img_path)
            if response.status_code == 200:
                return Image.open(BytesIO(response.content))
            else:
                st.write(f"Не вдалося завантажити зображення з URL: {img_path}")
        except Exception as e:
            st.write(f"Помилка при завантаженні зображення з URL: {e}")
    else:
        try:
            img_path = os.path.normpath(img_path)  # Нормалізація шляху
            return Image.open(img_path)
        except Exception as e:
            st.write(f"Помилка при обробці локального зображення: {e}")
    return None

st.write('<h1 style="text-align: center;">Перегляд даних за ID</h1>', unsafe_allow_html=True)

id_input = st.text_input('Введіть ID')

if id_input:
    filtered_df = df[df['id'] == int(id_input)]
    
    if not filtered_df.empty:
        with st.expander("Інформація для вибраного ID:", expanded=True):
            # Спочатку показати зображення
            if 'Image' in filtered_df.columns:
                for img_path in filtered_df['Image']:
                    image = load_image(img_path)
                    if image:
                        new_size = (400, 300)
                        resized_image = image.resize(new_size, Image.LANCZOS)
                        st.image(resized_image, width=200)
            
            # Потім показати інформацію з відображенням у два стовпці
            column_mapping = {
                "id": "Основний постачальник",
                "Тип": "Всього ящиків",
                "Артикул": "Штук у ящику",
                "Категорія": "Залишок штук",
                "Зона": "Залишок ящиків",
                "Номенклатура": "Замовлення 2024 ящиків",
                "Рядів": "Глибина зони ящиків",
                "Ширина": "Ящиків у висоту",
                "Штук об'єм": "Ящик об'єм",
                "Штук ширина": "Ящик ширина (вздовж глибини)",
                "Штук вага": "Ящик вага",
                "Штук довжина": "Ящик довжина (до стіни)",
                "Штук висота": "Ящик висота"
            }

            # Виведення у два стовпці
            col1, col2 = st.columns(2)

            def format_value(value, column_name):
                """Форматування значення: округлення чисел до двох десяткових знаків, крім 'id' та 'Артикул'."""
                try:
                    if column_name in ["id", "Артикул"]:
                        return value
                    return f"{float(value):.2f}"
                except ValueError:
                    return value

            for i, (col_left, col_right) in enumerate(column_mapping.items()):
                if col_left in filtered_df.columns:
                    value = filtered_df[col_left].values[0]
                    formatted_value = format_value(value, col_left)
                    if col_left in ["Штук об'єм", "Штук ширина", "Штук вага", "Штук довжина", "Штук висота", "Ящик об'єм", "Ящик ширина (вздовж глибини)", "Ящик вага", "Ящик довжина (до стіни)", "Ящик висота"]:
                        col1.write(f'<p style="color:#023E8A;"><strong>{col_left}:</strong> {formatted_value}</p>', unsafe_allow_html=True)
                    else:
                        col1.write(f"**{col_left}:** {formatted_value}")

                if col_right in filtered_df.columns:
                    value = filtered_df[col_right].values[0]
                    formatted_value = format_value(value, col_right)
                    if col_right in ["Штук об'єм", "Штук ширина", "Штук вага", "Штук довжина", "Штук висота", "Ящик об'єм", "Ящик ширина (вздовж глибини)", "Ящик вага", "Ящик довжина (до стіни)", "Ящик висота"]:
                        col2.write(f'<p style="color:#023E8A;"><strong>{col_right}:</strong> {formatted_value}</p>', unsafe_allow_html=True)
                    else:
                        col2.write(f"**{col_right}:** {formatted_value}")

    else:
        st.write('Не знайдено даних для вказаного ID')

# === Блок 2 ===
styled_line(color='#8bbdd9', height='1px')

st.write('<h1 style="text-align: center;">Фільтрація даних по Зонам</h1>', unsafe_allow_html=True)

# Фіксований порядок зон
fixed_order = ['A', 'C1', 'C3', 'C4', 'D1', 'D2', 'E1', 'E2', 'F1', 'F2', 'G1', 'G2', 'G3', 'H1', 'H2', 'I1', 'I2', 'K1', 'K2', 'Стелаж', '2й поверх 1']

# Отримання унікальних значень зон і сортування за фіксованим порядком
valid_areas = df['Зона'].dropna().unique()
valid_areas = [area for area in valid_areas if pd.notna(area) and area.strip() != '']

# Залишаємо тільки ті зони, що є в фіксованому порядку, і сортуємо їх
valid_areas = [area for area in fixed_order if area in valid_areas]

# Додаємо опції для вибору зон, включаючи "Без зони"
options = ["Вибрати зону", "Без зони"] + valid_areas

selected_area = st.selectbox("", options)

if selected_area == "Вибрати зону":
    st.write("")
else:
    if selected_area == "Без зони":
        # Фільтруємо рядки, де зона не вказана (NaN або пусто)
        filtered_df = df[df['Зона'].isna() | (df['Зона'].str.strip() == '')]
    else:
        # Фільтруємо за вибраною зоною
        filtered_df = df[df['Зона'] == selected_area]
    
    filtered_df.reset_index(drop=True, inplace=True)
    filtered_df.insert(0, '№', filtered_df.index + 1)
    filtered_df['Рядів'] = pd.to_numeric(filtered_df['Рядів'], errors='coerce').round(2)
    filtered_df['Ширина'] = pd.to_numeric(filtered_df['Ширина'], errors='coerce').round(2)

    if not filtered_df.empty:
        treemap_data = filtered_df[['Артикул', 'Ширина']].drop_duplicates(subset='Артикул').dropna(subset=['Ширина'])
        treemap_data = treemap_data[treemap_data['Ширина'] > 0]

        try:
            fig = px.treemap(
                treemap_data,
                path=['Артикул'],
                values='Ширина',
                title=f'Графік для зони {selected_area}',
                color='Ширина',
                color_continuous_scale='Blues'
            )
            
            # Адаптивне відображення графіка
            fig.update_layout(
                autosize=True,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            with st.expander("", expanded=True):
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Помилка при створенні графіка: {e}")
    else:
        st.write("Немає даних для побудови графіка")

    columns_to_display = [
        '№', 'Номенклатура', 'id', 'Категорія', 'Артикул', 'Рядів', 'Ширина'
    ]

    with st.expander("Детальна інформація", expanded=True):
        # Відображення таблиці з прокруткою
        st.markdown("""
            <style>
            .table-container {
                max-width: 100%;
                overflow-x: auto;
            }
            .table {
                width: 100%;
            }
            </style>
        """, unsafe_allow_html=True)

        st.write(
            f'<div class="table-container">{filtered_df[columns_to_display].to_html(index=False, classes="table")}</div>',
            unsafe_allow_html=True
        )
# Блок 3: Загальна інформація по зонам
st.write('<h3 style="text-align: center;">Загальна інформація по зонам</h3>', unsafe_allow_html=True)
df['Ширина'] = pd.to_numeric(df['Ширина'], errors='coerce')

data = {
    'Зона': ['A', 'C1', 'C3', 'C4', 'D1', 'D2', 'E1', 'E2', 'F1', 'F2', 'G1', 'G2', 'G3', 'H1', 'H2', 'I1', 'I2', 'K1', 'K2', 'Стелаж', '2й поверх 1'],
    'Глибина': [8.8, 2.0, 1.2, 1.2, 2.5, 4.0, 3.0, 4.5, 3.0, 6.0, 3.0, 3.0, 3.0, 3.0, 4.5, 3.0, 6.0, 6.9, 4.1, None, None],
    'Ширина': [35.0, 11.0, 12.0, 12.0, 4.0, 7.5, 4.5, 7.0, 6.0, 7.0, 6.0, 7.0, 7.0, 4.5, 7.0, 6.0, 7.0, 16.0, 6.0, None, None]
}

area = pd.DataFrame(data)
area['Ширина'] = pd.to_numeric(area['Ширина'], errors='coerce')

def calculate_total_width(zone):
    filtered_df = df[df['Зона'] == zone]
    total_width = filtered_df['Ширина'].sum()
    return total_width

area['Сума_Ширина'] = area['Зона'].apply(calculate_total_width)
area['Залишок'] = area['Ширина'] - area['Сума_Ширина']

table_styles = """
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        text-align: center;
        padding: 8px;
    }
    th {
        background-color: #f2f2f2;
    }
    </style>
"""

html_table = table_styles + area.to_html(index=False)

with st.expander("Детальна інформація про зони", expanded=False):
    st.write(html_table, unsafe_allow_html=True)

# Роздільник
styled_line(color='#8bbdd9', height='1px')

# Блок 4: Фільтрація даних по 'Category'
st.write('<h1 style="text-align: center;"> Інформація по Категоріям</h1>', unsafe_allow_html=True)

def get_valid_categories(df):
    valid_categories = df['Категорія'].dropna().unique()
    return [category for category in valid_categories if pd.notna(category) and category.strip() != '']

valid_categories = get_valid_categories(df)
options = ["Вибрати категорію"] + valid_categories

selected_category = st.selectbox("", options)

if selected_category == "Вибрати категорію":
    st.write("")
else:
    filtered_df = df[df['Категорія'] == selected_category]
    filtered_df.reset_index(drop=True, inplace=True)
    filtered_df.insert(0, '№', filtered_df.index + 1)
    filtered_df['Рядів'] = pd.to_numeric(filtered_df['Рядів'], errors='coerce').round(2)
    filtered_df['Ширина'] = pd.to_numeric(filtered_df['Ширина'], errors='coerce').round(2)

    columns_to_display = [
        '№', 'Номенклатура', 'id', 'Категорія', 'Артикул', 'Рядів', 'Ширина'
    ]

    with st.expander("Детальна інформація", expanded=True):
        st.write(
            filtered_df[columns_to_display].to_html(index=False),
            unsafe_allow_html=True
        )
