from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from datetime import datetime
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# ─── Database Setup ───────────────────────────────────────────────────────────
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/tododb"
    APP_NAME: str = "Todos App"
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# ─── Model ────────────────────────────────────────────────────────────────────
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


# ─── App & Templates ──────────────────────────────────────────────────────────
app = FastAPI(title=settings.APP_NAME)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ─── Dependency ───────────────────────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
async def index(request: Request, db: Session = Depends(get_db)):
    todos = db.query(Todo).order_by(Todo.created_at.desc()).all()
    total = len(todos)
    completed = sum(1 for t in todos if t.completed)
    pending = total - completed
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": todos,
        "total": total,
        "completed": completed,
        "pending": pending,
    })


@app.post("/add")
async def add_todo(
    title: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db)
):
    if not title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    todo = Todo(title=title.strip(), description=description.strip())
    db.add(todo)
    db.commit()
    return RedirectResponse("/", status_code=303)


@app.post("/toggle/{todo_id}")
async def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = not todo.completed
    db.commit()
    return RedirectResponse("/", status_code=303)


@app.post("/delete/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return RedirectResponse("/", status_code=303)


@app.get("/edit/{todo_id}")
async def edit_page(todo_id: int, request: Request, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return templates.TemplateResponse("edit.html", {"request": request, "todo": todo})


@app.post("/edit/{todo_id}")
async def edit_todo(
    todo_id: int,
    title: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = title.strip()
    todo.description = description.strip()
    db.commit()
    return RedirectResponse("/", status_code=303)


@app.post("/delete-completed")
async def delete_completed(db: Session = Depends(get_db)):
    db.query(Todo).filter(Todo.completed == True).delete()
    db.commit()
    return RedirectResponse("/", status_code=303)
