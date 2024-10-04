# Changelog

All notable changes to this project will be documented in this file.

## [0.1.17] - 2024-09-15

- `clear_on_submit` now also resets the `default_options`
- added `clearable` style option to determine when the clear icon is shown
- enforce kwargs usage due to the large number of parameters

## [0.1.16] - 2024-09-01

- added `reset_function` that is called when a user resets the searchbox
- clear icons now have hover effects

## [0.1.15] - 2024-08-26

- support for `@fragment` scoped reruns
- added option to `debounce` react callbacks
- added option to set a `min_execution_time` to avoid reset issues with reruns

## [0.1.14] - 2024-07-27

- add wrapper styles that can be used to add margins to the searchbox

## [0.1.13] - 2024-07-03

- added option `default_use_searchterm` that changes the default return value to the current search
- added option for absolute positioning

## [0.1.12] - 2024-05-13

- fixes type hinting issue

## [0.1.11] - 2024-05-12

- added `style_overrides` options to customize the searchbox appearance

## [0.1.10] - 2024-04-15

- fixes an issue with the use of `kwargs`

## [0.1.9] - 2024-04-14

- added the option to pass `kwargs` to searchbox that will be forwarded to the search function


## [0.1.8] - 2024-03-17

- added different options to `edit_after_submit` and not reset the searchterm

## [0.1.7] - 2024-03-17

- fixes an issue with the searchbox loosing focus
- fixes an issue with state resets after submitting

## [0.1.6] - 2023-10-28

- update imports for `rerun` and `experimental_rerun`

## [0.1.5] - 2023-09-26

- extend support for different python versions

## [0.1.4] - 2023-09-17

- added `default_options` that are shown on first use
- added option to disable reruns on update

## [0.1.3] - 2023-04-15

- fix issue with empty search results

## [0.1.2] - 2023-03-26

- fix keyerror where session state is missing in case of reruns
- added `streamlit_searchbox` logger

## [0.1.1] - 2023-03-25

- remove `match` statements for version compatibility

## [0.1.0] - 2023-03-07

- added display options for `placeholders` and `labels`
- added option to `clear_on_submit` to reset the searchterm after selection
- added `default` return before first selection
