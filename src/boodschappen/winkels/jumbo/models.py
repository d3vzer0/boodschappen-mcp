from pydantic import BaseModel, Field


class PricePerUnit(BaseModel):
    price: int = Field(ge=0, description="Prijs per eenheid in cent")
    unit: str


class Price(BaseModel):
    price: int = Field(ge=0, description="Normale prijs in cent")
    promoPrice: int | None = Field(default=None, ge=0, description="Actieprijs in cent")
    pricePerUnit: PricePerUnit | None = None


class Availability(BaseModel):
    isAvailable: bool


class Product(BaseModel):
    id: str
    title: str
    brand: str | None = None
    category: str | None = None
    subtitle: str | None = Field(default=None, description="Verpakkingsgrootte")
    image: str | None = None
    link: str
    price: Price | None = None
    availability: Availability | None = None


class SearchProducts(BaseModel):
    products: list[Product]
    start: int = Field(ge=0)
    count: int = Field(ge=0, description="Totaal aantal zoekresultaten")


class ShoppingListItem(BaseModel):
    sku: str = Field(min_length=1, description="Jumbo product ID")
    quantity: int = Field(gt=0, description="Aantal producten")
