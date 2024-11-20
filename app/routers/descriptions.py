from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Description
from app.models.db_engine import engine
from app.schemas.base import DescriptionResponse, DescriptionRequest

router = APIRouter()

router.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent.parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get('/descriptions', response_model=list[DescriptionResponse])
async def get_descriptions(request: Request, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Description))
    descriptions = result.scalars().all()

    return templates.TemplateResponse('descriptions.html', {"request": request, "lst": descriptions})


@router.get('/descriptions/form')
async def get_description_form(request: Request):
    return templates.TemplateResponse("description_form.html", {"request": request})


@router.get('/descriptions/{id}', response_model=DescriptionResponse)
async def get_description(request: Request, id: int, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Description).where(Description.id == id))
    description = result.scalar_one_or_none()

    if description:
        return templates.TemplateResponse('description_card.html', {"request": request, "d": description})
    else:
        raise HTTPException(status_code=404, detail="Description not found")


@router.post('/descriptions')
async def add_description(description: DescriptionRequest, session: AsyncSession = Depends(engine.get_session)):
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


@router.put('/descriptions/{id}')
async def update_description(id: int, description_data: DescriptionRequest,
                             session: AsyncSession = Depends(engine.get_session)):
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


@router.delete('/descriptions/{id}')
async def delete_description(id: int, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Description).where(Description.id == id))
    description = result.scalar_one_or_none()

    if description is None:
        raise HTTPException(status_code=404, detail="Description not found")

    await session.delete(description)
    await session.commit()

    return '204'
