"""Starter tests for the weather module.

These tests deliberately cover only ordinary examples. They show how pytest works,
but they are not a sufficient test suite for the specification in SPECIFICATION.md.
"""
import pytest
from weather import (
    average_temperature,
    filter_by_temperature,
    hottest_measurement,
    parse_measurement,
    parse_time,
)

def test_parse_time_edge_cases():

    assert parse_time("00:00") == 0
    assert parse_time("23:59") == 1439

def test_parse_time_invalid_format():

    with pytest.raises(ValueError):
        parse_time("1421")
    with pytest.raises(ValueError):
        parse_time("14:21:00")

def test_parse_time_non_numeric():

    with pytest.raises(ValueError):
        parse_time("14:ab")
    with pytest.raises(ValueError):
        parse_time("ab:21")

def test_parse_time_out_of_range():
 
    with pytest.raises(ValueError):
        parse_time("24:00")  
    with pytest.raises(ValueError):
        parse_time("-1:00")
    with pytest.raises(ValueError):
        parse_time("12:60")  




def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)

def test_parse_measurement_invalid_type():
    with pytest.raises(ValueError):
        parse_measurement(12345)

def test_parse_measurement_invalid_fields_count():
    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21")
    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21;21.7;extra")

def test_parse_measurement_empty_city():
    with pytest.raises(ValueError):
        parse_measurement("   ;14:21;21.7")

def test_parse_measurement_invalid_temperature():
    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21;heiß")
    




def test_filter_by_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]
    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]

def test_filter_by_temperature_invalid_range():
    measurements = [("Köln", 600, 10.0)]
    with pytest.raises(ValueError):
        filter_by_temperature(measurements, 20.0, 10.0)

def test_filter_by_temperature_inclusive_boundaries():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 15.0),
        ("Bonn", 900, 20.0),
    ]
    result = filter_by_temperature(measurements, 10.0, 20.0)
    assert len(result) == 3





def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0


def test_average_temperature_city_not_found():
    measurements = [
        ("Köln", 600, 10.0),
    ]
    with pytest.raises(ValueError):
        average_temperature(measurements, "Düsseldorf")




def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)


def test_hottest_measurement_empty_list():
    with pytest.raises(ValueError):
        hottest_measurement([])

def test_hottest_measurement_with_tie_breaker():
    measurements = [
        ("Bonn", 900, 25.0),
        ("Köln", 600, 25.0),         
        ("Düsseldorf", 720, 25.0),
    ]
    
    assert hottest_measurement(measurements) == ("Köln", 600, 25.0)