"""Streamlit-приложение: расстояние между двумя координатами.

Запуск локально:
    streamlit run app.py
"""
import os
import sys

# Гарантируем, что папка, где лежит app.py, есть в sys.path —
# тогда `from geo import ...` работает независимо от рабочего каталога,
# из которого Streamlit Cloud запускает скрипт.
_APP_DIR = os.path.dirname(os.path.abspath(__file__))
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)

import pandas as pd
import streamlit as st

from geo import haversine, parse_coordinates, validate_lat_lon, format_distance

st.set_page_config(
    page_title="Калькулятор расстояний",
    page_icon="📍",
    layout="centered",
)

st.title("📍 Расстояние между двумя точками")
st.caption(
    "Формула гаверсинуса · радиус Земли 6 372 795 м · "
    "координаты можно скопировать из Яндекс Карт"
)

# ---------- Выбор способа ввода ----------
input_mode = st.radio(
    "Способ ввода",
    ["Числовые поля", "Строка координат"],
    horizontal=True,
)

# ---------- Ввод ----------
if input_mode == "Числовые поля":
    colA, colB = st.columns(2)
    with colA:
        st.subheader("Точка A")
        a_lat = st.number_input(
            "Широта A", value=55.753544, format="%.6f",
            min_value=-90.0, max_value=90.0, key="a_lat_num",
        )
        a_lon = st.number_input(
            "Долгота A", value=37.621202, format="%.6f",
            min_value=-180.0, max_value=180.0, key="a_lon_num",
        )
    with colB:
        st.subheader("Точка B")
        b_lat = st.number_input(
            "Широта B", value=55.752023, format="%.6f",
            min_value=-90.0, max_value=90.0, key="b_lat_num",
        )
        b_lon = st.number_input(
            "Долгота B", value=37.617499, format="%.6f",
            min_value=-180.0, max_value=180.0, key="b_lon_num",
        )
else:
    colA, colB = st.columns(2)
    with colA:
        st.subheader("Точка A")
        a_text = st.text_input("Координаты A", value="55.753544, 37.621202")
    with colB:
        st.subheader("Точка B")
        b_text = st.text_input("Координаты B", value="55.752023, 37.617499")

threshold = st.slider(
    "Порог близости, м", min_value=10, max_value=5000, value=200, step=10,
)

# ---------- Расчёт ----------
if st.button("Посчитать", type="primary", use_container_width=True):
    try:
        if input_mode == "Числовые поля":
            lat_a, lon_a, lat_b, lon_b = a_lat, a_lon, b_lat, b_lon
        else:
            lat_a, lon_a = parse_coordinates(a_text)
            lat_b, lon_b = parse_coordinates(b_text)

        validate_lat_lon(lat_a, lon_a)
        validate_lat_lon(lat_b, lon_b)

        d = haversine(lat_a, lon_a, lat_b, lon_b)
        within = d < threshold

        st.metric("Расстояние", format_distance(d))

        if within:
            st.success(f"**da** — ближе {threshold} м (порог пройден)")
        else:
            st.warning(f"**net** — дальше {threshold} м")

        df = pd.DataFrame({"lat": [lat_a, lat_b], "lon": [lon_a, lon_b]})
        st.map(df, zoom=14, use_container_width=True)

        st.caption(
            f"Точка A: ({lat_a:.6f}, {lon_a:.6f}) · "
            f"Точка B: ({lat_b:.6f}, {lon_b:.6f})"
        )

    except ValueError as e:
        st.error(f"Ошибка ввода: {e}")
