from __future__ import annotations

import enum
import logging
import random
import time
from typing import Any, List

import requests
import streamlit as st

from streamlit_searchbox import st_searchbox

logging.getLogger("streamlit_searchbox").setLevel(logging.DEBUG)

st.set_page_config(layout="centered", page_title="Searchbox Demo")


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


def search_kwargs(searchterm: str, **kwargs) -> List[str]:
    return [f"{searchterm}_{len(kwargs)}" for i in range(10)]


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
        key=search_wikipedia_ids.__name__,
    ),
    dict(
        search_function=search,
        default=None,
        label=search.__name__,
        clear_on_submit=False,
        key=search.__name__,
    ),
    dict(
        search_function=search_rnd_delay,
        default=None,
        clear_on_submit=False,
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
        default="initial",
        default_options=["inital", "list", "of", "options"],
        key=f"{search.__name__}_default_options_all",
        label=f"{search.__name__}_default_options_all",
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
    dict(
        search_function=search,
        key=f"{search.__name__}_edit_current_after_submit",
        edit_after_submit="current",
        label=f"{search.__name__}_edit_current_after_submit",
    ),
    dict(
        search_function=search,
        key=f"{search.__name__}_edit_option_after_submit",
        edit_after_submit="option",
        label=f"{search.__name__}_edit_option_after_submit",
    ),
    dict(
        search_function=search,
        key=f"{search.__name__}_edit_concat_after_submit",
        edit_after_submit="concat",
        label=f"{search.__name__}_edit_concat_after_submit",
    ),
    dict(
        search_function=search_kwargs,
        key=f"{search_kwargs.__name__}_kwargs",
        label=f"{search_kwargs.__name__}_kwargs",
        a=1,
        b=2,
    ),
]


searchboxes, visual_ref, form_example, manual_example = st.tabs(
    ["Searchboxes", "Visual Reference", "Form Example", "Manual Example"]
)

with searchboxes:
    # iterate over boxes in groups of 3, fit into columns
    for box_l in [boxes[i : i + 2] for i in range(0, len(boxes), 2)]:
        cols = st.columns(2)

        for i, box in enumerate(box_l):
            with cols[i]:
                selected_value = st_searchbox(**box)  # type: ignore

                if selected_value:
                    st.info(f"{selected_value} {type(selected_value)}")

        st.markdown("---")


with visual_ref:
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

with form_example:
    with st.form("myform"):
        c1, c2 = st.columns(2)
        with c1:
            sr = st_searchbox(
                search_function=search,
                key=f"{search.__name__}_form",
            )
        with c2:
            st.form_submit_button("load suggestions")

        submit = st.form_submit_button("real submit")
        if submit:
            st.write("form submitted")
            st.write(sr)

with manual_example:
    key = f"{search.__name__}_manual"

    if key in st.session_state:
        st.session_state[key]["options_js"] = [
            {"label": f"{st.session_state[key]['search']}_{i}", "value": i}
            for i in range(5)
        ]
        st.session_state[key]["options_py"] = [i for i in range(5)]

    manual = st_searchbox(
        search_function=lambda _: [],
        key=key,
    )

    st.write(manual)
