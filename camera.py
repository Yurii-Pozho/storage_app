import streamlit as st

# JavaScript для запуску камери і сканування штрих-кодів
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

# Відображення кнопки та поля для результату
st.write(quagga_js, unsafe_allow_html=True)

# Поле для введення штрих-коду після сканування
barcode_input = st.text_input('Штрих-код', key="barcode_result")

# Обробка після зчитування
if barcode_input:
    st.write(f"Зчитаний штрих-код: {barcode_input}")
