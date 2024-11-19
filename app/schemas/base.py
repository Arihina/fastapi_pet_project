from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: int
    product_quantity: int
    total_cost: float
    provider_id: int

    class Config:
        from_attributes = True


class OrderRequest(BaseModel):
    product_quantity: int = None
    total_cost: float = None
    provider_id: int = None


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
    full_name: str
    product_name: str
    phone_number: str
    email: str

    class Config:
        from_attributes = True


class ProviderRequest(BaseModel):
    full_name: str = None
    product_name: str = None
    phone_number: str = None
    email: str = None
