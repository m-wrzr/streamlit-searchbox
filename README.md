# streamlit-searchbox

A streamlit custom component for a autocomplete searchbox

![Example](./assets/example.gif)

## Installation

```python
pip install streamlit-searchbox
```

## Example Usage

```python
from typing import List

import wikipedia

import streamlit as st
from streamlit_searchbox import st_searchbox


# function with list of labels
def search_wikipedia(searchterm) -> List[str]:
    return wikipedia.search(searchterm) if searchterm else []


# pass search function to searchbox
selected_value = st_searchbox(
    search_wikipedia,
    key="wiki_searchbox",
)
st.markdown("You've selected: %s" % selected_value)
```

If you want the searchbox to return a value assicoated with the label, e.g. some id refer to the example below.

```python
from typing import List, Tuple

import requests

import streamlit as st
from streamlit_searchbox import st_searchbox




# function with list of tuples (label:str, value:any)
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
    return [
        (
            str(article["title"]),
            article["pageid"],
        )
        for article in response
    ]


# pass search function to searchbox
selected_value = st_searchbox(
    search_wikipedia_ids,
    key="wiki_searchbox",
)
st.markdown("You've selected: %s" % selected_value)
```
