from flet import (
    Animation,
    AnimationCurve,
    Column,
    Container,
    Dropdown,
    Event,
    FontWeight,
    Icon,
    IconButton,
    Icons,
    MainAxisAlignment,
    Padding,
    Row,
    Text,
    control,
)

from gui.checkboxes import Checkboxes
from gui.controls import CheckboxCategory, SelectionButton
from gui.shared import FletControl


class OptionCategory:
    def __init__(
        self,
        text: str,
        text_width: int,
        block_width: int,
        checkboxes: list[FletControl],
    ) -> None:
        self.text = Text(value=text, size=20, weight=FontWeight.BOLD)

        self.row = Row(
            controls=[self.text],
            width=text_width,
            alignment=MainAxisAlignment.CENTER,
        )

        self.block = Column(
            controls=[
                self.row,
                Column(
                    controls=checkboxes,
                    alignment=MainAxisAlignment.START,
                    spacing=-10,
                ),
            ],
            width=block_width,
        )


@control
class ExpandableOptions(Container):
    def init(self) -> None:
        self.full_height = 760
        self.hidden_height = 64
        self.height = self.hidden_height

        self.bgcolor = "white10"
        self.border_radius = 11
        self.animate_size = Animation(400, AnimationCurve.DECELERATE)
        self.padding = Padding.only(left=10, right=10, top=10)

        self.name = Text(size=16, weight=FontWeight.BOLD)

        self.expand_icon = IconButton(
            icon=Icons.KEYBOARD_ARROW_DOWN,
            icon_size=30,
            on_click=self.expand_container,
        )

        self.preset = Dropdown()
        self.select_all_button = SelectionButton(
            content="select_all",
            data=True,
        )
        self.deselect_all_button = SelectionButton(
            content="deselect_all",
            data=False,
        )
        self.checkboxes = Checkboxes()

        self.icon_options = OptionCategory(
            text="t_icons",
            text_width=190,
            block_width=190,
            checkboxes=self.checkboxes.icons_group,
        )
        self.text_options = OptionCategory(
            text="t_text",
            text_width=210,
            block_width=210,
            checkboxes=self.checkboxes.text_group,
        )
        self.sound_options = OptionCategory(
            text="t_sounds",
            text_width=135,
            block_width=135,
            checkboxes=self.checkboxes.sound_group,
        )
        self.models_options = OptionCategory(
            text="t_models",
            text_width=210,
            block_width=210,
            checkboxes=self.checkboxes.models_group,
        )
        self.textures_options = OptionCategory(
            text="t_textures",
            text_width=135,
            block_width=135,
            checkboxes=self.checkboxes.textures_group,
        )
        self.other_options = OptionCategory(
            text="t_other",
            text_width=150,
            block_width=150,
            checkboxes=self.checkboxes.other_group,
        )
        self.executable_options = OptionCategory(
            text="t_exe",
            text_width=185,
            block_width=185,
            checkboxes=self.checkboxes.executable_group,
        )

        self.content = Column(
            controls=[
                Row(
                    controls=[
                        Icon(Icons.SETTINGS),
                        self.name,
                        self.expand_icon,
                    ],
                    spacing=10,
                ),
                Column(
                    controls=[
                        Row(
                            controls=[
                                self.preset,
                                self.select_all_button,
                                self.deselect_all_button,
                            ],
                            alignment=MainAxisAlignment.CENTER,
                        ),
                        Row(
                            width=self.width,
                            height=365,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                CheckboxCategory(content=category.block)
                                for category in (
                                    self.icon_options,
                                    self.text_options,
                                    self.sound_options,
                                    self.models_options,
                                )
                            ],
                        ),
                        Row(
                            width=self.width,
                            height=235,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                CheckboxCategory(content=category.block)
                                for category in (
                                    self.textures_options,
                                    self.other_options,
                                    self.executable_options,
                                )
                            ],
                        ),
                    ],
                ),
            ],
            spacing=12,
        )

    def expand_container(self, _: Event) -> None:
        """Open or close container depending on it's current height."""
        if self.height != self.full_height:
            self.height = self.full_height
            self.expand_icon.icon = Icons.KEYBOARD_ARROW_UP
            self.update()
            return

        self.height = self.hidden_height
        self.expand_icon.icon = Icons.KEYBOARD_ARROW_DOWN
        self.update()
