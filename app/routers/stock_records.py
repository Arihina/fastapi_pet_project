from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import StockRecord
from app.models.db_engine import engine
from app.schemas.base import StockRecordRequest, StockRecordResponse

router = APIRouter()

router.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent.parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get('/stocks-accounting', response_model=list[StockRecordResponse])
async def get_all_stocks_accounting(request: Request, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(StockRecord))
        stocks = result.scalars().all()

        return templates.TemplateResponse('stocks.html', {"request": request, "lst": stocks})
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при получении поступления")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.get('/stocks-accounting/form')
async def get_stock_form(request: Request):
    return templates.TemplateResponse("stock_form.html", {"request": request})


@router.get('/stock-accounting/{id}', response_model=StockRecordResponse)
async def get_sale(request: Request, id: int, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(StockRecord).where(StockRecord.id == id))
        stock = result.scalar_one_or_none()

        if stock:
            return templates.TemplateResponse('stock_card.html', {"request": request, "sale": stock})
        else:
            raise HTTPException(status_code=404, detail="Поступление не найдена")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при получении поступления")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.post('/stocks-accounting')
async def add_stocks_accounting(stock_data: StockRecordRequest, session: AsyncSession = Depends(engine.get_session)):
    try:
        new_stock = StockRecord(
            date=stock_data.date,
            product_id=stock_data.product_id,
            quantity=stock_data.quantity
        )

        session.add(new_stock)
        await session.commit()
        await session.refresh(new_stock)

        return '201'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при добавлении поступлаения")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.put('/stocks-accounting/{id}')
async def update_stocks_accounting(id: int, stock_data: StockRecordRequest,
                                   session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(StockRecord).where(StockRecord.id == id))
        stock = result.scalar_one_or_none()

        if stock is None:
            raise HTTPException(status_code=404, detail="Поступление не найдено")

        if stock_data.date is not None:
            stock.date = stock_data.date
        if stock_data.product_id is not None:
            stock.product_id = stock_data.product_id
        if stock_data.quantity is not None:
            stock.quantity = stock_data.quantity

        await session.commit()
        await session.refresh(stock)

        return '200'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при обвнолении продажи")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.delete('/stocks-accounting/{id}')
async def delete_stock_accounting(id: int, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(StockRecord).where(StockRecord.id == id))
        stock_accounting = result.scalar_one_or_none()

        if stock_accounting is None:
            raise HTTPException(status_code=404, detail="Поступление не найдено")

        await session.delete(stock_accounting)
        await session.commit()

        return '204'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при удалении поступления")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")
