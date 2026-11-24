from flet import (
    Alignment,
    Button,
    Colors,
    Column,
    Container,
    FontWeight,
    MainAxisAlignment,
    ProgressBar,
    Row,
    ScrollMode,
    Stack,
    Text,
    control,
)

from gui.controls import RandomizationLog, RandomizationLogHeading, RandomizationLogOverlay


@control
class RandomizationOverlay(Stack):
    def init(self) -> None:
        self.expand = True
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        self.alignment = Alignment.CENTER

        self.background = Container(bgcolor=Colors.BLACK_87, expand=True)

        self.progress_bar = ProgressBar(width=590, height=20, value=0)
        self.heading = Text(size=16, weight=FontWeight.BOLD)
        self.ok_button = Button(content="OK", width=150, height=50)
        self.log = Column(
            spacing=1,
            width=600,
            scroll=ScrollMode.ALWAYS,
        )

        self.controls = [
            self.background,
            RandomizationLogOverlay(
                content=Column(
                    controls=[
                        Row(
                            controls=[RandomizationLogHeading(content=self.heading)],
                            alignment=MainAxisAlignment.CENTER,
                        ),
                        Row(
                            controls=[RandomizationLog(content=self.log)],
                            alignment=MainAxisAlignment.CENTER,
                        ),
                        Row(
                            controls=[self.progress_bar],
                            alignment=MainAxisAlignment.CENTER,
                        ),
                        Row(
                            controls=[self.ok_button],
                            alignment=MainAxisAlignment.CENTER,
                        ),
                    ],
                ),
            ),
        ]
