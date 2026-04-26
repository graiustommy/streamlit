import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
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
    
    # Тема оформления
    theme = st.selectbox("Выберите тему:", ["Светлая", "Темная"])
    
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
        
        df = pd.DataFrame({
            'x': x,
            'y': y,
            'sin(x)': np.sin(x)
        })
        
        # Создание графика с помощью plotly
        fig = px.line(df, x='x', y=['y', 'sin(x)'], 
                      title=f'Сравнение зашумленных данных с sin(x)',
                      labels={'x': 'X ось', 'value': 'Значение'},
                      template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Гистограмма")
        
        # Гистограмма распределения ошибок
        errors = y - np.sin(x)
        fig2 = px.histogram(errors, nbins=30, 
                           title='Распределение ошибок',
                           labels={'value': 'Ошибка', 'count': 'Частота'},
                           color_discrete_sequence=['skyblue'])
        fig2.update_layout(bargap=0.1)
        st.plotly_chart(fig2, use_container_width=True)

elif mode == "Загрузка файла":
    st.subheader("📁 Загрузка данных из файла")
    
    uploaded_file = st.file_uploader("Выберите CSV или Excel файл", 
                                     type=['csv', 'xlsx', 'xls'])
    
    if uploaded_file is not None:
        try:
            # Определяем тип файла и читаем
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
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
            cols = st.multiselect("Выберите столбцы для графика:", df.columns)
            
            if len(cols) >= 2:
                fig = px.scatter(df, x=cols[0], y=cols[1], 
                                title=f'{cols[1]} vs {cols[0]}',
                                trendline="ols")
                st.plotly_chart(fig)
        
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
            
            # Визуализация
            fig = px.scatter(df, x=col1_name, y=col2_name, 
                           title='Диаграмма рассеяния',
                           opacity=0.6)
            st.plotly_chart(fig)
            
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
        Создано с помощью Streamlit • 
        <a href='https://streamlit.io'>Документация</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Вывод метрики в боковую панель (альтернативный способ)
with st.sidebar:
    st.markdown("---")
    st.metric("Текущая версия Streamlit", "1.28.0")
