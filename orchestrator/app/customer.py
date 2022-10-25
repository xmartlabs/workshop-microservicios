import crud
from models import CustomerSchema
from fastapi import APIRouter, HTTPException
from typing import List 

router = APIRouter()


@router.post("/", response_model=CustomerSchema, status_code=201)
async def create_customer(payload: CustomerSchema):
    await crud.post(payload)

    response_object = {
        "id": payload.id,
        "name": payload.name,
        "address": payload.address,
        "bank_account": payload.bank_account
    }
    return response_object


@router.get("/{id}/", response_model=CustomerSchema)
async def read_customer(id: str):
    customer = await crud.get(id)
    if not customer:
        raise HTTPException(status_code=404, detail="customer not found")
    return customer


@router.get("/", response_model=List[CustomerSchema])
async def read_all_customers():
    return await crud.get_all()


@router.put("/{id}/", response_model=CustomerSchema)
async def update_customer(payload:CustomerSchema, id: str):
    customer = await crud.get(id)
    if not customer:
        raise HTTPException(status_code=404, detail="customer not found")
    customer_id = await crud.put(id, payload)
    response_object = {
        "id": customer_id,
        "name": payload.name,
        "address": payload.address,
        "bank_account": payload.bank_account
    }
    return response_object


@router.delete("/{id}/", response_model=CustomerSchema)
async def delete_customer(id: str):
    customer = await crud.get(id)
    if not customer:
        raise HTTPException(status_code=404, detail="customer not found")
    await crud.delete(id)

    return customer
