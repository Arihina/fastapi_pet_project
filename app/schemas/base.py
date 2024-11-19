from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: int
    product_quantity: int
    total_cost: float
    provider_id: int

    class Config:
        from_attributes = True
