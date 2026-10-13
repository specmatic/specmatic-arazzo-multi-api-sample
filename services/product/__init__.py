from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from common.database import Database


def get_session():
    with Session(Database().engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

from .schema import graphql_router  # noqa: E402
app.include_router(graphql_router, prefix="/graphql")
