from pydantic import BaseModel, Field, ValidationError, validator


class CustomerSchema(BaseModel):
    id: str = Field(..., min_length=36, max_length=36)
    name: str = Field(..., min_length=3, max_length=50) 
    address: str = Field(..., min_length=3, max_length=150)
    bank_account: str


class AmountPayload(BaseModel):
    amount: float

    @validator('amount')
    def positive_number(cls, value):
        if not value > 0:
            raise ValueError("Must be a positive amount")
        return value