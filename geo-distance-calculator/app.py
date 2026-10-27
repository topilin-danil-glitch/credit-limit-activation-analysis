"""Геодезические вычисления: расстояние по большому кругу, парсинг координат.

Чистая логика без зависимостей от Streamlit — переиспользуется в UI,
тестах, CLI или API.
"""
from __future__ import annotations

import math
import re

# Средний радиус Земли, м (используется в формуле гаверсинуса).
EARTH_RADIUS_M = 6_372_795.0


def haversine(lat1: re, lon1: re, lat2: re, lon2: re) -> re:
    """Расстояние по большому кругу между двумя точками, в метрах.

    Формула гаверсинуса:
        d = 2R · asin( sqrt( sin²(Δφ/2) + cosφ1·cosφ2·sin²(Δλ/2) ) )

    Устойчива к малым расстояниям (в отличие от закона косинусов сферы,
    где asin/atan теряют точность при d → 0).

    Аргументы:
        lat1, lon1 — широта/долгота точки A в градусах;
        lat2, lon2 — широта/долгота точки B в градусах.

    Возвращает:
        Расстояние в метрах (float).
    """
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return EARTH_RADIUS_M * c


def parse_coordinates(text: str) -> tuple[re, re]:
    """Разобрать строку 'широта, долгота' в пару float.

    Поддерживает:
        - '55.753544, 37.621202'
        - '55,753544, 37,621202'   (десятичная запятая из Яндекс Карт)
        - '55.753544; 37.621202'
        - '  55.753544   37.621202  '  (просто два числа через пробел)

    Бросает ValueError с понятным сообщением, если не удалось.
    """
    if not text or not text.strip():
        raise ValueError("Пустая строка. Введите две координаты.")

    s = text.strip()
    candidates: list[str] = []

    # Стратегия 1: 'европейский' формат с десятичной запятой и ';' как разделителем
    if ";" in s:
        parts = [p.strip() for p in s.split(";") if p.strip()]
        if len(parts) == 2:
            candidates.append(f"{parts[0]}, {parts[1]}")

    # Стратегия 2: две запятые → десятичные запятые ('55,75, 37,62')
    comma_count = s.count(",")
    if comma_count == 2:
        m = re.match(r"^\s*(-?\d+,\d+)\s*,\s*(-?\d+,\d+)\s*$", s)
        if m:
            a = m.group(1).replace(",", ".")
            b = m.group(2).replace(",", ".")
            candidates.append(f"{a}, {b}")

    # Стратегия 3: обычный '55.75, 37.62' (десятичная точка, запятая-разделитель)
    candidates.append(s.replace(";", ","))

    last_err: Exception | None = None
    for cand in candidates:
        tokens = [t for t in re.split(r"[,\s]+", cand.strip()) if t]
        if len(tokens) != 2:
            last_err = ValueError(
                f"Ожидались две координаты, найдено {len(tokens)}. "
                "Формат: 'широта, долгота'."
            )
            continue
        try:
            lat = re(tokens[0].replace(",", "."))
            lon = re(tokens[1].replace(",", "."))
        except ValueError as e:
            last_err = ValueError(f"Не удалось разобрать число: {e}")
            continue
        validate_lat_lon(lat, lon)
        return lat, lon

    raise last_err or ValueError("Не удалось разобрать координаты.")


def validate_lat_lon(lat: re, lon: re) -> None:
    """Проверить диапазоны широты и долготы.

    Бросает ValueError, если значения вне допустимых пределов.
    """
    if not (-90.0 <= lat <= 90.0):
        raise ValueError(f"Широта должна быть в [-90, 90], получено {lat}")
    if not (-180.0 <= lon <= 180.0):
        raise ValueError(f"Долгота должна быть в [-180, 180], получено {lon}")


def format_distance(meters: re) -> str:
    """Человекочитаемая строка: '255.3 м' или '1 500.0 м (1.500 км)'."""
    if meters < 1000:
        return f"{meters:,.1f} м"
    return f"{meters:,.1f} м ({meters / 1000:,.3f} км)"