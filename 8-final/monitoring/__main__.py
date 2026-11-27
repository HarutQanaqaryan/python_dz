from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static


class MonitoringApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Мониторинг доступности — заготовка")
        yield Footer()


def main() -> None:
    MonitoringApp().run()


if __name__ == "__main__":
    main()