from decouple import config
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager
from h11 import CLIENT

CORS_ORIGINS = config("CORS_ORIGINS").split(",")
ALLOW_METHODS = ["*"]
ALLOW_HEADERS = ["*"]
ALLOW_CREDENTIALS = True

TEMPLATES_DIR = "templates"


class CustomJinja2Templates(Jinja2Templates):
    def get_template(self, name: str):
        if not name.endswith(".jinja"):
            name += ".jinja"
        return super().get_template(name)


templates = CustomJinja2Templates(directory=TEMPLATES_DIR)

STATIC_URL = "/static"
STATIC_FILES = StaticFiles(directory="static")

OKTA_CLIENT_ID = config("OKTA_CLIENT_ID")
OKTA_CLIENT_SECRET = config("OKTA_CLIENT_SECRET")
OKTA_ORG_URL = config("OKTA_ORG_URL")
OKTA_REDIRECT_URI = config("OKTA_REDIRECT_URI")
OKTA_ISSUER_URI = config("OKTA_ISSUER_URI")
OKTA_AUDIENCE = config("OKTA_AUDIENCE")

SECRET = "your-secret-key"
manager = LoginManager(SECRET, token_url="/auth/token")
fake_db = {"johndoe@e.mail": {"password": "hunter2"}}
