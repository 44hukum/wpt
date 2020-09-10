import pytest

from webdriver.error import NoSuchWindowException

from tests.perform_actions.support.refine import filter_dict, get_events
from tests.support.asserts import assert_move_to_coordinates


def test_null_response_value(session, wheel_chain):
    value = wheel_chain.scroll(0, 0, 0, 10).perform()
    assert value is None


def test_no_browsing_context(session, closed_window, wheel_chain):
    with pytest.raises(NoSuchWindowException):
        wheel_chain.scroll(0, 0, 0, 10).perform()


def test_wheel_scroll(session, test_actions_scroll_page, wheel_chain):
    session.execute_script("document.scrollingElement.scrollTop = 0")

    outer = session.find.css("#outer", all=False)
    wheel_chain.scroll(0, 0, 5, 10, origin=outer).perform()
    events = get_events(session)
    assert len(events) > 0
    event_types = [e["type"] for e in events]
    assert "wheel" in event_types
    for e in events:
        if e["type"] == "wheel":
            assert e["deltaX"] >= 5
            assert e["deltaY"] >= 10
            assert e["deltaZ"] == 0
            assert e["target"] == "outer"


# def test_wheel_scroll_overflow(session, test_actions_scroll_page, wheel_chain):
#     session.execute_script("document.scrollingElement.scrollTop = 0")

#     scrollable = session.find.css("#scrollable", all=False)
#     wheel_chain.scroll(0, 0, 5, 10, origin=scrollable).perform()
#     events = get_events(session)
#     assert len(events) > 0
#     event_types = [e["type"] for e in events]
#     assert "wheel" in event_types
#     for e in events:
#         if e["type"] == "wheel":
#             assert e["deltaX"] >= 5
#             assert e["deltaY"] >= 10
#             assert e["deltaZ"] == 0
#             assert e["target"] == "scrollContent"


# def test_wheel_scroll_iframe(session, test_actions_scroll_page, wheel_chain):
#     session.execute_script("document.scrollingElement.scrollTop = 0")

#     subframe = session.find.css("#subframe", all=False)
#     wheel_chain.scroll(0, 0, 5, 10, origin=subframe).perform()
#     events = get_events(session)
#     assert len(events) > 0
#     event_types = [e["type"] for e in events]
#     assert "wheel" in event_types
#     for e in events:
#         if e["type"] == "wheel":
#             assert e["deltaX"] >= 5
#             assert e["deltaY"] >= 10
#             assert e["deltaZ"] == 0
#             assert e["target"] == "iframeContent"
