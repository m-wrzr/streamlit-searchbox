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
        headers={
            "User-Agent": "StreamlitSearchboxExample/1.0 (https://github.com/m-wrzr/streamlit-searchbox)"
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
        search_function=search,
        default=None,
        label=f"{search.__name__}_debounce_250ms",
        clear_on_submit=False,
        debounce=250,
        key=f"{search.__name__}_debounce_250ms",
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
        default="initial",
        default_searchterm="initial",
        default_options=["initial", "list", "of", "options"],
        key=f"{search.__name__}_default_options",
        label=f"{search.__name__}_default_options",
        style_overrides={
            "clear": {"width": 25, "height": 25},
            "searchbox": {"option": {"highlight": "#f1660f"}, "optionEmpty": "hidden"},
        },
    ),
    dict(
        search_function=search,
        default="initial",
        default_options=["initial", "list", "of", "options"],
        key=f"{search.__name__}_default_options_all",
        label=f"{search.__name__}_default_options_all",
    ),
    dict(
        search_function=search,
        default_options=[("initial", "i"), ("list", "l")],
        key=f"{search.__name__}_default_options_tuple",
        label=f"{search.__name__}_default_options_tuple",
    ),
    dict(
        search_function=search,
        key=f"{search.__name__}_default_use_searchterm",
        default_use_searchterm=True,
        label=f"{search.__name__}_default_use_searchterm",
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
    dict(
        search_function=search,
        reset_function=lambda: print("reset function called"),
        key=f"{search.__name__}_reset_function",
        label=f"{search.__name__}_reset_function",
    ),
    dict(
        search_function=search,
        default=None,
        label=f"{search.__name__}_override_style",
        clear_on_submit=False,
        key=f"{search.__name__}_override_style",
        style_overrides={
            "clear": {
                "width": 20,
                "height": 20,
                "icon": "circle-unfilled",
                "stroke-width": 2,
                "stroke": "red",
            },
            "dropdown": {
                "rotate": True,
                "width": 30,
                "height": 30,
            },
            "searchbox": {
                "menuList": {"backgroundColor": "transparent"},
                "singleValue": {"color": "red"},
                "option": {"color": "blue", "backgroundColor": "yellow"},
            },
        },
    ),
    dict(
        search_function=search_wikipedia_ids,
        placeholder="Search Wikipedia",
        label="search with help text",
        default="SOME DEFAULT",
        help="help text",
        clear_on_submit=False,
        key=f"{search.__name__}_help_icon",
    ),
]


searchboxes, visual_ref, form_example, manual_example, fragment_example = st.tabs(
    [
        "Searchboxes",
        "Visual Reference",
        "Form Example",
        "Manual Example",
        "Fragment Example",
    ]
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

    st_searchbox(
        search_function=search,
        key=f"{search.__name__}_style_manual",
        style_overrides={
            "clear": {
                "width": 20,
                "height": 20,
                "icon": "circle-unfilled",
                "stroke-width": 2,
                "stroke": "red",
            },
            "dropdown": {
                "rotate": True,
                "width": 30,
                "height": 30,
            },
            "searchbox": {
                "menuList": {"backgroundColor": "transparent"},
                "singleValue": {"color": "red", "some": "data"},
                "option": {
                    "color": "blue",
                    "backgroundColor": "yellow",
                    "highlightColor": "green",
                },
            },
        },
    )


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

with fragment_example:
    if st.__version__ < "1.37":
        st.write(f"streamlit >=1.37 needed for this example. version={st.__version__}")
        st.stop()

    if "app_runs" not in st.session_state:
        st.session_state.app_runs = 0
        st.session_state.fragment_runs = 0

    @st.fragment  # type: ignore - code not reached in older streamlit versions
    def _fragment():
        st.session_state.fragment_runs += 1
        st.button("Run Fragment")

        selected_value_fragment = st_searchbox(
            search_wikipedia_ids,
            key="wiki_searchbox_fragment",
            rerun_on_update=True,
            rerun_scope="fragment",
        )

        if selected_value_fragment:
            st.write(selected_value_fragment)

        st.write(f"Fragment says it ran {st.session_state.fragment_runs} times.")

    st.session_state.app_runs += 1

    _fragment()

    st.button("Rerun full app")

    selected_value_app = st_searchbox(
        search_wikipedia_ids,
        key="wiki_searchbox_full_app",
        rerun_on_update=True,
        rerun_scope="app",
    )

    if selected_value_app:
        st.write(selected_value_app)

    st.write(f"Full app says it ran {st.session_state.app_runs} times.")
    st.write(f"Full app sees that fragment ran {st.session_state.fragment_runs} times.")
