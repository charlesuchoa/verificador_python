from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_soma_comutativa(x, y):
    assert x + y == y + x