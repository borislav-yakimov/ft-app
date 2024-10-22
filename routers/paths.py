from dataclasses import dataclass


@dataclass
class Path:
    home: str = "/"
    login: str = "/login"
    offers: str = "/offers"
    # offers: str = "/offers"
    authorization_code_callback: str = "/authorization-code/callback"


@dataclass
class OktaPath:
    authorize: str = "/oauth2/default/v1/authorize"
    auth_token: str = "/oauth2/default/v1/token"
    user_info: str = "/oauth2/default/v1/userinfo"
    # logout: str = "/oauth2/default/v1/logout"
    logout: str = "/oauth2/default/v1/logout"
