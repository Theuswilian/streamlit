# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from playwright.sync_api import Page, expect

from e2e_playwright.conftest import ImageCompareFunction, wait_for_app_run
from e2e_playwright.shared.app_utils import expect_help_tooltip


def test_slider_rendering(themed_app: Page, assert_snapshot: ImageCompareFunction):
    st_sliders = themed_app.get_by_test_id("stSlider")
    expect(st_sliders).to_have_count(14)
    expect_help_tooltip(themed_app, st_sliders.nth(4), "This is some help tooltip!")

    assert_snapshot(st_sliders.nth(4), name="st_slider-regular_with_format")
    assert_snapshot(st_sliders.nth(7), name="st_slider-disabled")
    assert_snapshot(st_sliders.nth(8), name="st_slider-hidden_label")
    assert_snapshot(st_sliders.nth(9), name="st_slider-label_collapsed")
    assert_snapshot(st_sliders.nth(10), name="st_slider-labels_overlap_slider")


def test_slider_contains_correct_format_func_value_and_in_session_state(
    app: Page,
):
    expect(
        app.get_by_text(
            "Value 1: (datetime.date(2019, 8, 1), datetime.date(2019, 9, 1))"
        )
    ).to_have_count(1)
    first_slider = app.get_by_test_id("stSlider").nth(4)
    first_slider.hover()
    # click in middle
    app.mouse.down()

    # Move mouse to 2000, 200 pixels on the screen to simulate dragging right
    app.mouse.move(2000, 200)
    app.mouse.up()
    wait_for_app_run(app)

    expect(
        app.get_by_text(
            "Value 1: (datetime.date(2019, 8, 1), datetime.date(2021, 6, 4))"
        )
    ).to_have_count(1)


def test_using_arrow_keys_on_slider_produces_correct_values(app: Page):
    expect(
        app.get_by_text(
            "Value 1: (datetime.date(2019, 8, 1), datetime.date(2019, 9, 1))"
        )
    ).to_have_count(1)
    first_slider = app.get_by_test_id("stSlider").nth(4)
    first_slider.hover()
    # click in middle
    app.mouse.down()

    # Move slider once to right
    app.keyboard.press("ArrowRight")
    wait_for_app_run(app)
    expect(
        app.get_by_text(
            "Value 1: (datetime.date(2019, 8, 1), datetime.date(2020, 7, 3))"
        )
    ).to_have_count(1)

    # Move slider once to left
    app.keyboard.press("ArrowLeft")
    wait_for_app_run(app)

    expect(
        app.get_by_text(
            "Value 1: (datetime.date(2019, 8, 1), datetime.date(2020, 7, 2))"
        )
    ).to_have_count(1)


def test_slider_calls_callback(app: Page):
    expect(app.get_by_text("Value 8: 25")).to_be_visible()
    expect(app.get_by_text("Slider changed: False")).to_be_visible()
    slider = app.get_by_test_id("stSlider").nth(11)
    slider.hover()
    # click in middle
    app.mouse.down()

    wait_for_app_run(app)
    expect(app.get_by_text("Value 8: 50")).to_be_visible()
    expect(app.get_by_text("Slider changed: True")).to_be_visible()


def test_slider_works_in_forms(app: Page):
    expect(app.get_by_text("slider-in-form selection: 25")).to_be_visible()
    slider = app.get_by_test_id("stSlider").nth(12)
    slider.hover()
    # click in middle
    app.mouse.down()

    # The value is not submitted so the value should not have changed yet
    expect(app.get_by_text("slider-in-form selection: 25")).to_be_visible()

    # need to wait for the actual component value to update and then submit
    app.wait_for_timeout(200)
    app.get_by_test_id("baseButton-secondaryFormSubmit").click()
    wait_for_app_run(app)

    expect(app.get_by_text("slider-in-form selection: 50")).to_be_visible()


def test_slider_works_with_fragments(app: Page):
    expect(app.get_by_text("Runs: 1")).to_be_visible()
    expect(app.get_by_text("slider-in-fragment selection: 25")).to_be_visible()
    slider = app.get_by_test_id("stSlider").nth(13)
    slider.hover()
    # click in middle
    app.mouse.down()

    wait_for_app_run(app)
    expect(app.get_by_text("slider-in-fragment selection: 50")).to_be_visible()
    expect(app.get_by_text("Runs: 1")).to_be_visible()
