# Вызываемые функции
import fastapi
import jwt
import sqlalchemy.orm as orm
import passlib.hash as _hash
from fastapi import HTTPException
import fastapi.security as security
import database as database, models as models, schemas as schemas


def create_database():
    return database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_user(user, db: orm.Session):
    user_obj = models.User(
        name=user.name,
        email=user.email,
        password=_hash.bcrypt.hash(user.password)
    )

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    return user_obj


async def get_user_by_id(user_id: int, db: orm.Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return {
        "name": user.name,
        "reviews": user.reviews
    }


async def get_book_by_id(book_id: int, db: orm.Session):
    book = db.query(models.User).filter(models.Book.id == book_id).first()
    return book


async def get_user(name: str, db: orm.Session):
    user = db.query(models.User).filter(models.User.name == name).first()
    return user


async def delete_user_by_id(user_id: int, db: orm.Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"user with id = {user_id} does not exist")
    db.delete(user)
    db.commit()
    return user


async def update_user_by_id(user_id: str, user: models.User, db: orm.Session):
    item = db.query(models.User).filter(models.User.id == user_id).first()
    if item is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"user with id = {user_id} does not exist")

    item.name = user.name
    item.email = user.email

    db.commit()

    return item


async def get_user_by_name(user_name: str, db: orm.Session):
    return db.query(models.User).filter(models.User.name.like(f"%{user_name}%")).all()


async def create_review(review_text: str, user_id: str, db: orm.Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"user with id = {user_id} does not exist")

    review = models.Review(
        review_text=review_text,
        user_id=user_id,
        owner=user
    )
    db.add(review)
    db.commit()

    return review


async def authentificate_user(username: str, password: str, db: orm.Session):
    user = await get_user(username, db)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

# Создание токена
JWT_SECRET = "my"


async def create_token(user: models.User):
    token = jwt.encode(dict(name=user.name, id=user.id, email=user.email), JWT_SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "Bearer", "user_id": user.id}

# Проверка токена
oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/api/get-token")


async def get_current_user(
        db: orm.Session = fastapi.Depends(get_db),
        token: str = fastapi.Depends(oauth2schema)
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithm="HS256")
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(status_code=401, detail="Invalid token")
    return {"name": user.name, "id": user.id}


def create_book(name: str, description: str, file_path: str, db: orm.Session):
    new_book = models.Book(name=name, description=description, file_path=file_path)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    db.close()
    return new_book
