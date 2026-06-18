from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class IncomeCreate(BaseModel):
    date: str
    amount: float = 0
    source: str = ""
    desc: str = ""
    tag: str = "other"
    year: int
    month: int


class IncomeOut(IncomeCreate):
    id: int
    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    date: str
    amount: float = 0
    name: str = ""
    category: str = "other"
    desc: str = ""
    year: int
    month: int


class ExpenseOut(ExpenseCreate):
    id: int
    class Config:
        from_attributes = True


class PotentialCreate(BaseModel):
    date: str
    amount: float = 0
    source: str = ""
    desc: str = ""
    tag: str = "other"
    year: int
    month: int

class PotentialOut(PotentialCreate):
    id: int
    class Config:
        from_attributes = True

class ClientCreate(BaseModel):
    name: str = ""
    type: str = "tracking"
    start: str = ""
    end: str = ""
    amount: float = 0
    status: str = "active"
    tasks: str = ""
    chat: str = ""
    canvas: str = ""
    notes: str = ""
    contract_file: str = ""
    manager: str = ""


class ClientOut(ClientCreate):
    id: int
    class Config:
        from_attributes = True


class ClientTaskCreate(BaseModel):
    text: str
    order: int = 0
    is_header: bool = False

class ClientTaskUpdate(BaseModel):
    done: Optional[bool] = None
    delivered: Optional[bool] = None
    verified: Optional[bool] = None
    is_header: Optional[bool] = None
    text: Optional[str] = None
    order: Optional[int] = None

class ClientTaskOut(BaseModel):
    id: int
    text: str
    done: bool
    delivered: bool
    verified: bool = False
    is_header: bool = False
    order: int
    class Config:
        from_attributes = True

class ClientCommentCreate(BaseModel):
    text: str

class ClientCommentOut(BaseModel):
    id: int
    text: str
    created_at: str
    class Config:
        from_attributes = True

class StaffCostCreate(BaseModel):
    name: str = ""
    desc: str = ""
    amount: float = 0
    date: str = ""

class StaffCostOut(StaffCostCreate):
    id: int
    class Config:
        from_attributes = True

class StreamCreate(BaseModel):
    course: str = ""
    name: str = ""
    start: str = ""
    t1: int = 0
    t2: int = 0
    t3: int = 0
    p1: float = 0
    p2: float = 0
    p3: float = 0
    managers: str = ""
    notes: str = ""


class StreamOut(StreamCreate):
    id: int
    class Config:
        from_attributes = True
