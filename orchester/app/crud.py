from models import CustomerSchema
from db import customer, database


async def post(payload: CustomerSchema):
    query = customer.insert().values(id=payload.id, name=payload.name, address=payload.address)

    return await database.execute(query=query)

async def get(id: int):
    query = customer.select().where(id == customer.c.id)
    return await database.fetch_one(query=query)
    

async def get_all():
    query = customer.select()
    return await database.fetch_all(query=query)


async def put(id:int, payload=CustomerSchema):
    query = (
        customer.update().where(id == customer.c.id).values(name=payload.name, address=payload.address)
        .returning(customer.c.id)
    )
    return await database.execute(query=query)


async def delete(id:int):
    query = customer.delete().where(id == customer.c.id)
    return await database.execute(query=query)
