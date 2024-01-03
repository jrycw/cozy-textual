import pytest
from textual.widgets._select import SelectOverlay  # noqa: F401
from typing_tutor import Select, TypingTutorApp, textual_facts  # noqa: F401


@pytest.mark.asyncio
async def test_initial_select():
    async with TypingTutorApp().run_test() as pilot:
        assert pilot.app.query_one("#topic_select").value == Select.BLANK


@pytest.mark.asyncio
async def test_initial_orig():
    async with TypingTutorApp().run_test() as pilot:
        assert str(pilot.app.query_one("#orig").renderable) == textual_facts[0]


@pytest.mark.parametrize(
    "offset, idx",
    [
        ((2, 2), 0),
        ((2, 3), 1),
        ((2, 5), 2),
        ((2, 6), 3),
        ((2, 8), 4),
        ((2, 9), 5),
    ],
)
@pytest.mark.asyncio
async def test_select_changed(offset, idx):
    expected = textual_facts[idx]
    async with TypingTutorApp().run_test() as pilot:
        await pilot.click(Select)
        await pilot.click(SelectOverlay, offset=offset)
        await pilot.pause()
        assert str(pilot.app.query_one("#topic_select").value) == expected

        for key in expected:
            await pilot.press(key)
        await pilot.pause()
        assert str(pilot.app.query_one("#diff").renderable) == expected
        assert len(pilot.app._notifications) == 1
        assert pilot.app.query_one("#pgbar").progress == 100
