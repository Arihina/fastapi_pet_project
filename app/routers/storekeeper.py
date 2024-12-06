from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Product, Description, Buyer, Provider, Order, SalesRecord, StockRecord
from app.models.db_engine import engine
from app.schemas.base import ProductInfo, SaleInfo, StockInfo, ProductData

router = APIRouter(prefix='/storekeeper')

router.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent.parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get('/')
async def storekeeper(request: Request):
    return templates.TemplateResponse("storekeeper.html", {"request": request})


@router.get('/products-info')
async def get_products_info(request: Request, session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(Product.price, Product.stock, Description.dimensions, Description.weight, Description.furniture_type,
               Description.material, Product.id, Product.stock)
        .join(Description, Product.description_id == Description.id))

    result = await session.execute(query)
    result = [ProductInfo.from_orm(_).dict() for _ in result.fetchall()]

    return templates.TemplateResponse("products_table.html", {"request": request, "lst": result})


@router.get('/products-info-filtered')
async def filter_products_info(request: Request, furniture_type: str,
                               session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(Product.price, Product.stock, Description.dimensions, Description.weight, Description.furniture_type,
               Description.material, Product.id)
        .join(Description, Product.description_id == Description.id)
        .where(Description.furniture_type == furniture_type))

    result = await session.execute(query)
    result = [ProductInfo.from_orm(_).dict() for _ in result.fetchall()]

    return templates.TemplateResponse("products_table_filter.html", {"request": request, "lst": result})


@router.get('/sales-info')
async def get_sales_info(request: Request, session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(SalesRecord.date, Order.total_cost, Order.product_quantity, Buyer.address, Buyer.phone_number,
               )
    ).join(SalesRecord, Order.id == SalesRecord.order_id).join(Buyer, Buyer.id == SalesRecord.buyer_id)

    result = await session.execute(query)
    result = [SaleInfo.from_orm(_).dict() for _ in result.fetchall()]

    return templates.TemplateResponse("sales_table.html", {"request": request, "lst": result})


@router.get('/stocks-info')
async def get_stocks_info(request: Request, session: AsyncSession = Depends(engine.get_session)):
    query = (
        select(Provider.organization_name, StockRecord.product_id,
               StockRecord.date, StockRecord.quantity)
    ).join(Product, StockRecord.product_id == Product.id).join(Provider, Provider.id == Product.provider_id)

    result = await session.execute(query)
    result = [StockInfo.from_orm(_).dict() for _ in result.fetchall()]

    return templates.TemplateResponse("stocks_table.html", {"request": request, "lst": result})


@router.get('/orders-info')
async def get_orders_info(request: Request, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Order))
    result = result.scalars().all()

    return templates.TemplateResponse("orders_table.html", {"request": request, "lst": result})


@router.get('/providers-info')
async def get_providers_info(request: Request, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Provider))
    result = result.scalars().all()

    return templates.TemplateResponse("providers_table.html", {"request": request, "lst": result})


@router.get('/order-form')
async def get_order_form(request: Request):
    return templates.TemplateResponse("order_form.html", {"request": request})


@router.get('/buyer-form')
async def get_buyer_form(request: Request):
    return templates.TemplateResponse("buyer_form.html", {"request": request})


@router.get('/sale-form')
async def get_sale_form(request: Request):
    return templates.TemplateResponse("sale_form.html", {"request": request})


@router.get('/stock-form')
async def get_stock_form(request: Request):
    return templates.TemplateResponse("stock_form.html", {"request": request})


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

        if product_data.count is not None:
            product.stock = product_data.count

        await session.commit()
        await session.refresh(product)

        return '200'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении товара")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")
