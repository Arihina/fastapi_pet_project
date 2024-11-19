from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Order
from app.models.db_engine import engine
from app.schemas.base import OrderResponse, OrderRequest

router = APIRouter()


@router.get('/orders', response_model=list[OrderResponse])
async def get_orders(session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Order))
    orders = result.scalars().all()

    return orders


@router.get('/orders/{id}', response_model=OrderResponse)
async def get_order(id: int, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Order).where(Order.id == id))
    order = result.scalar_one_or_none()

    if order:
        return order
    else:
        raise HTTPException(status_code=404, detail="Order not found")


@router.post('/orders')
async def add_order(order: OrderRequest, session: AsyncSession = Depends(engine.get_session)):
    new_order = Order(
        product_quantity=order.product_quantity,
        total_cost=order.total_cost,
        provider_id=order.provider_id
    )

    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)

    return '201'


@router.put('/orders/{id}')
async def update_order(id: int, order_data: OrderRequest, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Order).where(Order.id == id))
    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if order_data.product_quantity is not None:
        order.product_quantity = order_data.product_quantity
    if order_data.total_cost is not None:
        order.total_cost = order_data.total_cost
    if order_data.provider_id is not None:
        order.provider_id = order_data.provider_id

    await session.commit()
    await session.refresh(order)

    return '200'


@router.delete('/orders/{id}')
async def delete_order(id: int, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Order).where(Order.id == id))
    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    await session.delete(order)
    await session.commit()

    return '204'

