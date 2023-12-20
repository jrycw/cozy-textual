import pytest
from textual.widgets import Input
from three_digits_radio import RadioSelect, ThreeDigitsRadioApp


@pytest.mark.asyncio
async def test_initial_input():
    app = ThreeDigitsRadioApp()
    async with app.run_test() as pilot:
        await pilot.click(Input)
        assert app.query_one(Input).value == "000"


@pytest.mark.asyncio
async def test_input_changed():
    app = ThreeDigitsRadioApp()
    async with app.run_test() as pilot:
        test_value = "234"
        app.query_one(Input).value = test_value
        await pilot.click(Input)
        assert app.query_one(Input).value == test_value

        for rs, digit in zip(app.query(RadioSelect), test_value):
            assert rs.value == int(digit)


@pytest.mark.skip(reason="need to figure it out how to click the specific radio button")
@pytest.mark.asyncio
async def test_radio_changed():
    app = ThreeDigitsRadioApp()
    async with app.run_test() as pilot:
        test_value = [2, 3, 4]
