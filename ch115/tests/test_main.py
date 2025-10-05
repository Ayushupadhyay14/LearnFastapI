from app.main import add, divide
import pytest

def test_add():
  assert add(2, 3) == 5

def test_divide():
    assert divide(6, 2) == 3

def test_divide_by_zero():
    with pytest.raises(ValueError):
      divide(10, 0)

