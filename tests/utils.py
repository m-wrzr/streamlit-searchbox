from __future__ import annotations

import enum
import random
import time
from typing import Any, List

import requests
import streamlit as st


def search_wikipedia_ids(searchterm: str) -> List[tuple[str, Any]]:
    """
    function with list of tuples (label:str, value:any)
    """
    # you can use a nice default here
    if not searchterm:
        return []

    # search that returns a list of wiki articles in dict form
    # with information on title, id, etc
    response = requests.get(
        "http://en.wikipedia.org/w/api.php",
        params={
            "list": "search",
            "format": "json",
            "action": "query",
            "srlimit": 10,
            "limit": 10,
            "srsearch": searchterm,
        },
        timeout=5,
    ).json()["query"]["search"]

    # first element will be shown in search, second is returned from component
    return [
        (
            str(article["title"]),
            article["pageid"],
        )
        for article in response
    ]


def search(searchterm: str) -> List[str]:
    return [f"{searchterm}_{i}" for i in range(10)]


def search_rnd_delay(searchterm: str) -> List[str]:
    time.sleep(random.randint(1, 5))
    return [f"{searchterm}_{i}" for i in range(10)]


def search_enum_return(_: str):
    e = enum.Enum("FancyEnum", {"a": 1, "b": 2, "c": 3})
    return [e.a, e.b, e.c]


def search_empty_list(_: str):
    if not st.session_state.get("search_empty_list_n", None):
        st.session_state["search_empty_list_n"] = 1
        return ["a", "b", "c"]

    return []


def selection_to_text(result):
    return f"result={result} type={type(result).__name__}"


#################################
#### application starts here ####
#################################


# searchbox configurations, see __init__.py for details
# will pass all kwargs to the searchbox component
boxes = [
    dict(
        search_function=search_wikipedia_ids,
        placeholder="Search Wikipedia",
        label=search_wikipedia_ids.__name__,
        default="SOME DEFAULT",
        clear_on_submit=False,
        clearable=True,
        key=search_wikipedia_ids.__name__,
    ),
    dict(
        search_function=search,
        default=None,
        label=search.__name__,
        clear_on_submit=True,
        key=search.__name__,
    ),
    dict(
        search_function=search_rnd_delay,
        default=None,
        clear_on_submit=False,
        clearable=True,
        label=search_rnd_delay.__name__,
        key=search_rnd_delay.__name__,
    ),
    dict(
        search_function=search_enum_return,
        clear_on_submit=True,
        key=search_enum_return.__name__,
        label=search_enum_return.__name__,
    ),
    dict(
        search_function=search_empty_list,
        clear_on_submit=True,
        key=search_empty_list.__name__,
        label=search_empty_list.__name__,
    ),
    dict(
        search_function=search,
        default_options=["inital", "list", "of", "options"],
        key=f"{search.__name__}_default_options",
        label=f"{search.__name__}_default_options",
    ),
    dict(
        search_function=search,
        default_options=[("inital", "i"), ("list", "l")],
        key=f"{search.__name__}_default_options_tuple",
        label=f"{search.__name__}_default_options_tuple",
    ),
    dict(
        search_function=search,
        key=f"{search.__name__}_rerun_disabled",
        rerun_on_update=False,
        label=f"{search.__name__}_rerun_disabled",
    ),
]
