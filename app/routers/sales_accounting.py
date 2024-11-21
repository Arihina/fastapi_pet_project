from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import SalesAccounting
from app.models.db_engine import engine
from app.schemas.base import SalesAccountingResponse, SalesAccountingRequest

router = APIRouter()

router.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent.parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get('/sales-accounting', response_model=list[SalesAccountingResponse])
async def get_all_sales_accounting(request: Request, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(SalesAccounting))
        sales = result.scalars().all()

        return templates.TemplateResponse('sales.html', {"request": request, "lst": sales})
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при получении продаж")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.get('/sales-accounting/form')
async def get_sale_form(request: Request):
    return templates.TemplateResponse("sale_form.html", {"request": request})


@router.get('/sales-accounting/{id}', response_model=SalesAccountingResponse)
async def get_sale(request: Request, id: int, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(SalesAccounting).where(SalesAccounting.id == id))
        sale = result.scalar_one_or_none()

        if sale:
            return templates.TemplateResponse('sale_card.html', {"request": request, "sale": sale})
        else:
            raise HTTPException(status_code=404, detail="Продажа не найдена")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при получении продажи")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.post('/sales-accounting')
async def add_sales_accounting(sale_data: SalesAccountingRequest, session: AsyncSession = Depends(engine.get_session)):
    try:
        new_sales = SalesAccounting(
            date=sale_data.date,
            product_id=sale_data.product_id,
            buyer_id=sale_data.buyer_id
        )

        session.add(new_sales)
        await session.commit()
        await session.refresh(new_sales)

        return '201'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при добавлении продажи")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.put('/sales-accounting/{id}')
async def update_sales_accounting(id: int, sale_data: SalesAccountingRequest,
                                  session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(SalesAccounting).where(SalesAccounting.id == id))
        sale = result.scalar_one_or_none()

        if sale is None:
            raise HTTPException(status_code=404, detail="Продажа не найдена")

        if sale_data.date is not None:
            sale.date = sale_data.date
        if sale_data.product_id is not None:
            sale.product_id = sale_data.product_id
        if sale_data.buyer_id is not None:
            sale.buyer_id = sale_data.buyer_id

        await session.commit()
        await session.refresh(sale)

        return '200'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при обвнолении продажи")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.delete('/sales-accounting/{id}')
async def delete_sales_accounting(id: int, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(SalesAccounting).where(SalesAccounting.id == id))
        sales_accounting = result.scalar_one_or_none()

        if sales_accounting is None:
            raise HTTPException(status_code=404, detail="Продажа не найдена")

        await session.delete(sales_accounting)
        await session.commit()

        return '204'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при удалении продажи")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")
