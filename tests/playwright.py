from __future__ import annotations

import re
import subprocess
import time
from typing import Literal

import pytest
import requests
from playwright.sync_api import Frame, Page, expect

from tests.utils import boxes, selection_to_text

_SCREENSHOT_COUNTER: dict[str, int] = {}


def screenshot(page: Page, caller_name: str, suffix: str | None = None) -> None:
    """
    screenshot fixture that keepts track of the number of screenshots taken
    """

    _SCREENSHOT_COUNTER[caller_name] = _SCREENSHOT_COUNTER.get(caller_name, 0)

    folder = "tests/screenshots"
    suffix = "" if suffix is None else f"-{suffix}"

    name = f"{caller_name}-{_SCREENSHOT_COUNTER[caller_name]}{suffix}"

    page.screenshot(
        path=f"{folder}/{name}.png",
        full_page=True,
    )

    _SCREENSHOT_COUNTER[caller_name] += 1


def wait_for_reload(page: Page) -> None:
    """
    wait until loading spinner is gone
    """
    page.wait_for_selector(
        "[data-testid='stStatusWidget']",
        timeout=5000,
        state="detached",
    )


@pytest.fixture(scope="session", autouse=True)
def streamlit_app():
    def is_server_running():
        try:
            return (
                requests.get("http://localhost:8501/_stcore/health", timeout=1).text
                == "ok"
            )
        except Exception as _:
            return False

    assert not is_server_running(), "Streamlit app is already running"

    # Start the Streamlit app in the background
    process = subprocess.Popen(
        [
            "streamlit",
            "run",
            "example_ci.py",
            "--server.fileWatcherType=none",
            "--logger.level=error",
        ]
    )

    start_time = time.time()

    while not is_server_running():
        time.sleep(1)

        if time.time() - start_time > 30:
            assert False, "Streamlit app failed to start within 60 seconds"

    yield process

    process.terminate()

    # Check the return code; if it's 0, the app loaded without errors
    assert process.returncode in [
        0,
        None,
    ], f"Streamlit app exited with code {process.returncode}"


@pytest.fixture(scope="function", autouse=True)
def reload(streamlit_app, page: Page):
    page.goto("localhost:8501")


def test_streamlit_app_loads(streamlit_app):
    # test fixture loads the app in the background
    pass


StatusType = Literal["skip", "full", "partial"]


def get_status(label: str) -> StatusType:
    if label in [
        "search",
        "search_enum_return",
    ]:
        return "full"

    if label in [
        # TODO: locator with x not working here
        "search_default_options",
        "search_default_options_tuple",
        "search_empty_list",
    ]:
        return "partial"

    if label in [
        # unreliable due to external calls
        "search_wikipedia_ids",
        # unreliable due to random delays
        "search_rnd_delay",
    ]:
        return "skip"

    raise NotImplementedError(f"status for {label} not implemented")


# iterate over all searchboxes in separate streamlit app
@pytest.mark.parametrize(
    "search_function,label,i, status",
    [
        (b["search_function"], b["label"], i, get_status(b["label"]))
        # for b in boxes
        for i, b in enumerate(boxes)
    ],
)
def test_e2e(search_function, label: str, i: int, status: StatusType, page: Page):
    if status == "skip":
        pytest.skip(f"skipping {label} - not supported")

    ###### 1. go to the Streamlit app and check for the header ######

    page.goto("localhost:8501")

    expect(page).to_have_title(re.compile("Searchbox Demo"))

    wait_for_reload(page)

    screenshot(page, label)

    ###### 2. find the correct iframe and searchbox ######

    # find frame with searchbox, otherwise content isn't available
    frame: Frame = [
        frame for frame in page.frames if "streamlit_searchbox" in frame.url
    ][i]

    loc_label = frame.locator(f"div:has-text('{label}')")
    loc_searchbox = frame.locator("input[type='text']")

    if loc_label.count() == 0 or loc_searchbox.count() == 0:
        assert False, f"searchbox not found: {label}"

    # can't search for some search_functions, so skip
    if status == "partial":
        return

    ###### 3. search for term x and select first option ######

    search_term = "x"
    search_result = search_function(search_term)[0]

    loc_searchbox.focus()
    loc_searchbox.fill(search_term)

    screenshot(page, label)
    loc_searchbox.press("Enter")

    # wait for options to appear
    wait_for_reload(page)
    time.sleep(0.5)

    screenshot(page, label)

    ###### 4. check if the option is displayed ######

    if not isinstance(search_result, tuple):
        search_text = str(search_result)
    else:
        search_text = str(search_result[0])

    l_option = frame.wait_for_selector(f"text={search_text}", state="attached")

    assert l_option is not None

    l_option.focus()
    l_option.press("Enter")

    wait_for_reload(page)

    screenshot(page, label)

    ###### 5. check if the result is displayed in main page ######

    text_displayed = selection_to_text(
        search_result if not isinstance(search_result, tuple) else search_result[1]
    )

    # results are be displayed in main page, since it's not part of the searchbox iframe
    assert page.get_by_text(text_displayed).count() == 1
