from streamlit_searchbox import _list_to_options_js, _list_to_options_py


def test_list_to_options_py_single_values():
    options = [1, 2, "three", 4.0]
    assert _list_to_options_py(options) == options


def test_list_to_options_py_tuples():
    options = [(1, "one"), (2, "two"), ("3", "three")]
    assert _list_to_options_py(options) == ["one", "two", "three"]


def test_list_to_options_py_mixed():
    options = [1, (2, "two"), 3, ("4", "four")]
    assert _list_to_options_py(options) == [1, "two", 3, "four"]


def test_list_to_options_py_empty():
    options = []
    assert _list_to_options_py(options) == []


def test_list_to_options_js_single_values():
    options = [1, 2, "three", 4.0]
    expected = [
        {"label": "1", "value": 0},
        {"label": "2", "value": 1},
        {"label": "three", "value": 2},
        {"label": "4.0", "value": 3},
    ]
    assert _list_to_options_js(options) == expected


def test_list_to_options_js_tuples():
    options = [(1, "one"), (2, "two"), ("3", "three")]
    expected = [
        {"label": "1", "value": 0},
        {"label": "2", "value": 1},
        {"label": "3", "value": 2},
    ]
    assert _list_to_options_js(options) == expected


def test_list_to_options_js_mixed():
    options = [1, (2, "two"), 3, ("4", "four")]
    expected = [
        {"label": "1", "value": 0},
        {"label": "2", "value": 1},
        {"label": "3", "value": 2},
        {"label": "4", "value": 3},
    ]
    assert _list_to_options_js(options) == expected


def test_list_to_options_js_empty():
    options = []
    assert _list_to_options_js(options) == []
