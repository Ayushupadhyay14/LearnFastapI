from app.main import add, divide
import pytest

@pytest.fixture
def setup_data():
  return {"a": 10, "b": 5}

def test_add_with_fixture(setup_data):
  assert add(setup_data["a"], setup_data["b"]) == 15

@pytest.mark.parametrize("a, b, expected", [(2, 3, 5), (-1, 1, 0), (0, 0, 0)])
def test_add_params(a, b, expected):
  assert add(a, b) == expected

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
  pass