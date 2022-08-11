from pydantic import BaseModel, Field


class CustomerSchema(BaseModel):
    id: str = Field(..., min_length=36, max_length=36)
    name: str = Field(..., min_length=3, max_length=50) 
    address: str = Field(..., min_length=3, max_length=150)
