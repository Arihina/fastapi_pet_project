from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Order
from app.models.db_engine import engine
from app.schemas.base import OrderResponse

router = APIRouter()


@router.get("/orders", response_model=list[OrderResponse])
async def get_orders(session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Order))
    orders = result.scalars().all()

    return orders
