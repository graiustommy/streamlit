import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# Настройка страницы (должна быть первой командой)
st.set_page_config(
    page_title="Мое Streamlit приложение",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Заголовок приложения
st.title("📊 Панель аналитики данных")
st.markdown("---")

# Боковая панель для фильтров
with st.sidebar:
    st.header("⚙️ Настройки")
    
    # Выбор режима
    mode = st.radio(
        "Выберите режим работы:",
        ["Визуализация данных", "Загрузка файла", "Генерация данных", "Калькулятор"],
        index=0
    )
    
    st.markdown("---")
    
    # Прогресс
    if st.button("Показать информацию"):
        st.info("Это пример приложения Streamlit с различными функциями!")

# Основной контент в зависимости от выбранного режима
if mode == "Визуализация данных":
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Генерация данных и график")
        
        # Параметры для генерации
        n_points = st.slider("Количество точек:", 10, 500, 100)
        noise = st.slider("Уровень шума:", 0.0, 2.0, 0.5)
        
        # Генерация данных
        x = np.linspace(0, 10, n_points)
        y = np.sin(x) + np.random.normal(0, noise, n_points)
        
        # Создание DataFrame для отображения
        df_plot = pd.DataFrame({
            'X': x,
            'Sin(x)': np.sin(x),
            'Зашумленные данные': y
        })
        
        # Используем line_chart для тренда
        st.write("**Линия тренда (sin(x))**")
        st.line_chart(df_plot.set_index('X')[['Sin(x)']])
        
        st.write("**Зашумленные данные**")
        st.scatter_chart(df_plot.set_index('X')[['Зашумленные данные']])
    
    with col2:
        st.subheader("📊 Статистика данных")
        
        # Вычисляем ошибки
        errors = y - np.sin(x)
        
        # Создаем DataFrame для гистограммы
        df_errors = pd.DataFrame({
            'Ошибка': errors
        })
        
        st.write("**Гистограмма ошибок**")
        st.bar_chart(df_errors['Ошибка'].value_counts().sort_index().head(20))
        
        st.write("**Статистика ошибок:**")
        st.write(f"- Среднее: {np.mean(errors):.4f}")
        st.write(f"- Стандартное отклонение: {np.std(errors):.4f}")
        st.write(f"- Минимум: {np.min(errors):.4f}")
        st.write(f"- Максимум: {np.max(errors):.4f}")

elif mode == "Загрузка файла":
    st.subheader("📁 Загрузка данных из файла")
    
    uploaded_file = st.file_uploader("Выберите CSV файл", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Читаем CSV файл
            df = pd.read_csv(uploaded_file)
            
            st.success(f"Файл успешно загружен! Размер: {df.shape}")
            
            # Просмотр данных
            st.subheader("Предпросмотр данных")
            st.dataframe(df.head(10))
            
            # Информация о данных
            st.subheader("Статистика по данным")
            st.write(df.describe())
            
            # Отображение типов столбцов
            st.subheader("Типы данных")
            st.write(df.dtypes)
            
            # Выбор столбцов для визуализации
            st.subheader("Быстрая визуализация")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 2:
                x_col = st.selectbox("Выберите столбец для оси X:", numeric_cols)
                y_col = st.selectbox("Выберите столбец для оси Y:", numeric_cols)
                
                if st.button("Построить график"):
                    chart_data = df[[x_col, y_col]].dropna()
                    st.scatter_chart(chart_data.set_index(x_col)[[y_col]])
        
        except Exception as e:
            st.error(f"Ошибка при чтении файла: {str(e)}")

elif mode == "Генерация данных":
    st.subheader("🎲 Генерация случайных данных")
    
    # Форма для ввода параметров
    with st.form("data_generation_form"):
        rows = st.number_input("Количество строк:", min_value=1, max_value=10000, value=100)
        
        col1_name = st.text_input("Название первого столбца:", "column_1")
        col2_name = st.text_input("Название второго столбца:", "column_2")
        
        distribution = st.selectbox("Тип распределения:", 
                                   ["Нормальное", "Равномерное", "Экспоненциальное"])
        
        generate_btn = st.form_submit_button("Сгенерировать данные")
    
    if generate_btn:
        with st.spinner("Генерация данных..."):
            time.sleep(1)  # Имитация загрузки
            
            # Генерация данных в зависимости от распределения
            if distribution == "Нормальное":
                data1 = np.random.normal(0, 1, rows)
                data2 = np.random.normal(5, 2, rows)
            elif distribution == "Равномерное":
                data1 = np.random.uniform(0, 10, rows)
                data2 = np.random.uniform(-5, 5, rows)
            else:  # Экспоненциальное
                data1 = np.random.exponential(1, rows)
                data2 = np.random.exponential(2, rows)
            
            df = pd.DataFrame({
                col1_name: data1,
                col2_name: data2,
                'index': range(rows)
            })
            
            st.success(f"Сгенерировано {rows} строк данных!")
            
            # Отображение данных
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(df.head(20))
            
            with col2:
                # Статистика
                st.write("Статистика:")
                st.write(df[[col1_name, col2_name]].describe())
            
            # Визуализация с помощью встроенных инструментов
            st.subheader("Визуализация данных")
            chart_df = df[[col1_name, col2_name]].dropna()
            
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.write(f"**{col1_name} - {col2_name}**")
                st.scatter_chart(chart_df.set_index(col1_name)[[col2_name]])
            
            with col_chart2:
                st.write(f"**Гистограмма {col1_name}**")
                st.bar_chart(df[col1_name].value_counts().sort_index().head(20))
            
            # Кнопка скачивания
            csv = df.to_csv(index=False)
            st.download_button(
                label="Скачать данные в CSV",
                data=csv,
                file_name=f"generated_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

else:  # Калькулятор
    st.subheader("🧮 Простой калькулятор")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        num1 = st.number_input("Первое число:", value=0.0, step=0.1)
    
    with col2:
        operation = st.selectbox("Операция:", ["+", "-", "*", "/", "^", "sqrt"])
    
    with col3:
        if operation in ["+", "-", "*", "/", "^"]:
            num2 = st.number_input("Второе число:", value=0.0, step=0.1)
    
    # Результат
    if st.button("Вычислить"):
        try:
            if operation == "+":
                result = num1 + num2
                symbol = "+"
                second = num2
            elif operation == "-":
                result = num1 - num2
                symbol = "-"
                second = num2
            elif operation == "*":
                result = num1 * num2
                symbol = "×"
                second = num2
            elif operation == "/":
                if num2 != 0:
                    result = num1 / num2
                    symbol = "÷"
                    second = num2
                else:
                    st.error("Деление на ноль!")
                    st.stop()
            elif operation == "^":
                result = num1 ** num2
                symbol = "^"
                second = num2
            else:  # sqrt
                if num1 >= 0:
                    result = np.sqrt(num1)
                    symbol = "√"
                    second = ""
                else:
                    st.error("Квадратный корень из отрицательного числа!")
                    st.stop()
            
            st.markdown(f"### Результат: {num1} {symbol} {second} = {result:.6f}")
            
        except Exception as e:
            st.error(f"Ошибка: {str(e)}")
    
    # Исторический прогресс (просто для демонстрации)
    if st.checkbox("Показать пример прогресса"):
        progress_bar = st.progress(0)
        for i in range(100):
            progress_bar.progress(i + 1)
            time.sleep(0.01)
        st.success("Готово!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        Создано с помощью Streamlit
    </div>
    """,
    unsafe_allow_html=True
)

# Вывод метрики в боковую панель
with st.sidebar:
    st.markdown("---")
    st.metric("Версия Streamlit", "1.56.0")
