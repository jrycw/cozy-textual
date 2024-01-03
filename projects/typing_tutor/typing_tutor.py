import time

from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Horizontal, Middle, VerticalScroll
from textual.widgets import ProgressBar, Select, Static, TextArea

# TODO
# "Textual apps run on macOS, Linux, and Windows — from single board computer to the most powerful server. Locally, or over SSH."
# "—" will cause test failure(missing one dot in the end).
# How to properly test "em-dash" key event without directly accessing renderable?

textual_facts = [
    "Textual is a Rapid Application Development framework for Python.",
    "Build sophisticated user interfaces with a simple Python API.",
    "Run your apps in the terminal and a web browser!",
    "Textual adds interactivity to Rich with an API inspired by modern web development.",
    "Textual apps run on macOS, Linux, and Windows.",
    "Build with Python. Deploy anywhere.",
]


def get_excerpt(line: str) -> str:
    excerpt = " ".join(line.split()[:4])
    if len(excerpt) > 4:
        excerpt += "..."
    return excerpt


class TypingTutorApp(App):
    CSS_PATH = "typing_tutor.tcss"

    def compose(self) -> ComposeResult:
        with Horizontal(id="top-h"):
            with Center():
                with Middle():
                    yield Select(
                        ((get_excerpt(line), line) for line in textual_facts),
                        prompt="Please select one topic",
                        id="topic_select",
                    )

            with Center():
                with Middle():
                    yield ProgressBar(id="pgbar", total=100, show_eta=False)

        with VerticalScroll():
            yield Static(id="orig")
        with VerticalScroll():
            yield Static(id="diff")
        with VerticalScroll():
            typing_area = TextArea(id="typing_area")
            typing_area.focus()
            yield typing_area

    def _set_default(self) -> None:
        self._orig_len = len(self._orig)
        self.query_one("#orig").update(self._orig)
        self.query_one("#diff").update()
        self.query_one("#typing_area").text = ""
        self.query_one("#typing_area").focus()

        self._is_notify = False
        self._start = time.perf_counter()

    def on_mount(self) -> None:
        self._orig = textual_facts[0]  # default
        self._set_default()

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self._orig = str(event.value)
        self._set_default()

    @on(TextArea.Changed, "#typing_area")
    def on_typing_area_changed(self, event: TextArea.Changed) -> None:
        if self._is_notify:
            return

        contents = Text()
        count = 0
        _event = event.text_area.text
        for orig_text, event_text in zip(self._orig, _event):
            if orig_text == event_text:
                contents.append(event_text)
                count += 1
            else:
                self.log("not equal")
                contents.append(f"{orig_text}", style="bold magenta")

        self.query_one("#diff").update(contents)

        percentage = round(count / self._orig_len * 100)
        self.query_one("#pgbar").update(total=100, progress=percentage)

        if percentage == 100:
            elapsed = time.perf_counter() - self._start
            self.notify(f"Completed in {elapsed:.2f} secs")
            self.bell()
            self._is_notify = True


if __name__ == "__main__":
    app = TypingTutorApp()
    app.run()
