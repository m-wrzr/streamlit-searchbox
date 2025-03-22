"""
module for streamlit searchbox component
"""

from __future__ import annotations

import datetime
import logging
import os
import time
import warnings
from typing import Any, Callable, List, Literal, TypedDict

import streamlit as st
import streamlit.components.v1 as components

try:
    from streamlit import rerun  # type: ignore
except ImportError:
    # conditional import for streamlit version <1.27
    from streamlit import experimental_rerun as rerun  # type: ignore


# default milliseconds for the search function to run, this is used to avoid
# fast consecutive reruns. possibly remove this in later versions
# see: https://github.com/streamlit/streamlit/issues/9002
# NOTE: DEPRECATED, remove in future versions
MIN_EXECUTION_TIME_DEFAULT = (
    250 if st.__version__ >= "1.35" and st.__version__ < "1.39" else 0
)

# point to build directory
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")
_get_react_component = components.declare_component(
    "searchbox",
    path=build_dir,
)

logger = logging.getLogger(__name__)


def _rerun(rerun_scope: Literal["app", "fragment"]) -> None:
    # only pass scope if the version is >= 1.37
    if st.__version__ >= "1.37":
        rerun(scope=rerun_scope)  # type: ignore
    else:
        rerun()


def _list_to_options_py(options: list[Any] | list[tuple[str, Any]]) -> list[Any]:
    """
    unpack search options for proper python return types
    """
    return [v[1] if isinstance(v, tuple) else v for v in options]


def _list_to_options_js(
    options: list[Any] | list[tuple[str, Any]],
) -> list[dict[str, Any]]:
    """
    unpack search options for use in react component
    """
    return [
        {
            "label": str(v[0]) if isinstance(v, tuple) else str(v),
            "value": i,
        }
        for i, v in enumerate(options)
    ]


def _process_search(
    search_function: Callable[[str], List[Any]],
    key: str,
    searchterm: str,
    rerun_on_update: bool,
    rerun_scope: Literal["app", "fragment"] = "app",
    min_execution_time: int = 0,
    **kwargs,
) -> None:
    # nothing changed, avoid new search
    if searchterm == st.session_state[key]["search"]:
        return

    st.session_state[key]["search"] = searchterm

    ts_start = datetime.datetime.now()

    search_results = search_function(searchterm, **kwargs)

    if search_results is None:
        search_results = []

    st.session_state[key]["options_js"] = _list_to_options_js(search_results)
    st.session_state[key]["options_py"] = _list_to_options_py(search_results)

    if rerun_on_update:
        ts_stop = datetime.datetime.now()
        execution_time_ms = (ts_stop - ts_start).total_seconds() * 1000

        # wait until minimal execution time is reached
        if execution_time_ms < min_execution_time:
            time.sleep((min_execution_time - execution_time_ms) / 1000)

        _rerun(rerun_scope)


def _set_defaults(
    key: str,
    default: Any,
    default_searchterm: str = "",
    default_options: List[Any] | None = None,
) -> None:
    st.session_state[key] = {
        # updated after each selection / reset
        "result": default,
        # updated after each search keystroke
        "search": default_searchterm,
        # updated after each search_function run
        "options_js": [],
        # key that is used by react component, use time suffix to reload after clear
        "key_react": f"{key}_react_{str(time.time())}",
    }

    if default_options:
        st.session_state[key]["options_js"] = _list_to_options_js(default_options)
        st.session_state[key]["options_py"] = _list_to_options_py(default_options)


ClearStyle = TypedDict(
    "ClearStyle",
    {
        # determines which icon is used for the clear button
        "icon": Literal["circle-unfilled", "circle-filled", "cross"],
        # determines when the clear button is shown
        "clearable": Literal["always", "never", "after-submit"],
        # further css styles for the clear button
        "width": int,
        "height": int,
        "fill": str,
        "stroke": str,
        "stroke-width": int,
    },
    total=False,
)

DropdownStyle = TypedDict(
    "DropdownStyle",
    {
        # weither to flip the dropdown if the menu is open
        "rotate": bool,
        # further css styles for the dropdown
        "width": int,
        "height": int,
        "fill": str,
    },
    total=False,
)

OptionStyle = TypedDict(
    "OptionStyle",
    {
        "color": str,
        "backgroundColor": str,
        "highlightColor": str,
    },
    total=False,
)


class SearchboxStyle(TypedDict, total=False):
    menuList: dict | None
    singleValue: dict | None
    input: dict | None
    placeholder: dict | None
    control: dict | None
    option: OptionStyle | None


class StyleOverrides(TypedDict, total=False):
    wrapper: dict | None
    clear: ClearStyle | None
    dropdown: DropdownStyle | None
    searchbox: SearchboxStyle | None


def st_searchbox(
    search_function: Callable[[str], List[Any]],
    placeholder: str = "Search ...",
    label: str | None = None,
    default: Any = None,
    *,
    default_searchterm: str = "",
    default_use_searchterm: bool = False,
    default_options: List[Any] | None = None,
    clear_on_submit: bool = False,
    rerun_on_update: bool = True,
    edit_after_submit: Literal["disabled", "current", "option", "concat"] = "disabled",
    style_absolute: bool = False,
    style_overrides: StyleOverrides | None = None,
    debounce: int = 150,
    min_execution_time: int = MIN_EXECUTION_TIME_DEFAULT,
    reset_function: Callable[[], None] | None = None,
    submit_function: Callable[[Any], None] | None = None,
    key: str = "searchbox",
    rerun_scope: Literal["app", "fragment"] = "app",
    help: str | None = None,
    **kwargs,
) -> Any:
    """
    Create a new searchbox instance, that provides suggestions based on the user input
    and returns a selected option or empty string if nothing was selected

    Args:
        search_function (Callable[[str], List[any]]):
            Function that is called to fetch new suggestions after user input.
        placeholder (str, optional):
            Label shown in the searchbox. Defaults to "Search ...".
        label (str, optional):
            Label shown above the searchbox. Defaults to None.
        default (any, optional):
            Return value if nothing is selected so far. Defaults to None.
        default_searchterm (str, optional):
            Inital searchterm when the searchbox is created. Defaults to "".
        default_use_searchterm (bool, optional):
            Return the current searchterm if nothing was selected. Defaults to False.
        default_options (List[any], optional):
            Initial list of options. Defaults to None.
        clear_on_submit (bool, optional):
            Remove suggestions on select and reset default_options. Defaults to False.
        rerun_on_update (bool, optional):
            Rerun the streamlit app after each search. Defaults to True.
        edit_after_submit ("disabled", "current", "option", "concat", optional):
            Edit the search term after submit. Defaults to "disabled".
        style_absolute (bool, optional):
            Position the searchbox absolute on the page. This will affect all other
            searchboxes and should be passed to every element. Defaults to False.
        style_overrides (StyleOverrides, optional):
            CSS styling passed directly to the react components. Defaults to None.
        rerun_scope ("app", "fragment", optional):
            The scope in which to rerun the Streamlit app. Only applicable if Streamlit
            version >= 1.37. Defaults to "app".
        debounce (int, optional):
            Time in milliseconds to wait before sending the input to the search function
            to avoid too many requests, i.e. during fast keystrokes. Defaults to 150.
        min_execution_time (int, optional):
            Deprecated: Minimal execution time for the search function in milliseconds.
            This is used to avoid fast consecutive reruns, where fast reruns can lead to
            resets within the component in some streamlit versions.
            Defaults to 0 or 250 depending on the streamlit version.
        reset_function (Callable[[], None], optional):
            Function that is called after the user reset the combobox. Defaults to None.
        submit_function (Callable[[any], None], optional):
            Function that is called after the user submits a new/unique option from the
            combobox. Defaults to None.
        help (str, optional):
            Show a help tooltip, only visible if a label is provided. Defaults to None.
        key (str, optional):
            Streamlit session key. Defaults to "searchbox".

    Returns:
        any: based on user selection
    """

    if min_execution_time > 0 and min_execution_time != MIN_EXECUTION_TIME_DEFAULT:
        warnings.warn(
            "min_execution_time is deprecated and will be removed in the future.",
            category=DeprecationWarning,
            stacklevel=2,
        )

    if key not in st.session_state:
        _set_defaults(
            key,
            default,
            default_searchterm,
            default_options,
        )

    # everything here is passed to react as this.props.args
    react_state = _get_react_component(
        options=st.session_state[key]["options_js"],
        clear_on_submit=clear_on_submit,
        placeholder=placeholder,
        label=label,
        edit_after_submit=edit_after_submit,
        style_overrides=style_overrides,
        debounce=debounce,
        default_searchterm=default_searchterm,
        # react return state within streamlit session_state
        help=help,
        key=st.session_state[key]["key_react"],
    )

    if style_absolute:
        # add empty markdown blocks to reserve space for the iframe
        st.markdown("")
        st.markdown("")

        css = """
        iframe[title="streamlit_searchbox.searchbox"] {
            position: absolute;
            z-index: 10;
        }
        """
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    if react_state is None:
        return st.session_state[key]["result"]

    interaction, value = react_state["interaction"], react_state["value"]

    if interaction == "search":
        if default_use_searchterm:
            st.session_state[key]["result"] = value

        # triggers rerun, no ops afterwards executed
        _process_search(
            search_function,
            key,
            value,
            rerun_on_update,
            rerun_scope=rerun_scope,
            min_execution_time=min_execution_time,
            **kwargs,
        )

    if interaction == "submit":
        submit_value = (
            st.session_state[key]["options_py"][value]
            if "options_py" in st.session_state[key]
            else value
        )

        # ensure submit_function only runs when value changed
        if st.session_state[key]["result"] != submit_value:
            st.session_state[key]["result"] = submit_value
            if submit_function is not None:
                submit_function(submit_value)

        if clear_on_submit:
            _set_defaults(
                key,
                st.session_state[key]["result"],
                default_searchterm,
                default_options,
            )
            _rerun(rerun_scope)

        return st.session_state[key]["result"]

    if interaction == "reset":
        _set_defaults(
            key,
            default,
            default_searchterm,
            default_options,
        )

        if reset_function is not None:
            reset_function()

        if rerun_on_update:
            _rerun(rerun_scope)

        return default

    # no new react interaction happened
    return st.session_state[key]["result"]
