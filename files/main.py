import os.path

import fastapi as fastapi
import uvicorn
from fastapi.openapi.utils import get_openapi
from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import fastapi.security as security
import sqlalchemy.orm as orm
import services as services, schemas as schemas
from typing import Annotated

app = fastapi.FastAPI()


openapi_schema = get_openapi(
    title="My app",
    version="1.0.0",
    routes=app.routes
)


@app.get("/api")
async def root():
    return {"message": "Hello World! This server is up!"}


@app.post("/api/user")
async def create_user(user: schemas.UserBase, db: orm.Session = fastapi.Depends(services.get_db)):
    user = await services.create_user(user, db)
    return user


@app.get("/api/users/me")
async def get_current_user(user: schemas.User = fastapi.Depends(services.get_current_user)):
    return user


@app.get("/api/users/{user_id}")
async def get_user_by_id(user_id: int, db: orm.Session = fastapi.Depends(services.get_db)):
    user = await services.get_user_by_id(user_id, db)
    return user


@app.delete("/api/users/{user_id}")
async def delete_user_by_id(user_id: int, db: orm.Session = fastapi.Depends(services.get_db)):
    user = await services.delete_user_by_id(user_id, db)
    return user


@app.put("/api/users/{user_id}")
async def get_user_by_id(user_id: str, user: schemas.UserBase, db: orm.Session = fastapi.Depends(services.get_db)):
    user = await services.update_user_by_id(user_id, user, db)
    return user


@app.post("/api/users")
async def get_user_by_name(name: str | None = None, db: orm.Session = fastapi.Depends(services.get_db)):
    user = await services.get_user_by_name(name, db)
    return user


@app.post("/api/review")
async def create_rewiew(review: schemas.ReviewBase, db: orm.Session = fastapi.Depends(services.get_db), user: schemas.UserBase = fastapi.Depends(services.get_current_user)):
    review = await services.create_review(review.review_text, review.user_id, db)
    if user["id"] != review.user_id:
        raise fastapi.HTTPException(status_code=401, detail="Invalid access")
    return review


@app.post("/api/get-token")
async def generate_token(
    form_data: security.OAuth2PasswordRequestForm = fastapi.Depends(),
    db: orm.Session = fastapi.Depends(services.get_db)
):
    user = await services.authentificate_user(form_data.username, form_data.password, db)
    if not user:
        raise fastapi.HTTPException(status_code=401, detail="Wrong username or password")
    return await services.create_token(user)


@app.post("/upload-book/")
async def upload_book(file: Annotated[UploadFile, File(description="A file read as UploadFile")],name: str, description: str, db: orm.Session = fastapi.Depends(services.get_db)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    book = services.create_book(name=name, description=description, file_path=file_path, db=db)
    return book


@app.get("/api/get-book/{book_id}")
async def get_book_by_id(book_id: int, db: orm.Session = fastapi.Depends(services.get_db)):
    book = await services.get_book_by_id(book_id, db)
    return book


@app.get("/api/files/{file_path}")
async def read_file(file_path: str):
    full_path = f"uploads/{file_path}"
    if not os.path.exists(full_path):
        raise fastapi.HTTPException(status_code=404, detail="File not found")
    return FileResponse(full_path)
# 13 минута, лекция 9.1, открывать файл с фронтендом


app.mount("/", StaticFiles(directory=Path("frontend"), html=True))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")

