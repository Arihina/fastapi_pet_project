from fastapi import APIRouter

from .description import router as descriptions_router
from .orders import router as orders_router

router = APIRouter()

router.include_router(descriptions_router)
router.include_router(orders_router)
