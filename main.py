from auth import BasicAuthBackend, OktaJWTMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.api import api_router
from settings import ALLOW_CREDENTIALS, ALLOW_HEADERS, ALLOW_METHODS, CORS_ORIGINS, STATIC_FILES, STATIC_URL
from starlette.config import Config
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.mount(STATIC_URL, STATIC_FILES, name="static")

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)

app.add_middleware(SessionMiddleware, secret_key="sessionkey")
app.add_middleware(OktaJWTMiddleware)
app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())


config = Config(".env")
