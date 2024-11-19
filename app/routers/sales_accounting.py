from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import SalesAccounting
from app.models.db_engine import engine
from app.schemas.base import SalesAccountingResponse, SalesAccountingRequest

router = APIRouter()


@router.get('/sales-accounting', response_model=list[SalesAccountingResponse])
async def get_all_sales_accounting(session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(SalesAccounting))
    sales = result.scalars().all()

    return sales


@router.get('/sales-accounting/{id}', response_model=SalesAccountingResponse)
async def get_product(id: int, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(SalesAccounting).where(SalesAccounting.id == id))
    sale = result.scalar_one_or_none()

    if sale:
        return sale
    else:
        raise HTTPException(status_code=404, detail="Sale not found")


@router.post('/sales-accounting')
async def add_sales_accounting(sale_data: SalesAccountingRequest, session: AsyncSession = Depends(engine.get_session)):
    new_sales = SalesAccounting(
        date=sale_data.date,
        product_id=sale_data.product_id,
        buyer_id=sale_data.buyer_id
    )

    session.add(new_sales)
    await session.commit()
    await session.refresh(new_sales)

    return '201'


@router.put('/sales-accounting/{id}')
async def update_sales_accounting(id: int, sale_data: SalesAccountingRequest,
                                  session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(SalesAccounting).where(SalesAccounting.id == id))
    sale = result.scalar_one_or_none()

    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    if sale_data.date is not None:
        sale.date = sale_data.date
    if sale_data.product_id is not None:
        sale.product_id = sale_data.product_id
    if sale_data.buyer_id is not None:
        sale.buyer_id = sale_data.buyer_id

    await session.commit()
    await session.refresh(sale)

    return '200'


@router.delete('/sales-accounting/{id}')
async def delete_sales_accounting(id: int, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(SalesAccounting).where(SalesAccounting.id == id))
    sales_accounting = result.scalar_one_or_none()

    if sales_accounting is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    await session.delete(sales_accounting)
    await session.commit()

    return '204'
