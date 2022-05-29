import os
from typing import Callable, List

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
    search_function: Callable[[str], List[str]],
    key: str = "searchbox",
) -> str:
    """
    Create a new searchbox instance, that provides suggestions based on the user input
    and returns a selected option or empty string if nothing was selected

    Parameters
    ----------
    search_function: Callable[[str], List[str]]
        Function that is called to fetch new suggestions after user input.
    key: str
        An key that uniquely identifies this component, used to store state.
    """

    # define unique key for searchbox state
    search_state = f"{key}_search"

    if search_state not in st.session_state:
        st.session_state[search_state] = ""

    # draw react component with search_function options
    react_state = _get_react_component(
        options=[
            {"label": result, "value": result}
            for result in search_function(st.session_state[search_state])
        ],
        key=key,
    )

    if react_state:
        if react_state["option"]:
            return react_state["option"]

        # in case the searchbox has new characters, redraw the whole component and call the options function
        # almost always true, as the functions gets triggered after a react state change, i.e. user input
        if st.session_state[search_state] != react_state["search"]:
            st.session_state[search_state] = react_state["search"]
            st.experimental_rerun()

    return ""


# for development: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st
    import wikipedia

    # define for local testing
    _get_react_component = components.declare_component(
        "searchbox",
        url="http://localhost:3001",
    )

    def search_wikipedia(searchterm: str) -> List[str]:
        return wikipedia.search(searchterm) if searchterm else []

    selected_value = st_searchbox(search_wikipedia, key="wiki_searchbox")

    if selected_value:
        st.markdown("You've selected: %s" % selected_value)
