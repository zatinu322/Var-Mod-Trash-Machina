from pydantic import ConfigDict

model_config = ConfigDict(
    validate_assignment=True,
    validate_default=True,
    extra="forbid",
)
