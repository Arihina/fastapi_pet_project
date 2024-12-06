import datetime

from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: int
    product_quantity: int
    total_cost: float
    product_id: int

    class Config:
        from_attributes = True


class OrderRequest(BaseModel):
    product_quantity: int = None
    total_cost: float = None
    product_id: int = None


class DescriptionResponse(BaseModel):
    id: int
    furniture_type: str
    material: str
    weight: int
    dimensions: str

    class Config:
        from_attributes = True


class DescriptionRequest(BaseModel):
    furniture_type: str = None
    material: str = None
    weight: int = None
    dimensions: str = None


class BuyerResponse(BaseModel):
    id: int
    full_name: str
    organization_name: str
    phone_number: str
    address: str

    class Config:
        from_attributes = True


class BuyerRequest(BaseModel):
    full_name: str = None
    organization_name: str = None
    phone_number: str = None
    address: str = None


class ProviderResponse(BaseModel):
    id: int
    organization_name: str
    phone_number: str
    email: str

    class Config:
        from_attributes = True


class ProviderRequest(BaseModel):
    organization_name: str = None
    phone_number: str = None
    email: str = None


class ProductResponse(BaseModel):
    id: int
    price: float
    stock: int
    provider_id: int
    description_id: int

    class Config:
        from_attributes = True


class ProductRequest(BaseModel):
    price: float = None
    stock: int = None
    provider_id: int = None
    description_id: int = None


class SalesRecordResponse(BaseModel):
    id: int
    date: datetime.datetime
    order_id: int
    buyer_id: int

    class Config:
        from_attributes = True


class SalesRecordRequest(BaseModel):
    date: datetime.datetime = None
    order_id: int = None
    buyer_id: int = None


class StockRecordResponse(BaseModel):
    id: int
    date: datetime.datetime
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class StockRecordRequest(BaseModel):
    date: datetime.datetime = None
    product_id: int = None
    quantity: int = None


class ProductInfo(BaseModel):
    id: int
    price: float
    count: int
    dimensions: str
    furniture_type: str
    weight: int
    material: str

    class Config:
        from_attributes = True


class SaleInfo(BaseModel):
    price: float
    count: int
    order_id: int
    date: datetime.datetime

    class Config:
        from_attributes = True


class BuyerInfo(BaseModel):
    date: datetime.datetime
    full_name: str
    organization_name: str
    phone_number: str
    address: str
    product_id: int

    class Config:
        from_attributes = True


class OrderInfo(BaseModel):
    id: int
    product_quantity: int
    total_cost: float
    full_name: str
    product_name: str
    phone_number: str
    email: str

    class Config:
        from_attributes = True


class ProductData(BaseModel):
    id: int
    price: float | None = None
    count: int | None = None
    order_id: int | None = None
    description_id: int | None = None
