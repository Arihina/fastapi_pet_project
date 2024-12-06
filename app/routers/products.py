from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Product
from app.models.db_engine import engine
from app.schemas.base import ProductResponse, ProductRequest

router = APIRouter()

router.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent.parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get('/products', response_model=list[ProductResponse])
async def get_products(request: Request,  session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Product))
        products = result.scalars().all()

        return templates.TemplateResponse('products.html', {"request": request, "lst": products})
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при получении товаров")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.get('/products/form')
async def get_product_form(request: Request):
    return templates.TemplateResponse("product_form.html", {"request": request})


@router.get('/products/{id}', response_model=ProductResponse)
async def get_product(request: Request, id: int, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Product).where(Product.id == id))
        product = result.scalar_one_or_none()

        if product:
            return templates.TemplateResponse('product_card.html', {"request": request, "pr": product})
        else:
            raise HTTPException(status_code=404, detail="Товар не найден")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при получении товара")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.post('/products')
async def add_product(product: ProductRequest, session: AsyncSession = Depends(engine.get_session)):
    try:
        new_product = Product(
            price=product.price,
            stock=product.stock,
            provider_id=product.provider_id,
            description_id=product.description_id
        )

        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)

        return '201'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при добавлении товаров")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.put('/products/{id}')
async def update_product(id: int, product_data: ProductRequest,
                         session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Product).where(Product.id == id))
        product = result.scalar_one_or_none()

        if product is None:
            raise HTTPException(status_code=404, detail="Товар не найден")

        if product_data.price is not None:
            product.price = product_data.price
        if product_data.stock is not None:
            product.stock = product_data.stock
        if product_data.provider_id is not None:
            product.provider_id = product_data.provider_id
        if product_data.description_id is not None:
            product.description_id = product_data.description_id

        await session.commit()
        await session.refresh(product)

        return '200'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении товара")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.delete('/products/{id}')
async def delete_product(id: int, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Product).where(Product.id == id))
        product = result.scalar_one_or_none()

        if product is None:
            raise HTTPException(status_code=404, detail="Товар не найден")

        await session.delete(product)
        await session.commit()

        return '204'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при удалении товара")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")

