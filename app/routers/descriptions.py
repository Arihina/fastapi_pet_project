from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Description
from app.models.db_engine import engine
from app.schemas.base import DescriptionResponse, DescriptionRequest

router = APIRouter()

router.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent.parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get('/descriptions', response_model=list[DescriptionResponse])
async def get_descriptions(request: Request, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Description))
        descriptions = result.scalars().all()

        return templates.TemplateResponse('descriptions.html', {"request": request, "lst": descriptions})
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при получении описаний")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.get('/descriptions/form')
async def get_description_form(request: Request):
    return templates.TemplateResponse("description_form.html", {"request": request})


@router.get('/descriptions/{id}', response_model=DescriptionResponse)
async def get_description(request: Request, id: int, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Description).where(Description.id == id))
        description = result.scalar_one_or_none()

        if description:
            return templates.TemplateResponse('description_card.html', {"request": request, "d": description})
        else:
            raise HTTPException(status_code=404, detail="Описание не найдено")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при получении описания")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.post('/descriptions')
async def add_description(description: DescriptionRequest, session: AsyncSession = Depends(engine.get_session)):
    try:
        new_description = Description(
            furniture_type=description.furniture_type,
            material=description.material,
            weight=description.weight,
            dimensions=description.dimensions
        )

        session.add(new_description)
        await session.commit()
        await session.refresh(new_description)

        return '201'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при добавлении описания")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.put('/descriptions/{id}')
async def update_description(id: int, description_data: DescriptionRequest,
                             session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Description).where(Description.id == id))
        description = result.scalar_one_or_none()

        if description is None:
            raise HTTPException(status_code=404, detail="Description not found")

        if description_data.furniture_type is not None:
            description.furniture_type = description_data.furniture_type
        if description_data.material is not None:
            description.material = description_data.material
        if description_data.weight is not None:
            description.weight = description_data.weight
        if description_data.dimensions is not None:
            description.dimensions = description_data.dimensions

        await session.commit()
        await session.refresh(description)

        return '200'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении описания")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.delete('/descriptions/{id}')
async def delete_description(id: int, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Description).where(Description.id == id))
        description = result.scalar_one_or_none()

        if description is None:
            raise HTTPException(status_code=404, detail="Description not found")

        await session.delete(description)
        await session.commit()

        return '204'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при удалении описания")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.get('/descriptions-filtered')
async def filter_descriptions(request: Request, furniture_type: str, session: AsyncSession = Depends(engine.get_session)):
    try:
        descriptions = await session.execute(select(Description).where(Description.furniture_type == furniture_type))
        descriptions = descriptions.scalars().all()

        return templates.TemplateResponse('descriptions_filter.html', {"request": request, "lst": descriptions})
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при получении покупателей")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")
