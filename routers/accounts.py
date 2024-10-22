# @router.get("/signout")
# async def signout(request: Request):
#     request.session.clear()
#     id_token = request.cookies.get("access_token")  # Assuming the ID token is stored in a cookie

#     if not id_token:
#         # Handle the case where the ID token is not available
#         return RedirectResponse(url=Path.login)

#     # Construct the Okta logout URL
#     okta_logout_url = (
#         f"https://dev-08417400.okta.com/oauth2/v1/logout"
#         f"?id_token_hint={id_token}"
#         f"&post_logout_redirect_uri=http://localhost:8000"
#         f"&state=someState"
#     )

#     response = RedirectResponse(url=okta_logout_url)
#     response.delete_cookie(key="access_token")
#     response.delete_cookie(key="id_token")  # Optionally delete the ID token cookie
#     return response

import base64
import hashlib
import secrets

import requests
from fastapi import APIRouter, HTTPException, Request
from routers.paths import OktaPath, Path
from settings import OKTA_CLIENT_ID, OKTA_CLIENT_SECRET, OKTA_ORG_URL, OKTA_REDIRECT_URI
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get(Path.authorization_code_callback)
async def callback(request: Request):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    code = request.query_params.get("code")
    app_state = request.query_params.get("state")

    if app_state != request.session["app_state"]:
        raise HTTPException(status_code=400, detail="The app state doesn't match")
    if not code:
        raise HTTPException(status_code=403, detail="The code wasn't returned or isn't accessible")

    query_params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": str(request.base_url)[0:-1] + request.url.path,
        "code_verifier": request.session["code_verifier"],
    }
    query_params = requests.compat.urlencode(query_params)
    exchange = requests.post(
        f"{OKTA_ORG_URL}{OktaPath.auth_token}",
        headers=headers,
        data=query_params,
        auth=(OKTA_CLIENT_ID, OKTA_CLIENT_SECRET),
    ).json()

    if not exchange.get("token_type"):
        raise HTTPException(status_code=403, detail="Unsupported token type. Should be 'Bearer'.")

    access_token = exchange["access_token"]

    response = RedirectResponse(url=Path.home)
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return response


@router.get(Path.login)
async def login(request: Request):
    request.session["app_state"] = secrets.token_urlsafe(64)
    request.session["code_verifier"] = secrets.token_urlsafe(64)

    hashed = hashlib.sha256(request.session["code_verifier"].encode("ascii")).digest()
    encoded = base64.urlsafe_b64encode(hashed)
    code_challenge = encoded.decode("ascii").strip("=")

    query_params = {
        "client_id": OKTA_CLIENT_ID,
        "redirect_uri": OKTA_REDIRECT_URI,
        "scope": "openid email profile",
        "state": request.session["app_state"],
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "response_type": "code",
        "response_mode": "query",
    }

    request_uri = "{base_url}?{query_params}".format(
        base_url=f"{OKTA_ORG_URL}{OktaPath.authorize}", query_params=requests.compat.urlencode(query_params)
    )

    return RedirectResponse(request_uri)
