from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Provider
from app.models.db_engine import engine
from app.schemas.base import ProviderResponse, ProviderRequest

router = APIRouter()

router.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent.parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get('/providers', response_model=list[ProviderResponse])
async def get_providers(request: Request, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Provider))
        providers = result.scalars().all()

        return templates.TemplateResponse('providers.html', {"request": request, "lst": providers})
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при получении постващиков")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.get('/providers/form')
async def get_provider_form(request: Request):
    return templates.TemplateResponse("provider_form.html", {"request": request})


@router.get('/providers/{id}', response_model=ProviderResponse)
async def get_provider(request: Request, id: int, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Provider).where(Provider.id == id))
        provider = result.scalar_one_or_none()

        if provider:
            return templates.TemplateResponse('provider_card.html', {"request": request, "pr": provider})
        else:
            raise HTTPException(status_code=404, detail="Поставщик не найден")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при получении поставщика")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.post('/providers')
async def add_provider(provider: ProviderRequest, session: AsyncSession = Depends(engine.get_session)):
    try:
        new_provider = Provider(
            full_name=provider.full_name,
            product_name=provider.product_name,
            phone_number=provider.phone_number,
            email=provider.email
        )

        session.add(new_provider)
        await session.commit()
        await session.refresh(new_provider)

        return '201'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при добавлении поставщика")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.put('/providers/{id}')
async def update_provider(id: int, provider_data: ProviderRequest,
                          session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Provider).where(Provider.id == id))
        provider = result.scalar_one_or_none()

        if provider is None:
            raise HTTPException(status_code=404, detail="Поставщик не найден")

        if provider_data.full_name is not None:
            provider.full_name = provider_data.full_name
        if provider_data.product_name is not None:
            provider.product_name = provider_data.product_name
        if provider_data.phone_number is not None:
            provider.phone_number = provider_data.phone_number
        if provider_data.email is not None:
            provider.email = provider_data.email

        await session.commit()
        await session.refresh(provider)

        return '200'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении поставщика")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")


@router.delete('/providers/{id}')
async def delete_provider(id: int, session: AsyncSession = Depends(engine.get_session)):
    try:
        result = await session.execute(select(Provider).where(Provider.id == id))
        provider = result.scalar_one_or_none()

        if provider is None:
            raise HTTPException(status_code=404, detail="Поставщик не найден")

        await session.delete(provider)
        await session.commit()

        return '204'
    except SQLAlchemyError as error:
        raise HTTPException(status_code=500, detail="Ошибка при удалении поставщика")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Ошибка при обработке запроса, попробуйте позже")

