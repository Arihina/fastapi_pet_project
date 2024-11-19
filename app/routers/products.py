from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Product
from app.models.db_engine import engine
from app.schemas.base import ProductResponse, ProductRequest

router = APIRouter()


@router.get('/products', response_model=list[ProductResponse])
async def get_products(session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Product))
    products = result.scalars().all()

    return products


@router.get('/products/{id}', response_model=ProductResponse)
async def get_product(id: int, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Product).where(Product.id == id))
    product = result.scalar_one_or_none()

    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@router.post('/products')
async def add_product(product: ProductRequest, session: AsyncSession = Depends(engine.get_session)):
    new_product = Product(
        price=product.price,
        count=product.count,
        order_id=product.order_id,
        description_id=product.description_id
    )

    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)

    return '201'


@router.put('/products/{id}')
async def update_product(id: int, product_data: ProductRequest,
                         session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Product).where(Product.id == id))
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if product_data.price is not None:
        product.price = product_data.price
    if product_data.count is not None:
        product.count = product_data.count
    if product_data.order_id is not None:
        product.order_id = product_data.order_id
    if product_data.description_id is not None:
        product.description_id = product_data.description_id

    await session.commit()
    await session.refresh(product)

    return '200'


@router.delete('/products/{id}')
async def delete_product(id: int, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Product).where(Product.id == id))
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    await session.delete(product)
    await session.commit()

    return '204'
