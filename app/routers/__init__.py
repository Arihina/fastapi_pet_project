from fastapi import APIRouter

from .descriptions import router as descriptions_router
from .orders import router as orders_router
from .buyers import router as buyer_router
from .providers import router as provider_router
from .products import router as product_router
from .sales_accounting import router as sales_accounting_router

router = APIRouter()

router.include_router(descriptions_router)
router.include_router(orders_router)
router.include_router(buyer_router)
router.include_router(provider_router)
router.include_router(product_router)
router.include_router(sales_accounting_router)
