from datetime import datetime
from enum import Enum
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel, Field

# pip install sqlalchemy alembic psycopg2
# uvicorn main:app --reload

app = FastAPI(
    title="Trading APP"
)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

fake_users = [
    {"id": 1, "role": "admin", "name": "sah"},
    {"id": 2, "role": "investor", "name": "mot"},
    {"id": 3, "role": "trader", "name": "il", "degree": [
        {"id": 1, "create_at": "2020-01-01T00:00:00", "type_degree": "expert"}
    ]},
]


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"

class Degree(BaseModel):
    id: int
    create_at: datetime
    type_degree: DegreeType

class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []

@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


fake_trades= [
    {"id": 1, "user_id": 1, "currency": "BTR", "side": "buy", "price": 100, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTR", "side": "buy", "price": 220, "amount": 2.12},

]

class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float

@app.post("/trades")
def add_trade(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}