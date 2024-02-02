from __future__ import annotations

import inspect
import re
import subprocess
import time

import pytest
import requests
from playwright.sync_api import Page, expect

from tests.utils import boxes, selection_to_text


@pytest.fixture
def screenshot():
    """
    screenshot fixture that keepts track of the number of screenshots taken
    """

    i = 0

    # TODO: tests only pass when screenshots are enabled, why?
    def _screenshot(page: Page, path: str | None = None):
        nonlocal i

        caller_name = inspect.stack()[1][3]
        page.screenshot(
            path=f"tests/screenshots/{caller_name}_{path}_{i}.png",
            full_page=True,
        )
        i += 1

    yield _screenshot


def wait_for_reload(page: Page) -> None:
    """
    wait until loading spinner is gone
    """
    page.wait_for_selector(
        "[data-testid='stStatusWidget']",
        timeout=5000,
        state="detached",
    )


@pytest.fixture
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


def test_streamlit_app_loads(streamlit_app):
    # test fixture loads the app in the background
    pass


# iterate over all searchboxes in separate streamlit app
@pytest.mark.parametrize(
    "search_function,label",
    [
        (b["search_function"], b["label"])
        for b in boxes
        if b["label"]
        not in [
            # ignore since it relies on external api calls
            "search_wikipedia_ids",
            # ignore since it's has a different behavior
            "search_rerun_disabled",
            # TODO: make custom tests for these, initial result list makes it harder
            "search_default_options",
            "search_default_options_tuple",
        ]
    ],
)
def test_e2e(streamlit_app, search_function, label, screenshot, page: Page):
    page.goto("localhost:8501")

    expect(page).to_have_title(re.compile("Searchbox Demo"))

    wait_for_reload(page)

    screenshot(page, label)

    print(f"search_function={search_function.__name__}, search_label={label}")

    # find frame with searchbox, otherwise content isn't available
    searchbox_frames = [
        frame for frame in page.frames if "streamlit_searchbox" in frame.url
    ]

    for frame in searchbox_frames:
        l_searchbox = frame.locator(f"#{label}")

        # skip if in the wrong iframe
        if l_searchbox.count() == 0:
            continue

        search_term = "x"

        search_result = search_function(search_term)[0]

        l_searchbox.fill(search_term)
        l_searchbox.press("Enter")

        wait_for_reload(page)
        screenshot(page, label)

        l_option = frame.get_by_text(
            str(
                search_result
                if not isinstance(search_result, tuple)
                else search_result[0]
            )
        ).first
        l_option.focus()
        l_option.press("Enter")

        screenshot(page, label)

        wait_for_reload(page)

        screenshot(page, label)

        # loads result as streamlit fragment, so get from page instead of iframe
        assert (
            page.get_by_text(
                selection_to_text(
                    search_result
                    if not isinstance(search_result, tuple)
                    else search_result[1]
                )
            ).count()
            == 1
        )

        screenshot(page, label)

        break
