from sqlalchemy.orm import Session
from . import models, schemas
from .utils import hash_password

def create_user(db: Session, user: schemas.UserCreate):
    hashed = hash_password(user.password)

    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user