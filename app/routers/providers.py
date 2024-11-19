from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Provider
from app.models.db_engine import engine
from app.schemas.base import ProviderResponse, ProviderRequest

router = APIRouter()


@router.get('/providers', response_model=list[ProviderResponse])
async def get_providers(session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Provider))
    providers = result.scalars().all()

    return providers


@router.get('/providers/{id}', response_model=ProviderResponse)
async def get_provider(id: int, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Provider).where(Provider.id == id))
    provider = result.scalar_one_or_none()

    if provider:
        return provider
    else:
        raise HTTPException(status_code=404, detail="Provider not found")


@router.post('/providers')
async def add_provider(provider: ProviderRequest, session: AsyncSession = Depends(engine.get_session)):
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


@router.put('/providers/{id}')
async def update_provider(id: int, provider_data: ProviderRequest,
                          session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Provider).where(Provider.id == id))
    provider = result.scalar_one_or_none()

    if provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")

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


@router.delete('/providers/{id}')
async def delete_provider(id: int, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Provider).where(Provider.id == id))
    provider = result.scalar_one_or_none()

    if provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")

    await session.delete(provider)
    await session.commit()

    return '204'
