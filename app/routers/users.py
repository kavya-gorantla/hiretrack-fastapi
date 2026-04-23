from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .. import crud, schemas, models, database
from ..utils import verify_password
from ..auth import create_access_token, verify_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE USER
@router.post("/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


# LOGIN
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token}


# 🔐 PROTECTED ROUTE
@router.get("/secure")
def secure_data(token: str = Depends(oauth2_scheme)):
    verify_token(token)
    return {"message": "You are authorized"}