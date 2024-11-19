from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Buyer
from app.models.db_engine import engine
from app.schemas.base import BuyerResponse, BuyerRequest

router = APIRouter()


@router.get('/buyers', response_model=list[BuyerResponse])
async def get_buyers(session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Buyer))
    buyers = result.scalars().all()

    return buyers


@router.get('/buyers/{id}', response_model=BuyerResponse)
async def get_buyer(id: int, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Buyer).where(Buyer.id == id))
    buyer = result.scalar_one_or_none()

    if buyer:
        return buyer
    else:
        raise HTTPException(status_code=404, detail="Buyer not found")


@router.post('/buyers')
async def add_buyer(buyer: BuyerRequest, session: AsyncSession = Depends(engine.get_session)):
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


@router.put('/buyers/{id}')
async def update_buyer(id: int, buyer_data: BuyerRequest, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Buyer).where(Buyer.id == id))
    buyer = result.scalar_one_or_none()

    if buyer is None:
        raise HTTPException(status_code=404, detail="Buyer not found")

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


@router.delete('/buyers/{id}')
async def delete_buyer(id: int, session: AsyncSession = Depends(engine.get_session)):
    result = await session.execute(select(Buyer).where(Buyer.id == id))
    buyer = result.scalar_one_or_none()

    if buyer is None:
        raise HTTPException(status_code=404, detail="Buyer not found")

    await session.delete(buyer)
    await session.commit()

    return '204'

