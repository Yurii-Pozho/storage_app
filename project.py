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

#===== Блок 1: Фільтрація даних за введеним ID =====
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

st.write('<h1 style="text-align: center;">Перегляд даних за ID або Штрих-кодом</h1>', unsafe_allow_html=True)

# JavaScript для сканування штрих-коду
quagga_js = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/quagga/0.12.1/quagga.min.js"></script>
    <script>
    function startScanner() {
        var App = {
            init: function() {
                Quagga.init(this.state, function(err) {
                    if (err) {
                        console.log(err);
                        return;
                    }
                    App.attachListeners();
                    Quagga.start();
                });
            },
            state: {
                inputStream: {
                    type: "LiveStream",
                    constraints: {
                        width: 640,
                        height: 480,
                        facingMode: "environment" // використання основної камери
                    },
                },
                decoder: {
                    readers: ["code_128_reader", "ean_reader"] // Різні типи штрих-кодів
                }
            },
            attachListeners: function() {
                Quagga.onDetected(function(result) {
                    document.getElementById("barcode_result").value = result.codeResult.code;
                    Quagga.stop(); // Зупинка сканера після зчитування
                });
            }
        };

        App.init();
    }
    </script>
    <button onclick="startScanner()">📷 Сканувати штрих-код</button>
    <input id="barcode_result" type="text" placeholder="Результат штрих-коду">
"""

# Виведення кнопки для сканування штрих-коду та поля введення
st.write(quagga_js, unsafe_allow_html=True)

# Поле для вводу ID або зчитаного штрих-коду
id_input = st.text_input('Введіть ID або Штрих-код', key="barcode_result")

# Обробка введення
if id_input:
    filtered_df = df[df['id'] == int(id_input)]  # Пошук по ID
    
    if not filtered_df.empty:
        with st.expander("Інформація для вибраного ID:", expanded=True):
            # Відображення зображення
            if 'Image' in filtered_df.columns:
                for img_path in filtered_df['Image']:
                    image = load_image(img_path)
                    if image:
                        new_size = (400, 300)
                        resized_image = image.resize(new_size, Image.LANCZOS)
                        st.image(resized_image, width=200)
            
            # Відображення таблиці в два стовпці
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
                    if isinstance(value, (int, float)):
                        if column_name in ["id", "Артикул"]:
                            return value
                        return f"{float(value):.2f}"
                    else:
                        return value
                except ValueError:
                    return value

            for i, (col_left, col_right) in enumerate(column_mapping.items()):
                if col_left in filtered_df.columns:
                    value = filtered_df[col_left].values[0]
                    formatted_value = format_value(value, col_left)
                    col1.write(f"**{col_left}:** {formatted_value}")

                if col_right in filtered_df.columns:
                    value = filtered_df[col_right].values[0]
                    formatted_value = format_value(value, col_right)
                    col2.write(f"**{col_right}:** {formatted_value}")
    else:
        st.write('Не знайдено даних для вказаного ID або Штрих-коду')

# === Блок 2 ===
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os

# Блок 2: Фільтрація даних по 'Area'
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
    # Відображення таблиці з прокруткою та налаштуванням шрифта
        st.markdown("""
            <style>
            .table-container {
                max-width: 100%;
                overflow-x: auto;
            }

            /* Шрифт для десктопів */
            .table {
                font-size: 14px; /* Розмір шрифту для десктопу */
                width: 100%;
            }

            /* Шрифт для мобільних пристроїв */
            @media only screen and (max-width: 600px) {
                .table {
                    font-size: 10px; /* Розмір шрифту для мобільних пристроїв */
                    min-width: 300px; /* Мінімальна ширина таблиці для мобільних пристроїв */
                }
            }
            </style>
            <div class="table-container">
                <table class="table">
                    <!-- Тут буде ваша таблиця або дані -->
                </table>
            </div>
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
    .table-container {
        max-width: 100%;
        overflow-x: auto;
        font-size: 9px; /* Розмір шрифта таблиці */
    }
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
    .table {
        min-width: 50px; /* Мінімальна ширина таблиці для мобільних пристроїв */
    }
    </style>
"""

html_table = table_styles + '<div class="table-container">' + area.to_html(index=False, classes="table") + '</div>'

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

    # CSS for mobile responsiveness with horizontal scroll
    css = """
    <style>
    .table-container {
        overflow-x: auto;
    }
    .dataframe {
        border-collapse: collapse;
        width: 100%;
    }
    .dataframe th, .dataframe td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    .dataframe th {
        background-color: #f2f2f2;
    }
    @media only screen and (max-width: 600px) {
        .dataframe th, .dataframe td {
            font-size: 12px;
            padding: 4px;
        }
        .dataframe {
            font-size: 12px;
        }
    }
    </style>
    """

    st.write(css, unsafe_allow_html=True)

    with st.expander("Детальна інформація", expanded=True):
        html_table = filtered_df[columns_to_display].to_html(index=False, classes='dataframe')
        st.markdown(f'<div class="table-container">{html_table}</div>', unsafe_allow_html=True)