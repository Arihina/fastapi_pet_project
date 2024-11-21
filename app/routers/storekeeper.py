from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Product, Description, SalesAccounting, Buyer, Provider, Order
from app.models.db_engine import engine
from app.schemas.base import ProductInfo, SaleInfo, BuyerInfo, OrderInfo

router = APIRouter(prefix='/storekeeper')


@router.get('/')
async def storekeeper(session: AsyncSession = Depends(engine.get_session)):
    pass


@router.get('/products-info')
async def get_products_info(session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(Product.price, Product.count, Description.dimensions, Description.weight, Description.furniture_type,
               Description.material)
        .join(Description, Product.description_id == Description.id))
    result = await session.execute(query)

    return [ProductInfo.from_orm(_).dict() for _ in result.fetchall()]


@router.get('/sales-info')
async def get_sales_info(session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(Product.price, Product.count, Product.order_id,
               SalesAccounting.date)
    ).join(SalesAccounting, Product.id == SalesAccounting.product_id)
    result = await session.execute(query)

    return [SaleInfo.from_orm(_).dict() for _ in result.fetchall()]


@router.get('/buyers-info')
async def get_buyers_info(session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(Buyer.full_name, Buyer.organization_name, Buyer.phone_number,
               Buyer.address, SalesAccounting.date, SalesAccounting.product_id)
    ).join(SalesAccounting, Buyer.id == SalesAccounting.buyer_id)
    result = await session.execute(query)

    return [BuyerInfo.from_orm(_).dict() for _ in result.fetchall()]


@router.get('/orders-info')
async def get_orders_info(session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(Order.product_quantity, Order.total_cost,
               Product.price, Product.count, Provider.product_name,
               Provider.email, Provider.phone_number, Provider.full_name)
    ).join(Provider, Provider.id == Order.provider_id).join(Product, Product.order_id == Order.id)
    result = await session.execute(query)

    return [OrderInfo.from_orm(_).dict() for _ in result.fetchall()]