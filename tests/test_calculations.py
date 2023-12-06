import pytest

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (100, 98, 198)
])
def test_add(num1, num2, expected):
    print('testing add functioin')
    assert num1 + num2 == expected

def test_subtract(): 
    print('testing subtract function')
    assert 8 - 4 == 4
