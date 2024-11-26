from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Product, Description, SalesAccounting, Buyer, Provider, Order
from app.models.db_engine import engine
from app.schemas.base import ProductInfo, SaleInfo, BuyerInfo, OrderInfo, ProductData

router = APIRouter(prefix='/storekeeper')

router.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent.parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get('/')
async def storekeeper(request: Request):
    return templates.TemplateResponse("storekeeper.html", {"request": request})


@router.get('/products-info')
async def get_products_info(request: Request, session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(Product.price, Product.count, Description.dimensions, Description.weight, Description.furniture_type,
               Description.material, Product.id)
        .join(Description, Product.description_id == Description.id))

    result = await session.execute(query)
    result = [ProductInfo.from_orm(_).dict() for _ in result.fetchall()]

    return templates.TemplateResponse("products_table.html", {"request": request, "lst": result})


@router.get('/products-info-filtered')
async def filter_products_info(request: Request, furniture_type: str,
                               session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(Product.price, Product.count, Description.dimensions, Description.weight, Description.furniture_type,
               Description.material, Product.id)
        .join(Description, Product.description_id == Description.id)
        .where(Description.furniture_type == furniture_type))

    result = await session.execute(query)
    result = [ProductInfo.from_orm(_).dict() for _ in result.fetchall()]

    return templates.TemplateResponse("products_table_filter.html", {"request": request, "lst": result})


@router.get('/sales-info')
async def get_sales_info(request: Request, session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(Product.price, Product.count, Product.order_id,
               SalesAccounting.date)
    ).join(SalesAccounting, Product.id == SalesAccounting.product_id)

    result = await session.execute(query)
    result = [SaleInfo.from_orm(_).dict() for _ in result.fetchall()]

    return templates.TemplateResponse("sales_table.html", {"request": request, "lst": result})


@router.get('/buyers-info')
async def get_buyers_info(request: Request, session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(Buyer.full_name, Buyer.organization_name, Buyer.phone_number,
               Buyer.address, SalesAccounting.date, SalesAccounting.product_id)
    ).join(SalesAccounting, Buyer.id == SalesAccounting.buyer_id)

    result = await session.execute(query)
    result = [BuyerInfo.from_orm(_).dict() for _ in result.fetchall()]

    return templates.TemplateResponse("buyers_table.html", {"request": request, "lst": result})


@router.get('/buyers-info-filtered')
async def filter_buyers_info(request: Request, full_name: str,
                             session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(Buyer.full_name, Buyer.organization_name, Buyer.phone_number,
               Buyer.address, SalesAccounting.date, SalesAccounting.product_id)
    ).join(SalesAccounting, Buyer.id == SalesAccounting.buyer_id).where(Buyer.full_name == full_name)

    result = await session.execute(query)
    result = [BuyerInfo.from_orm(_).dict() for _ in result.fetchall()]

    return templates.TemplateResponse("buyers_table_filter.html", {"request": request, "lst": result})


@router.get('/orders-info')
async def get_orders_info(request: Request, session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(Order.product_quantity, Order.total_cost, Order.id,
               Provider.product_name, Provider.email,
               Provider.phone_number, Provider.full_name)
    ).join(Provider, Provider.id == Order.provider_id).join(Product, Product.order_id == Order.id)

    result = await session.execute(query)
    result = [OrderInfo.from_orm(_).dict() for _ in result.fetchall()]

    return templates.TemplateResponse("orders_table.html", {"request": request, "lst": result})


@router.get('/orders-info-filtered')
async def filter_orders_info(request: Request, product_name: str,
                             session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(Order.product_quantity, Order.total_cost, Order.id,
               Provider.product_name, Provider.email,
               Provider.phone_number, Provider.full_name)
    ).join(Provider, Provider.id == Order.provider_id).join(Product, Product.order_id == Order.id).where(
        Provider.product_name == product_name)

    result = await session.execute(query)
    result = [OrderInfo.from_orm(_).dict() for _ in result.fetchall()]

    return templates.TemplateResponse("orders_table_filter.html", {"request": request, "lst": result})


@router.get('/order-form')
async def get_order_form(request: Request):
    return templates.TemplateResponse("order_form.html", {"request": request})


@router.get('/product-form')
async def get_product_form(request: Request):
    return templates.TemplateResponse("product_form.html", {"request": request})


@router.get('/sale-form')
async def get_sale_form(request: Request):
    return templates.TemplateResponse("sale_form.html", {"request": request})


@router.get('/edit-form')
async def get_edit_form(request: Request):
    return templates.TemplateResponse("storekeeper_put_form.html", {"request": request})


@router.patch('/products')
async def update_product_info(product_data: ProductData, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Product).where(Product.id == product_data.id))
        product = result.scalar_one_or_none()

        if product is None:
            raise HTTPException(status_code=404, detail="Товар не найден")

        if product_data.price is not None:
            product.price = product_data.price
        if product_data.count is not None:
            product.count = product_data.count
        if product_data.order_id is not None:
            product.provider_id = product_data.order_id
        if product_data.description_id is not None:
            product.description_id = product_data.description_id

        await session.commit()
        await session.refresh(product)

        return '200'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении товара")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")
