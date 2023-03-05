from typing import List, Tuple
import time
import requests
import streamlit as st
import random
from streamlit_searchbox import st_searchbox
import enum


def search_wikipedia_ids(searchterm: str) -> List[Tuple[str, any]]:
    """
    function with list of tuples (label:str, value:any)
    """
    # you can use a nice default here
    if not searchterm:
        return []

    # search that returns a list of wiki articles in dict form with information on title, id, etc.
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


def search_sth_fast(searchterm: str) -> List[str]:
    """
    function with list of strings
    """
    return [f"{searchterm}_{i}" for i in range(10)]


def search_rnd_delay(searchterm: str) -> List[str]:
    print(f"searching... {searchterm}")
    time.sleep(random.randint(1, 5))
    return [f"{searchterm}_{i}" for i in range(10)]


def search_fancy_return(_: str):
    e = enum.Enum("FancyEnum", {"a": 1, "b": 2, "c": 3})
    return [e.a, e.b, e.c]


#################################
#### application starts here ####
#################################


c1, c2, c3 = st.columns(3)


with st.sidebar:
    selected_value = st_searchbox(
        search_function=search_wikipedia_ids,
        placeholder="Search Wikipedia",
        label="search_wikipedia_ids",
        default="SOME DEFAULT",
        clear_on_submit=False,
        clearable=True,
        key="search_wikipedia_ids",
    )
    st.info(f"{selected_value}")


c1, c2, c3 = st.columns(3)

with c1:

    selected_value2 = st_searchbox(
        search_sth_fast,
        default=None,
        label="search_sth_fast",
        clear_on_submit=True,
        key="search_sth_fast",
    )
    st.info(f"{selected_value2}")

with c2:
    selected_value3 = st_searchbox(
        search_rnd_delay,
        default=None,
        clear_on_submit=False,
        clearable=True,
        label="search_rnd_delay",
        key="search_rnd_delay",
    )
    st.info(f"{selected_value3}")

with c3:
    st.multiselect("For visual reference", [1, 2, 3], default=[1, 2])

st.markdown("---")

st.write("search_fancy_return (no label)")

# TODO: hangs on selection?
selected_value4 = st_searchbox(
    search_fancy_return,
    clear_on_submit=True,
    key="search_fancy_return",
)
st.info(f"{selected_value4} {type(selected_value4)}")


st.markdown("---")
st.header("Other components for reference:")
st.multiselect(
    "Multiselect",
    [1, 2, 3, 4, 5],
    default=[1, 2],
    key="multiselect",
)
st.selectbox(
    "Selectbox",
    [1, 2, 3],
    index=1,
    key="selectbox",
)
