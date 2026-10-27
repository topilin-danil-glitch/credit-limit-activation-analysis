"""Тесты для geo.py. Эталоны — из Яндекс Карт / независимой проверки."""
import math
import pytest

from geo import (
    EARTH_RADIUS_M,
    haversine,
    parse_coordinates,
    validate_lat_lon,
    format_distance,
)


class TestHaversine:
    def test_zero_distance(self):
        assert haversine(55.75, 37.62, 55.75, 37.62) == pytest.approx(0.0, abs=1e-6)

    def test_known_pair_moscow(self):
        # Красная площадь → Кремль (Спасская башня), эталон ≈ 255 м
        d = haversine(55.753544, 37.621202, 55.752023, 37.617499)
        assert d == pytest.approx(255, abs=5)

    def test_equator_one_degree_lon(self):
        # На экваторе 1° долготы ≈ 111.32 км
        d = haversine(0.0, 0.0, 0.0, 1.0)
        assert d == pytest.approx(111_320, abs=200)

    def test_one_degree_lat_anywhere(self):
        # 1° широты почти не зависит от долготы: ≈ 111.2 км
        assert haversine(0.0, 0.0, 1.0, 0.0) == pytest.approx(111_195, abs=300)
        assert haversine(55.0, 30.0, 56.0, 30.0) == pytest.approx(111_195, abs=300)

    def test_symmetry(self):
        d1 = haversine(55.75, 37.62, 59.93, 30.31)
        d2 = haversine(59.93, 30.31, 55.75, 37.62)
        assert d1 == pytest.approx(d2)

    def test_moscow_spb(self):
        # Москва → Санкт-Петербург по прямой ≈ 635 км
        d = haversine(55.7558, 37.6173, 59.9343, 30.3351)
        assert d == pytest.approx(635_000, rel=0.01)

    def test_haversine_stable_for_tiny_distance(self):
        # 1 метр по широте: Δφ = 1 / R
        dlat = math.degrees(1.0 / EARTH_RADIUS_M)
        d = haversine(55.0, 37.0, 55.0 + dlat, 37.0)
        assert d == pytest.approx(1.0, abs=1e-3)


class TestParse:
    @pytest.mark.parametrize("text,expected", [
        ("55.753544, 37.621202", (55.753544, 37.621202)),
        ("55,753544, 37,621202", (55.753544, 37.621202)),
        ("55.753544; 37.621202", (55.753544, 37.621202)),
        ("  55.753544   37.621202  ", (55.753544, 37.621202)),
        ("-33.8688, 151.2093", (-33.8688, 151.2093)),
    ])
    def test_parse_ok(self, text, expected):
        assert parse_coordinates(text) == pytest.approx(expected)

    @pytest.mark.parametrize("bad", ["", "   ", "abc", "55.75", "55.75, 37.62, 10"])
    def test_parse_bad(self, bad):
        with pytest.raises(ValueError):
            parse_coordinates(bad)

    def test_parse_out_of_range(self):
        with pytest.raises(ValueError):
            parse_coordinates("100, 37")
        with pytest.raises(ValueError):
            parse_coordinates("55, 200")


class TestValidate:
    def test_ok(self):
        validate_lat_lon(0, 0)
        validate_lat_lon(-90, -180)
        validate_lat_lon(90, 180)

    def test_bad(self):
        with pytest.raises(ValueError):
            validate_lat_lon(90.1, 0)
        with pytest.raises(ValueError):
            validate_lat_lon(0, 180.1)


def test_format_distance():
    assert "м" in format_distance(255.3)
    assert "км" in format_distance(1500)