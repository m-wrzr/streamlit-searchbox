# streamlit-searchbox

- [streamlit-searchbox](#streamlit-searchbox)
  - [Installation](#installation)
  - [Overview](#overview)
  - [Parameters](#parameters)
    - [Required](#required)
    - [Visual](#visual)
    - [Defaults](#defaults)
    - [Reruns](#reruns)
    - [Transitions](#transitions)
    - [Custom Styles](#custom-styles)
  - [Example](#example)
  - [Styling](#styling)
  - [Contributions](#contributions)
    - [Contributors](#contributors)

---

A streamlit custom component providing a searchbox with autocomplete.

![Example](./assets/example.gif)


## Installation

```python
pip install streamlit-searchbox
```

## Overview

Create a searchbox component and pass a `search_function` that accepts a `str` searchterm. The searchbox is triggered on user input, calls the search function for new options and redraws the page via `st.experimental_rerun()`.

You can either pass a list of arguments, e.g.

```python
import streamlit as st
import wikipedia

from streamlit_searchbox import st_searchbox


def search_wikipedia(searchterm: str) -> list:
    # search wikipedia for the searchterm
    return wikipedia.search(searchterm) if searchterm else []


# pass search function and other options as needed
selected_value = st_searchbox(
    search_wikipedia,
    placeholder="Search Wikipedia... ",
    key="my_key",
)

st.write(f"Selected value: {selected_value}")
```

This example will call the Wikipedia Api to reload suggestions. The `selected_value` will be one of the items the `search_wikipedia` function returns, the suggestions shown in the UI components are a `str` representation. In case you want to provide custom text for suggestions, pass a `Tuple`.

```python
def search(searchterm: str, **kwargs) -> List[Tuple[str, any]]:
    ...
```

You can also pass additional keyword arguments to a `search` function in case you need more context by adding them to `st_searchbox(search, a=1, b=2)`.

## Parameters

To customize the searchbox you can pass the following arguments:


### Required

```python
search_function: Callable[[str], List[any]]
```

Function that will be called on user input

```python
key: str = "searchbox"
```

Streamlit key for unique component identification.

---

### Visual

```python
placeholder: str = "Search ..."
```

Placeholder for empty searches shown within the component.

```python
label: str | None = None
```

Label shown above the component.

```python
help: str | None = None
```

Shows a help icon with a popover. Only shown when the label is visible.

---

### Defaults


```python
default: any = None
```

Default return value in case nothing was submitted or the searchbox cleared.


```python
default_searchterm: str = ''
```

Default searchterm value when the searchbox is initialized.

```python
default_use_searchterm: bool = False
```

Use the current searchterm as a default return value.

```python
default_options: list[str] | None = None
```

Default options that will be shown when first clicking on the searchbox.

### Reruns

```python
rerun_on_update: bool = True
```

Use `st.experimental_rerun()` to reload the app after user input and load new search suggestions. Disabling leads to delay in showing the proper search results.

```python
rerun_scope: Literal["app", "fragment"] = "app",
```

If the rerun should affect the whole app or just the fragment.

```python
debounce: int = 150
```

Delay executing the callback from the react component by `x` milliseconds to avoid too many / redudant requests, i.e. during fast typing.

```python
min_execution_time: int = 0
```

`DEPRECATED` Delay execution after the search function finished to reach a minimum amount of `x` milliseconds. This can be used to avoid fast consecutive reruns, which can cause resets of the component in some streamlit versions `>=1.35` and `<1.39`.

---

### Transitions

```python
clear_on_submit: bool = False
```

Automatically clear the input after selection.

```python
edit_after_submit: Literal["disabled", "current", "option", "concat"] = "disabled"
```

Specify behavior for search query after an option is selected. By setting `edit_after_submit` to `option` you can use the searchbox similar to an autocomplete.

```python
reset_function: Callable[[], None] | None = None
```

Function that will be called when the combobox is reset.

```python
submit_function: Callable[[Any], None] | None = None
```

Function that will be called when a new option is selected, with the selected option as argument.

---

### Custom Styles

```python
style_overrides: dict | None = None
```

See [section](#styling) below for more details.

```python
style_absolute: bool = False
```

Will position the searchbox as an absolute element. *NOTE:* this will affect all searchbox instances and should either be set for all boxes or none. See [#46](https://github.com/m-wrzr/streamlit-searchbox/issues/46) for inital workaround by [@JoshElgar](https://github.com/JoshElgar).

## Example

An example Streamlit app can be found [here](./example.py)

## Styling

To further customize the styling of the searchbox, you can override the default styling by passing `style_overrides` which will be directly applied in the react components. See below for an example, for more information on the available attributes, please see [styling.tsx](./streamlit_searchbox/frontend/src/styling.tsx) as well as the [react-select](https://react-select.com/styles) documentation.

```javascript
{
   // change the clear icon
   "clear":{
      "width":20,
      "height":20,
      // also available: circle-unfilled, circle-filled
      "icon":"cross",
      // also available: never, after-submit
      "clearable":"always"
   },
   // change the dropdown icon
   "dropdown":{
      "rotate":true,
      "width":30,
      "height":30,
      "fill":"red"
   },
   // styling for the searchbox itself, mostly passed to react-select
   "searchbox":{
      "menuList":{
         "backgroundColor":"transparent"
      },
      "singleValue":{
         "color":"red"
      },
      "option":{
         "color":"blue",
         "backgroundColor":"yellow",
         // highlight matching text
         "highlightColor":"green"
      }
   }
}
```

## Contributions

We welcome contributions from everyone. Here are a few ways you can help:

- **Reporting bugs**: If you find a bug, please report it by opening an issue.
- **Suggesting enhancements**: If you have ideas on how to improve the project, please share them by opening an issue.
- **Pull requests**: If you want to contribute directly to the code base, please make a pull request. Here's how you can do so:
  1. Fork the repository.
  2. Create a new branch (`git checkout -b feature-branch`).
  3. Make your changes.
  4. Commit your changes (`git commit -am 'Add some feature'`).
  5. Push to the branch (`git push origin feature-branch`).
  6. Create a new Pull Request.

### Contributors

- [@JoshElgar](https://github.com/JoshElgar) absolute positioning workaround
- [@dopc](https://github.com/dopc) bugfix for [#15](https://github.com/m-wrzr/streamlit-searchbox/issues/15)
- [@Jumitti](https://github.com/Jumitti) `st.rerun` compatibility
- [@salmanrazzaq-94](https://github.com/salmanrazzaq-94) `st.fragment` support
- [@hoggatt](https://github.com/hoggatt) `reset_function`
- [@bram49](https://github.com/bram49) `submit_function`
- [@ytausch](https://github.com/ytausch) remove `tests` folder from distributions
- [@hansthen](https://github.com/hansthen) `help` tooltip
