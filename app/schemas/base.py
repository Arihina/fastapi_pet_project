from pydantic import BaseModel


class OrderResponse(BaseModel):
    order_id: int
    product_quantity: int
    total_cost: float
    supplier_id: int

    class Config:
        from_attributes = True
