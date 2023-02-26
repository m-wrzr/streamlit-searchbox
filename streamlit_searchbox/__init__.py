import os

from typing import Callable, List, Dict

import streamlit as st
import streamlit.components.v1 as components

# point to build directory
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")
_get_react_component = components.declare_component(
    "searchbox",
    path=build_dir,
)


def st_searchbox(
    search_function: Callable[[str], List[any]],
    placeholder: str = "Search ...",
    default: any = None,
    clearable: bool = True,
    clear_on_submit: bool = False,
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
        clearable=clearable,
        clear_on_submit=clear_on_submit,
        placeholder=placeholder,
        # react return state within streamlit session_state
        key=key_react,
        **kwargs,
    )

    if react_state is None:
        return st.session_state[key]["result"]

    interaction, value = react_state["interaction"], react_state["value"]

    match interaction:
        case "search":

            # nothing changed
            if value == st.session_state[key]["search"]:
                return st.session_state[key]["result"]

            # TODO: doesn't work with non-react compatible types
            # new search, update from search_function
            st.session_state[key]["search"] = value
            st.session_state[key]["options"] = [
                {
                    "label": v if isinstance(v, str) else v[0],
                    "value": v if isinstance(v, str) else v[1],
                }
                for v in search_function(value)
            ]

            st.experimental_rerun()

        # common return cases
        case "submit":
            st.session_state[key]["result"] = value
            return value
        case "reset":
            st.session_state[key]["result"] = default
            return default
        # no new react interaction happened
        case _:
            return st.session_state[key]["result"]
