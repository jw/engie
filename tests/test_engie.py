from fastapi.testclient import TestClient

from engie.main import app, converter

client = TestClient(app)


def test_converter():
    assert converter(["A", "B"]) == [650, 660]
    assert converter(["H", "h"]) == [0, 0]
    assert converter(["x", "y"]) == [0, 0]
    assert converter(["A", "h", "H", "x"]) == [650, 0, 0, 0]
    assert converter(["A", "B", "C", "D"]) == [650, 660, 670, 680]
    assert converter([]) == []
    assert converter(["A"] * 1000) == [650] * 1000
    assert converter(["A", "h"] * 10) == [650, 0] * 10


def test_read_main():
    response = client.post("/convert", json={"data": ["A", "h", "H", "x"]})
    assert response.status_code == 200
    assert response.json() == {"result": [650, 0, 0, 0]}
