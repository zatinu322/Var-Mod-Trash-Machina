from dataclasses import field

from flet import (
    Button,
    Colors,
    Column,
    Container,
    CrossAxisAlignment,
    FontWeight,
    MainAxisAlignment,
    ProgressBar,
    Row,
    ScrollMode,
    Text,
    control,
)

from gui.controls import RandomizationLog, RandomizationLogHeading, RandomizationLogOverlay


@control
class InactiveOverlay(Container):
    bgcolor: Colors = Colors.BLACK_87
    content: Row = field(default_factory=lambda: Row(
        controls=[
            Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            ),
        ],
    ))


@control
class RandomizationOverlay(Row):
    def init(self) -> None:
        self.width = 800
        self.alignment = MainAxisAlignment.CENTER

        self.progress_bar = ProgressBar(width=590, height=20, value=0)
        self.status = Text()
        self.heading = Text(size=16, weight=FontWeight.BOLD)
        self.ok_button = Button(content="OK", width=150, height=50)
        self.log = Column(
            spacing=1,
            width=600,
            scroll=ScrollMode.ALWAYS,
        )

        self.controls = [
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
