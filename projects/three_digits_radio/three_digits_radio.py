from textual.app import App, ComposeResult
from textual.containers import Container
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, RadioButton, RadioSet


def prefix_zeros(value: str | int, n=3) -> str:
    value = str(value)
    len_value = len(value)
    if len_value > n:
        raise ValueError("Too many digits")
    n_zero = n - len_value
    return "0" * n_zero + value


class RadioSelect(Widget):
    DEFAULT_CSS = """
    RadioSelect {
        width: auto;
        height: auto;
    }
    """
    value = reactive(0)

    class RadioChangedMessage(Message):
        pass

    def __init__(self, loc: int):
        super().__init__()
        self.loc = loc

    def compose(self) -> ComposeResult:
        yield RadioSet(*(RadioButton(str(i)) for i in range(10)))

    def watch_value(self, value: int) -> None:
        rs_buttons = self.query(RadioButton)

        # need to clean radio buttons first
        for rs_button in rs_buttons:
            rs_button.value = False

        self.query_one(RadioSet).index = value
        for i, rs_button in enumerate(rs_buttons):
            if i == value:
                rs_button.value = True
                break

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        event.stop()
        self.value = event.index
        self.post_message(RadioSelect.RadioChangedMessage())


class RadioInput(Widget):
    DEFAULT_CSS = """
    RadioInput {
        width: auto;
        height: auto;
        border: blank;
        layout: horizontal;
    }
    RadioInput:focus-within {
        border: heavy $secondary;
    }
    """

    def compose(self) -> ComposeResult:
        for loc in reversed(range(3)):
            yield RadioSelect(loc)


class RadioEditor(Widget):
    DEFAULT_CSS = """
     RadioEditor > Container {
        align: center middle;
    }

    RadioEditor > Container.top {
        height: 1fr;
        background: $boost;
    }
    RadioEditor > Container.bottom {
        height: 2fr;
    }
    RadioEditor Input {
        width: 16;
    }
    """
    value = reactive(0)

    def validate_value(self, value: int) -> int:
        if value <= 0:
            value = 0
        elif value >= 999:
            value = 999
        return value

    def compose(self) -> ComposeResult:
        with Container(classes="top"):
            yield Input("000")
        with Container(classes="bottom"):
            yield RadioInput(id="radio-input")

    def on_radio_select_radio_changed_message(
        self, event: RadioSelect.RadioChangedMessage
    ) -> None:
        value = 0
        for rs in self.query(RadioSelect):
            value += 10 ** (rs.loc) * rs.value
        self.query_one(Input).value = prefix_zeros(value)

    def on_input_changed(self, event: Input.Changed) -> None:
        try:
            self.value = int(event.value or "000")
        except ValueError:
            pass

    def watch_value(self, value: int):
        value = prefix_zeros(value)
        reverse_value = value[::-1]
        for rs in self.query(RadioSelect):
            with rs.prevent(RadioSelect.RadioChangedMessage):
                rs.value = int(reverse_value[rs.loc])


class ThreeDigitsRadioApp(App):
    def compose(self) -> ComposeResult:
        yield RadioEditor()


if __name__ == "__main__":
    app = ThreeDigitsRadioApp()
    app.run()
