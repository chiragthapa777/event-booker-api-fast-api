from pydantic import BaseModel, ConfigDict

def to_camel(string: str) -> str:
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class BaseDto(BaseModel):
    model_config = ConfigDict(
    from_attributes=True,
    alias_generator=to_camel,  # default for all other fields
    populate_by_name=True,
)
