from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int


class Page(BaseModel):
    size: int
    totalElements: int
    totalPages: int
    number: int


class Product(BaseModel):
    webshopId: int
    hqId: int
    title: str
    salesUnitSize: str
    unitPriceDescription: str | None = None
    mainCategory: str
    subCategory: str
    brand: str
    descriptionFull: str
    bonusStartDate: str | None = None
    bonusEndDate: str | None = None
    currentPrice: float | None = None
    priceBeforeBonus: float | None = None


class SearchProducts(BaseModel):
    products: list[Product]
    page: Page
