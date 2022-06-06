import os
from typing import Callable, List, Tuple

import streamlit as st
import streamlit.components.v1 as components

# update for local testing
_RELEASE = True

if _RELEASE:
    # point to build directory and
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _get_react_component = components.declare_component(
        "searchbox",
        path=build_dir,
    )


def st_searchbox(
    search_function: Callable[[str], List[any]],
    key: str = "searchbox",
) -> any:
    """
    Create a new searchbox instance, that provides suggestions based on the user input
    and returns a selected option or empty string if nothing was selected

    Parameters
    ----------
    search_function: Callable[[str], List[str] | List[Tuple[str, any]]]
        Function that is called to fetch new suggestions after user input.
    key: str
        An key that uniquely identifies this component, used to store state.
    """
    SEARCH, OPTIONS = "search", "options"

    if SEARCH not in st.session_state:
        st.session_state[SEARCH] = ""
        st.session_state[OPTIONS] = []

    # draw react component with search_function options
    # in case of keyboard updates, react triggers st_searchbox and we get a new state here
    react_state = _get_react_component(
        options=st.session_state[OPTIONS],
        key=key,
    )

    if react_state:
        # option was selected from react, return it
        # check specifically for None, 0 might also be valid option selection
        if react_state.get("option", None) != None:
            del st.session_state[SEARCH]
            del st.session_state[OPTIONS]

            return react_state["option"]

        # in case the searchbox has new characters, redraw the whole component and call the options function
        # almost always true, as the functions gets triggered after a react state change, i.e. user input
        if st.session_state[SEARCH] != react_state[SEARCH]:
            st.session_state[SEARCH] = react_state[SEARCH]

            # if only string, assume this is the desired return value
            # make sure that labels are strings
            to_react = lambda v: {
                "label": v if type(v) == str else v[0],
                "value": v if type(v) == str else v[1],
            }

            # set new options, will be passed to react in re-run
            st.session_state[OPTIONS] = [
                to_react(v) for v in search_function(react_state[SEARCH])
            ]

            st.experimental_rerun()

    return None


# for development: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import requests
    import streamlit as st
    import wikipedia

    # define for local testing
    _get_react_component = components.declare_component(
        "searchbox",
        url="http://localhost:3001",
    )

    # function with single string list
    def search_wikipedia(searchterm: str) -> List[str]:
        return wikipedia.search(searchterm) if searchterm else []

    # function with key:value dictionary
    def search_wikipedia_ids(searchterm: str) -> List[Tuple[str, any]]:

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
        ).json()["query"]["search"]

        # first element will be shown in search, second is returned from component
        return [(str(article["title"]), article["pageid"]) for article in response]

    selected_value = st_searchbox(search_wikipedia_ids, key="wiki_searchbox")

    st.markdown("You've selected: %s" % selected_value)
