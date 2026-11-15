from dataclasses import field

from flet import (
    BoxFit,
    ButtonStyle,
    Colors,
    DecorationImage,
    RoundedRectangleBorder,
    value,
)


@value
class RandomizerButtonStyle(ButtonStyle):
    shape: RoundedRectangleBorder = field(default_factory=lambda: RoundedRectangleBorder(radius=10))
    bgcolor: str = "#8BA6B3"
    color: str = Colors.BLACK


@value
class LangDecorationImage(DecorationImage):
    fit: BoxFit = BoxFit.FILL
