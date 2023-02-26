from typing import List, Tuple

import requests
import streamlit as st

from streamlit_searchbox import st_searchbox


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


c1, c2, c3 = st.columns(3)


selected_value = st_searchbox(
    search_wikipedia_ids,
    placeholder="Search Wikipedia",
    default=5,
    clear_on_submit=False,
    clearable=True,
    key="wiki_searchbox_1",
)
st.markdown(f"You've selected: {selected_value}")
st.markdown("---")

selected_value2 = st_searchbox(
    search_wikipedia_ids,
    default=None,
    clear_on_submit=True,
    key="wiki_searchbox_2",
)
st.markdown(f"You've selected: {selected_value2}")
st.markdown("---")


selected_value3 = st_searchbox(
    search_wikipedia_ids,
    default=None,
    clear_on_submit=False,
    clearable=True,
    key="wiki_searchbox_3",
)
st.markdown(f"You've selected: {selected_value3}")
