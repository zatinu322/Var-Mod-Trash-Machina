from flet import (
    Column,
    Container,
    CrossAxisAlignment,
    Dropdown,
    Image,
    MainAxisAlignment,
    Row,
    ScrollMode,
    control,
)

from gui.controls import (
    GamePathBrowser,
    LangButton,
    RandomizationButton,
)
from gui.options import ExpandableOptions
from gui.overlay import InactiveOverlay, RandomizationOverlay
from gui.values import LangDecorationImage
from helpers.paths_utils import ASSETS_PATH


@control
class RandomizerGUI(Container):
    def init(self) -> None:
        self.rus_button = LangButton(image=LangDecorationImage(src=str((ASSETS_PATH / "rus.png").resolve())))
        self.eng_button = LangButton(image=LangDecorationImage(src=str((ASSETS_PATH / "eng.png").resolve())))
        self.options = ExpandableOptions(width=self.width)
        self.path_browser = GamePathBrowser()
        self.version = Dropdown(width=600)
        self.randomization_button = RandomizationButton()

        self.inactive_overlay = InactiveOverlay()
        self.randomization_overlay = RandomizationOverlay()

        self.content = Column(
            controls=[
                # extra row because padding and margin breaks scrolling
                Row(height=1),
                # language buttons
                Row(
                    controls=[self.rus_button, self.eng_button],
                    width=200,
                    alignment=MainAxisAlignment.CENTER,
                    spacing=30,
                ),
                # randomizer logo
                Row(
                    controls=[Container(
                        content=Image(
                            src=str((ASSETS_PATH / "logo.png").resolve()),
                            width=self.width,
                        ),
                    )],
                    alignment=MainAxisAlignment.CENTER,
                ),
                # settings
                Row(
                    controls=[self.options],
                    alignment=MainAxisAlignment.CENTER,
                ),
                # game path selection
                Row(
                    controls=[self.path_browser],
                    width=self.width,
                    height=100,
                    alignment=MainAxisAlignment.SPACE_AROUND,
                ),
                # game version selection
                Row(
                    controls=[self.version],
                    width=self.width,
                    alignment=MainAxisAlignment.SPACE_AROUND,
                ),
                # start randomization button
                Row(
                    controls=[self.randomization_button],
                    width=self.width,
                    alignment=MainAxisAlignment.CENTER,
                ),
                # extra row, because padding and margin breaks scrolling
                Row(height=1),
            ],
            # width=self.page.width - (self.page.padding.left * 2),
            horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.START,
            scroll=ScrollMode.HIDDEN,
            spacing=30,
        )
