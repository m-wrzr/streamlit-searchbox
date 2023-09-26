import logging

import streamlit as st

from streamlit_searchbox import st_searchbox
from tests.utils import boxes, selection_to_text

logging.getLogger("streamlit_searchbox").setLevel(logging.DEBUG)

st.set_page_config(layout="centered", page_title="Searchbox Demo")


# iterate over boxes in groups of 3, fit into columns
for box_l in [boxes[i : i + 2] for i in range(0, len(boxes), 2)]:
    cols = st.columns(2)

    for i, box in enumerate(box_l):
        with cols[i]:
            selected_value = st_searchbox(**box)

            if selected_value:
                st.info(selection_to_text(selected_value))

    st.markdown("---")
