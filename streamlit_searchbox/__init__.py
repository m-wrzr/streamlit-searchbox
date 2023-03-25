import os
from typing import Callable, List

import streamlit as st
import streamlit.components.v1 as components

# point to build directory
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")
_get_react_component = components.declare_component(
    "searchbox",
    path=build_dir,
)


def _process_search(
    search_function: Callable[[str], List[any]],
    key: str,
    searchterm: str,
    rerun: bool,
) -> bool:
    # nothing changed, avoid new search
    if searchterm == st.session_state[key]["search"]:
        return st.session_state[key]["result"]

    st.session_state[key]["search"] = searchterm
    search_results = search_function(searchterm)

    if not search_results:
        return st.session_state[key]["result"]

    def _get_label(label: any) -> str:
        return str(label[0]) if isinstance(label, tuple) else str(label)

    def _get_value(value: any) -> any:
        return value[1] if isinstance(value, tuple) else value

    # used for react component
    st.session_state[key]["options"] = [
        {
            "label": _get_label(v),
            "value": i,
        }
        for i, v in enumerate(search_results)
    ]

    # used for proper return types
    st.session_state[key]["options_real_type"] = [_get_value(v) for v in search_results]

    if rerun:
        st.experimental_rerun()


def st_searchbox(
    search_function: Callable[[str], List[any]],
    placeholder: str = "Search ...",
    label: str = None,
    default: any = None,
    clear_on_submit: bool = False,
    rerun: bool = True,
    key: str = "searchbox",
    **kwargs,
) -> any:
    """
    Create a new searchbox instance, that provides suggestions based on the user input
    and returns a selected option or empty string if nothing was selected

    Parameters
    ----------
    search_function: Callable[[str], List[str] | List[Tuple[str, any]]]
        Function that is called to fetch new suggestions after user input.
    default: Dict[str, any]
        Default value that is shown in the searchbox.
    key: str
        An key that uniquely identifies this component, used to store state.
    """

    # key without prefix used by react component
    key_react = f"{key}_react"

    if key not in st.session_state:
        st.session_state[key] = {
            # updated after each selection / reset
            "result": default,
            # updated after each search keystroke
            "search": "",
            # updated after each search_function run
            "options": [],
        }

    # everything here is passed to react as this.props.args
    react_state = _get_react_component(
        options=st.session_state[key]["options"],
        clear_on_submit=clear_on_submit,
        placeholder=placeholder,
        label=label,
        # react return state within streamlit session_state
        key=key_react,
        **kwargs,
    )

    if react_state is None:
        return st.session_state[key]["result"]

    interaction, value = react_state["interaction"], react_state["value"]

    if interaction == "search":
        return _process_search(search_function, key, value, rerun)

    if interaction == "submit":
        st.session_state[key]["result"] = (
            st.session_state[key]["options_real_type"][value]
            if "options_real_type" in st.session_state[key]
            else value
        )
        return st.session_state[key]["result"]

    if interaction == "reset":
        st.session_state[key]["result"] = default
        return default

    # no new react interaction happened
    return st.session_state[key]["result"]
