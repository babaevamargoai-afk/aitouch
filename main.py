from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session
from typing import List
import os, uuid, shutil

import models, schemas, auth, export
from database import engine, get_db, Base

Base.metadata.create_all(bind=engine)

_data_dir = os.environ.get("DATA_DIR", ".")
UPLOAD_DIR = os.path.join(_data_dir, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="AiTouch")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


# ===== AUTH =====

@app.post("/auth/register", response_model=schemas.Token)
def register(body: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == body.username).first():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    user = models.User(username=body.username, password_hash=auth.hash_password(body.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"access_token": auth.create_token(user.id)}


@app.post("/auth/login", response_model=schemas.Token)
def login(body: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == body.username).first()
    if not user or not auth.verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    return {"access_token": auth.create_token(user.id)}


# ===== INCOME =====

@app.get("/income", response_model=List[schemas.IncomeOut])
def list_income(year: int, month: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Income).filter(
        models.Income.user_id == current_user.id,
        models.Income.year == year,
        models.Income.month == month
    ).order_by(models.Income.date.desc()).all()


@app.post("/income", response_model=schemas.IncomeOut)
def create_income(body: schemas.IncomeCreate, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    item = models.Income(**body.model_dump(), user_id=current_user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.patch("/income/{item_id}", response_model=schemas.IncomeOut)
def update_income(item_id: int, body: schemas.IncomeCreate, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    item = db.query(models.Income).filter(
        models.Income.id == item_id, models.Income.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404)
    for k, v in body.model_dump().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item


@app.delete("/income/{item_id}")
def delete_income(item_id: int, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    item = db.query(models.Income).filter(
        models.Income.id == item_id, models.Income.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404)
    db.delete(item)
    db.commit()
    return {"ok": True}


# ===== EXPENSE =====

@app.get("/expense", response_model=List[schemas.ExpenseOut])
def list_expense(year: int, month: int, db: Session = Depends(get_db),
                 current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Expense).filter(
        models.Expense.user_id == current_user.id,
        models.Expense.year == year,
        models.Expense.month == month
    ).order_by(models.Expense.date.desc()).all()


@app.post("/expense", response_model=schemas.ExpenseOut)
def create_expense(body: schemas.ExpenseCreate, db: Session = Depends(get_db),
                   current_user: models.User = Depends(auth.get_current_user)):
    item = models.Expense(**body.model_dump(), user_id=current_user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.patch("/expense/{item_id}", response_model=schemas.ExpenseOut)
def update_expense(item_id: int, body: schemas.ExpenseCreate, db: Session = Depends(get_db),
                   current_user: models.User = Depends(auth.get_current_user)):
    item = db.query(models.Expense).filter(
        models.Expense.id == item_id, models.Expense.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404)
    for k, v in body.model_dump().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item


@app.delete("/expense/{item_id}")
def delete_expense(item_id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(auth.get_current_user)):
    item = db.query(models.Expense).filter(
        models.Expense.id == item_id, models.Expense.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404)
    db.delete(item)
    db.commit()
    return {"ok": True}


# ===== POTENTIAL INCOME =====

@app.get("/potential", response_model=List[schemas.PotentialOut])
def list_potential(year: int, month: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.PotentialIncome).filter(
        models.PotentialIncome.user_id == current_user.id,
        models.PotentialIncome.year == year,
        models.PotentialIncome.month == month
    ).order_by(models.PotentialIncome.date.desc()).all()

@app.post("/potential", response_model=schemas.PotentialOut)
def create_potential(body: schemas.PotentialCreate, db: Session = Depends(get_db),
                     current_user: models.User = Depends(auth.get_current_user)):
    item = models.PotentialIncome(**body.model_dump(), user_id=current_user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.delete("/potential/{item_id}")
def delete_potential(item_id: int, db: Session = Depends(get_db),
                     current_user: models.User = Depends(auth.get_current_user)):
    item = db.query(models.PotentialIncome).filter(
        models.PotentialIncome.id == item_id,
        models.PotentialIncome.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404)
    db.delete(item)
    db.commit()
    return {"ok": True}


# ===== FILE UPLOAD =====

@app.post("/upload/contract")
async def upload_contract(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user)
):
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": filename, "original": file.filename}


@app.get("/upload/contract/{filename}")
async def download_contract(
    filename: str,
    current_user: models.User = Depends(auth.get_current_user)
):
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404)
    return FileResponse(path, filename=filename)


# ===== CLIENTS =====

@app.get("/clients", response_model=List[schemas.ClientOut])
def list_clients(db: Session = Depends(get_db),
                 current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Client).filter(models.Client.user_id == current_user.id).all()


@app.post("/clients", response_model=schemas.ClientOut)
def create_client(body: schemas.ClientCreate, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    item = models.Client(**body.model_dump(), user_id=current_user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.delete("/clients/{item_id}")
def delete_client(item_id: int, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    item = db.query(models.Client).filter(
        models.Client.id == item_id, models.Client.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404)
    db.delete(item)
    db.commit()
    return {"ok": True}


# ===== CLIENT TASKS =====

def _get_client(client_id: int, user_id: int, db: Session):
    c = db.query(models.Client).filter(
        models.Client.id == client_id, models.Client.user_id == user_id).first()
    if not c:
        raise HTTPException(status_code=404)
    return c

@app.get("/clients/{client_id}/tasks", response_model=List[schemas.ClientTaskOut])
def get_tasks(client_id: int, db: Session = Depends(get_db),
              current_user: models.User = Depends(auth.get_current_user)):
    _get_client(client_id, current_user.id, db)
    return db.query(models.ClientTask).filter(
        models.ClientTask.client_id == client_id
    ).order_by(models.ClientTask.order).all()

@app.post("/clients/{client_id}/tasks/bulk")
def bulk_create_tasks(client_id: int, body: List[schemas.ClientTaskCreate],
                      db: Session = Depends(get_db),
                      current_user: models.User = Depends(auth.get_current_user)):
    _get_client(client_id, current_user.id, db)
    for t in body:
        db.add(models.ClientTask(client_id=client_id, user_id=current_user.id,
                                  text=t.text, order=t.order))
    db.commit()
    return {"ok": True}

@app.patch("/clients/{client_id}/tasks/{task_id}", response_model=schemas.ClientTaskOut)
def update_task(client_id: int, task_id: int, body: schemas.ClientTaskUpdate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    task = db.query(models.ClientTask).filter(
        models.ClientTask.id == task_id,
        models.ClientTask.client_id == client_id,
        models.ClientTask.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404)
    data = body.model_dump(exclude_none=True)
    for k, v in data.items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task

@app.delete("/clients/{client_id}/tasks/{task_id}")
def delete_task(client_id: int, task_id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    task = db.query(models.ClientTask).filter(
        models.ClientTask.id == task_id,
        models.ClientTask.client_id == client_id,
        models.ClientTask.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404)
    db.delete(task)
    db.commit()
    return {"ok": True}


# ===== CLIENT COMMENTS =====

@app.get("/clients/{client_id}/comments", response_model=List[schemas.ClientCommentOut])
def get_comments(client_id: int, db: Session = Depends(get_db),
                 current_user: models.User = Depends(auth.get_current_user)):
    _get_client(client_id, current_user.id, db)
    rows = db.query(models.ClientComment).filter(
        models.ClientComment.client_id == client_id
    ).order_by(models.ClientComment.created_at.desc()).all()
    result = []
    for r in rows:
        result.append(schemas.ClientCommentOut(
            id=r.id, text=r.text,
            created_at=r.created_at.strftime('%d.%m.%Y %H:%M')
        ))
    return result

@app.post("/clients/{client_id}/comments", response_model=schemas.ClientCommentOut)
def add_comment(client_id: int, body: schemas.ClientCommentCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    _get_client(client_id, current_user.id, db)
    from datetime import datetime
    item = models.ClientComment(client_id=client_id, user_id=current_user.id,
                                 text=body.text, created_at=datetime.utcnow())
    db.add(item)
    db.commit()
    db.refresh(item)
    return schemas.ClientCommentOut(id=item.id, text=item.text,
                                     created_at=item.created_at.strftime('%d.%m.%Y %H:%M'))

@app.delete("/clients/{client_id}/comments/{comment_id}")
def delete_comment(client_id: int, comment_id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(auth.get_current_user)):
    item = db.query(models.ClientComment).filter(
        models.ClientComment.id == comment_id,
        models.ClientComment.client_id == client_id,
        models.ClientComment.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404)
    db.delete(item)
    db.commit()
    return {"ok": True}


# ===== STREAMS =====

@app.get("/streams", response_model=List[schemas.StreamOut])
def list_streams(db: Session = Depends(get_db),
                 current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Stream).filter(models.Stream.user_id == current_user.id).all()


@app.post("/streams", response_model=schemas.StreamOut)
def create_stream(body: schemas.StreamCreate, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    item = models.Stream(**body.model_dump(), user_id=current_user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.patch("/streams/{item_id}", response_model=schemas.StreamOut)
def update_stream(item_id: int, body: schemas.StreamCreate, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    item = db.query(models.Stream).filter(
        models.Stream.id == item_id, models.Stream.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404)
    for k, v in body.model_dump().items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item


@app.delete("/streams/{item_id}")
def delete_stream(item_id: int, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    item = db.query(models.Stream).filter(
        models.Stream.id == item_id, models.Stream.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404)
    db.delete(item)
    db.commit()
    return {"ok": True}


# ===== ANALYTICS =====

@app.get("/analytics/monthly")
def monthly_analytics(months: int = 6, db: Session = Depends(get_db),
                       current_user: models.User = Depends(auth.get_current_user)):
    from datetime import date
    today = date.today()
    result = []
    y, m = today.year, today.month
    for _ in range(months):
        incomes = db.query(models.Income).filter(
            models.Income.user_id == current_user.id,
            models.Income.year == y, models.Income.month == m).all()
        expenses = db.query(models.Expense).filter(
            models.Expense.user_id == current_user.id,
            models.Expense.year == y, models.Expense.month == m).all()
        total_inc = sum(i.amount for i in incomes)
        total_exp = sum(e.amount for e in expenses)
        result.append({"year": y, "month": m, "income": total_inc,
                        "expense": total_exp, "profit": total_inc - total_exp})
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    result.reverse()
    return result


# ===== EXPORT =====

@app.get("/export/excel")
def export_excel(year: int, month: int, db: Session = Depends(get_db),
                 current_user: models.User = Depends(auth.get_current_user)):
    incomes = db.query(models.Income).filter(
        models.Income.user_id == current_user.id,
        models.Income.year == year, models.Income.month == month).all()
    expenses = db.query(models.Expense).filter(
        models.Expense.user_id == current_user.id,
        models.Expense.year == year, models.Expense.month == month).all()
    clients = db.query(models.Client).filter(models.Client.user_id == current_user.id).all()
    streams = db.query(models.Stream).filter(models.Stream.user_id == current_user.id).all()
    data = export.build_excel(incomes, expenses, clients, streams, year, month)
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=aitouch_{year}_{month+1:02d}.xlsx"}
    )


@app.get("/export/csv")
def export_csv(year: int, month: int, db: Session = Depends(get_db),
               current_user: models.User = Depends(auth.get_current_user)):
    incomes = db.query(models.Income).filter(
        models.Income.user_id == current_user.id,
        models.Income.year == year, models.Income.month == month).all()
    expenses = db.query(models.Expense).filter(
        models.Expense.user_id == current_user.id,
        models.Expense.year == year, models.Expense.month == month).all()
    data = export.build_csv_finance(incomes, expenses)
    return Response(
        content=data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=aitouch_{year}_{month+1:02d}.csv"}
    )
