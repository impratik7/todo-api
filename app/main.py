from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from datetime import timedelta
from . import crud, models, schemas, auth
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency of database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to To Do Task App"}

# Endpoint to register a new user
@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    # user.password = auth.get_password_hash(user.password)
    return crud.create_user(db=db, user=user)

# Endpoint to authenticate a user and return a JWT token
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
    # if not user or not auth.verify_password(form_data.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
            )   
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint to get all tasks for the authenticated user
@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    username = auth.decode_token(token)
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")
    tasks = db.query(models.Task).filter(models.Task.user_id == user.id).offset(skip).limit(limit).all()
    return tasks

# Endpoint to create a new task for the authenticated user
@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    username = auth.decode_token(token)
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")
    return crud.create_task(db=db, task=task, user_id=user.id)

# Endpoint to update an existing task for the authenticated user
@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    username = auth.decode_token(token)
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")
    db_task = db.query(models.Task).filter(models.Task.id == task.id, models.Task.user_id == user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

# Endpoint to remove an existing task for the authenticated user
@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    username = auth.decode_token(token)
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return db_task

# Endpoint to retrieve a specific task by its ID for the authenticated user
@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    username = auth.decode_token(token)
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
