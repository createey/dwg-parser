# dwg_parser/tests/test_data_converter.py
import pytest
from dwg_parser.data_converter import DataConverter
from dwg_parser.entities import Point, Line, Circle

def test_convert_point():
    converter = DataConverter()
    raw_data = {'x': 1.0, 'y': 2.0, 'z': 3.0}
    point = converter.convert_point(raw_data)
    assert isinstance(point, Point)
    assert point.x == 1.0
    assert point.y == 2.0
    assert point.z == 3.0

def test_convert_line():
    converter = DataConverter()
    raw_data = {
        'start': {'x': 0.0, 'y': 0.0, 'z': 0.0},
        'end': {'x': 1.0, 'y': 1.0, 'z': 0.0},
        'layer': 'test_layer',
        'handle': 123
    }
    line = converter.convert_line(raw_data)
    assert isinstance(line, Line)
    assert line.start.x == 0.0
    assert line.end.x == 1.0
    assert line.layer == 'test_layer'