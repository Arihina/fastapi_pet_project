from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Buyer
from app.models.db_engine import engine
from app.schemas.base import BuyerResponse, BuyerRequest

router = APIRouter()

router.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent.parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get('/buyers')
async def get_buyers(request: Request, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Buyer))
        buyers = result.scalars().all()

        return templates.TemplateResponse('buyers.html', {"request": request, "lst": buyers})
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при получении покупателей")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.get('/buyers/form')
async def get_buyer_form(request: Request):
    return templates.TemplateResponse("buyer_form.html", {"request": request})


@router.get('/buyers/{id}', response_model=BuyerResponse)
async def get_buyer(request: Request, id: int, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Buyer).where(Buyer.id == id))
        buyer = result.scalar_one_or_none()

        if buyer:
            return templates.TemplateResponse('buyer_card.html', {"request": request, "buyer": buyer})
        else:
            raise HTTPException(status_code=404, detail="Покупатель не найден")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при получении покупателя")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.post('/buyers')
async def add_buyer(buyer: BuyerRequest, session: AsyncSession = Depends(engine.get_session)):
    try:
        new_buyer = Buyer(
            full_name=buyer.full_name,
            organization_name=buyer.organization_name,
            phone_number=buyer.phone_number,
            address=buyer.address
        )

        session.add(new_buyer)
        await session.commit()
        await session.refresh(new_buyer)

        return '201'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при добавлении покупателя")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.put('/buyers/{id}')
async def update_buyer(id: int, buyer_data: BuyerRequest, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Buyer).where(Buyer.id == id))
        buyer = result.scalar_one_or_none()

        if buyer is None:
            raise HTTPException(status_code=404, detail="Покупатель не найден")

        if buyer_data.full_name is not None:
            buyer.full_name = buyer_data.full_name
        if buyer_data.organization_name is not None:
            buyer.organization_name = buyer_data.organization_name
        if buyer_data.phone_number is not None:
            buyer.phone_number = buyer_data.phone_number
        if buyer_data.address is not None:
            buyer.address = buyer_data.address

        await session.commit()
        await session.refresh(buyer)

        return '200'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении покупателя")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.delete('/buyers/{id}')
async def delete_buyer(id: int, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Buyer).where(Buyer.id == id))
        buyer = result.scalar_one_or_none()

        if buyer is None:
            raise HTTPException(status_code=404, detail="Покупатель не найден")

        await session.delete(buyer)
        await session.commit()

        return '204'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при получении покупателя")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")

