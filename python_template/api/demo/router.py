"""
Demo endpoints.

Check out following FastAPI documentation for more details:
- https://fastapi.tiangolo.com/tutorial/security/first-steps/#check-it
"""

from fastapi import APIRouter, HTTPException, Request

from python_template.api.middleware.log import LogMiddleware
from python_template.config import Configuration
from python_template.infrastructure.repository import Repository

from .item import Item

router = APIRouter(tags=["demo"])


@router.get("/config")
async def get_config(req: Request):
    """Get the application configuration."""
    config: Configuration = req.app.state.config
    bound_logger = LogMiddleware.get_logger(req)
    bound_logger.debug("Configuration endpoint called")
    return config.model_dump()


@router.get("/item/{item_id}")
async def get_item(req: Request, item_id: int) -> Item:
    """A demo endpoint to get an item."""
    repo: Repository = req.app.state.repo
    item_from_repo = repo.get(item_id=item_id)
    if item_from_repo is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item = Item(
        name=item_from_repo,
        description="A demo item retrieved from the repository.",
    )
    return item


@router.post("/item", status_code=201)
async def create_item(req: Request, item: Item) -> int:
    """A demo endpoint to create an item."""
    repo: Repository = req.app.state.repo
    return repo.put(item.name)
