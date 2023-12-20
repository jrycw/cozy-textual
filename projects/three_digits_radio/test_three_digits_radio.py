import pytest
from textual.widgets import Input
from three_digits_radio import RadioSelect, RadioSet, ThreeDigitsRadioApp


@pytest.mark.asyncio
async def test_initial_input():
    async with ThreeDigitsRadioApp().run_test() as pilot:
        await pilot.click(Input)
        assert pilot.app.query_one(Input).value == "000"


@pytest.mark.asyncio
async def test_input_changed():
    async with ThreeDigitsRadioApp().run_test() as pilot:
        test_value = "234"
        pilot.app.query_one(Input).value = test_value
        await pilot.click(Input)
        assert pilot.app.query_one(Input).value == test_value
        for rs, digit in zip(pilot.app.query(RadioSelect), test_value):
            assert rs.value == int(digit)


@pytest.mark.asyncio
async def test_input_changed_too_large():
    async with ThreeDigitsRadioApp().run_test() as pilot:
        test_value = "1234"
        pilot.app.query_one(Input).value = test_value
        await pilot.click(Input)
        assert pilot.app.query_one(Input).value == test_value
        for rs in pilot.app.query(RadioSelect):
            assert rs.value == 9


@pytest.mark.asyncio
async def test_input_changed_too_small():
    async with ThreeDigitsRadioApp().run_test() as pilot:
        test_value = "-1"
        pilot.app.query_one(Input).value = test_value
        await pilot.click(Input)
        assert pilot.app.query_one(Input).value == test_value
        for rs in pilot.app.query(RadioSelect):
            assert rs.value == 0


@pytest.mark.asyncio
async def test_invalid_input_changed():
    async with ThreeDigitsRadioApp().run_test() as pilot:
        test_value = "invalid"
        pilot.app.query_one(Input).value = test_value
        await pilot.click(Input)
        assert pilot.app.query_one(Input).value == test_value
        for rs in pilot.app.query(RadioSelect):
            assert rs.value == 0


@pytest.mark.parametrize("test_value", [(0, 0, 0), (2, 3, 4), (7, 8, 9), (9, 9, 9)])
@pytest.mark.asyncio
async def test_radio_changed(test_value):
    """
    https://github.com/Textualize/textual/blob/main/tests/toggles/test_radioset.py
    """
    async with ThreeDigitsRadioApp().run_test() as pilot:
        for rs, digit in zip(pilot.app.query(RadioSet), test_value):
            rs._nodes[digit].toggle()
        await pilot.pause()

        for rs, digit in zip(pilot.app.query(RadioSelect), test_value):
            assert rs.value == digit

        assert pilot.app.query_one(Input).value == "".join(map(str, test_value))
