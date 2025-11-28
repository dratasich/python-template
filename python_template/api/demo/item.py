from pydantic import BaseModel


class Item(BaseModel):
    """A demo item model."""

    name: str
    description: str | None = None
