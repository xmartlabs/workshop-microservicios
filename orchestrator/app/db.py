import os

from sqlalchemy import (Column, DateTime, Integer, String, Table, create_engine, MetaData)
from sqlalchemy.sql import func
from databases import Database

# Database url if none is passed the default one is used
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
customer = Table(
    "customer",
    metadata,
    Column("id", String(36), primary_key=True, autoincrement=False),
    Column("name", String(50)),
    Column("address", String(50)),
    Column("bank_account", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False)
)
# Databases query builder

database = Database(DATABASE_URL)
