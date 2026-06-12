from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Boolean, DateTime
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)


class Income(Base):
    __tablename__ = "incomes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(String)
    amount = Column(Float, default=0)
    source = Column(String, default="")
    desc = Column(Text, default="")
    tag = Column(String, default="other")
    year = Column(Integer)
    month = Column(Integer)


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(String)
    amount = Column(Float, default=0)
    name = Column(String, default="")
    category = Column(String, default="other")
    desc = Column(Text, default="")
    year = Column(Integer)
    month = Column(Integer)


class PotentialIncome(Base):
    __tablename__ = "potential_incomes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(String)
    amount = Column(Float, default=0)
    source = Column(String, default="")
    desc = Column(Text, default="")
    tag = Column(String, default="other")
    year = Column(Integer)
    month = Column(Integer)


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, default="")
    type = Column(String, default="tracking")
    start = Column(String, default="")
    end = Column(String, default="")
    amount = Column(Float, default=0)
    status = Column(String, default="active")
    tasks = Column(Text, default="")
    chat = Column(String, default="")
    canvas = Column(String, default="")
    notes = Column(Text, default="")
    contract_file = Column(String, default="")


class ClientTask(Base):
    __tablename__ = "client_tasks"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(Text, default="")
    done = Column(Boolean, default=False)
    delivered = Column(Boolean, default=False)
    order = Column(Integer, default=0)


class ClientComment(Base):
    __tablename__ = "client_comments"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class Stream(Base):
    __tablename__ = "streams"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course = Column(String, default="")   # название курса: X5, и т.д.
    name = Column(String, default="")     # название потока: Поток 1, Поток 2
    start = Column(String, default="")
    t1 = Column(Integer, default=0)       # Стандарт
    t2 = Column(Integer, default=0)       # Бизнес
    t3 = Column(Integer, default=0)       # Мастер-группа (учитывается в клиентах)
    p1 = Column(Float, default=0)
    p2 = Column(Float, default=0)
    p3 = Column(Float, default=0)
    managers = Column(Text, default="")
    notes = Column(Text, default="")
