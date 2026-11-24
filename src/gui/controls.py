from dataclasses import field

from flet import (
    Alignment,
    Border,
    Button,
    ButtonStyle,
    Colors,
    Column,
    Container,
    Icons,
    Padding,
    ProgressRing,
    Row,
    Text,
    TextField,
    control,
)

from gui.values import RandomizerButtonStyle


@control
class LangButton(Container):
    width: int = 80
    height: int = 40
    ink: bool = True


@control
class GamePathBrowser(Column):
    def init(self) -> None:
        self.path_field = TextField(width=600)
        self.browse_button = Button(
            bgcolor=Colors.WHITE_10,
            style=RandomizerButtonStyle(),
            content="browse",
            icon=Icons.FOLDER_OPEN,
        )
        self.status = Text()
        self.progress_ring = ProgressRing(width=16, height=16, stroke_width=2, visible=False)

        self.controls = [
            Row(controls=[self.path_field]),
            Row(controls=[self.browse_button, self.progress_ring, self.status]),
        ]


@control
class RandomizationButton(Button):
    width: int = 300
    height: int = 70
    style: ButtonStyle = field(default_factory=RandomizerButtonStyle)
    content: str = "randomize"


@control
class SelectionButton(Button):
    style: ButtonStyle = field(default_factory=RandomizerButtonStyle)
    width: int = 150
    height: int = 58


@control
class CheckboxCategory(Container):
    border: Border = field(default_factory=lambda: Border.all(1, Colors.BLACK))
    border_radius: int = 10
    bgcolor: Colors = Colors.WHITE_10


@control
class RandomizationLogOverlay(Container):
    alignment: Alignment = field(default_factory=lambda: Alignment.TOP_CENTER)
    bgcolor: str = "#3d5a68"
    opacity: int = 1
    border_radius: int = 20
    width: int = 700
    height: int = 470


@control
class RandomizationLogHeading(Container):
    padding: Padding = field(default_factory=lambda: Padding.only(top=5))


@control
class RandomizationLog(Container):
    width: int = 600
    height: int = 330

    opacity: float = 0.7
    alignment: Alignment = field(default_factory=lambda: Alignment.TOP_LEFT)
    padding: int = 10

    bgcolor: Colors = Colors.BLACK
    border_radius: int = 10
