from app.main import add, divide
import pytest

# assert conditon, [message]

def test_add():
  assert add(2, 3) == 5
  assert add(-1, 1) == 0
  assert add(0, 0) == 0

def test_divide():
    assert divide(6, 2) == 3
    assert divide(5, 2) == 2.5

def test_divide_by_zero():
    with pytest.raises(ValueError):
      divide(10, 0)