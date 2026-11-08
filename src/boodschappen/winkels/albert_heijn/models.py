from pydantic import BaseModel, Field


class AccessToken(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int


class Page(BaseModel):
    size: int
    totalElements: int
    totalPages: int
    number: int


class Image(BaseModel):
    width: int
    height: int
    url: str


class Product(BaseModel):
    webshopId: int
    hqId: int
    title: str
    images: list[Image]
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


class ShoppingListItems(BaseModel):
    prod_id: int = Field(gt=0, description="Albert Heijn product ID")
    count: int = Field(gt=0, description="Aantal producten")
