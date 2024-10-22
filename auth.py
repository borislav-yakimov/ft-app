import requests
from fastapi import Request
from models import User
from okta_jwt_verifier import AccessTokenVerifier
from routers.paths import OktaPath, Path
from settings import OKTA_AUDIENCE, OKTA_ISSUER_URI, OKTA_ORG_URL
from starlette.authentication import AuthCredentials, AuthenticationBackend
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        accessToken = request.cookies.get("access_token", None)
        if accessToken is not None:
            try:
                jwt_verifier = AccessTokenVerifier(issuer=OKTA_ISSUER_URI, audience=OKTA_AUDIENCE)
                await jwt_verifier.verify(accessToken)
                userinfo_response = requests.get(
                    OKTA_ORG_URL + OktaPath.user_info, headers={"Authorization": f"Bearer {accessToken}"}
                ).json()
                userinfo_response.pop("sub", None)

                return AuthCredentials(["authenticated"]), User(**userinfo_response)
            except Exception as e:
                # return JSONResponse({"error": f"Unauthorized token or {e}"}, status_code=401)
                # return RedirectResponse(url=Path.login)
                return None

        return None


class OktaJWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if (
            ("user" in request.scope and request.user.is_authenticated)
            or request.url.path == Path.login
            or request.url.path == Path.authorization_code_callback
        ):
            return await call_next(request)

        return RedirectResponse(url=Path.login)
