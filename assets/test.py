from typing import List

import streamlit as st
import wikipedia

from streamlit_searchbox import st_searchbox


def search_wikipedia(searchterm: str) -> List[str]:
    return wikipedia.search(searchterm) if searchterm else []


selected_value = st_searchbox(search_wikipedia, key="wiki_searchbox")

if selected_value:
    st.markdown("You've selected: %s" % selected_value)
