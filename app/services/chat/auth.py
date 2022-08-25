import logging

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from platform_services.keycloak.injectors import JWTTokenModel, strict_bearer_auth
from pydantic import UUID4
from keycloak import KeycloakOpenID

logger = logging.getLogger(__name__)


# async def auth_required(token: JWTTokenModel = Depends(strict_bearer_auth)) -> UUID4:
#     try:
#         return token.subject
#     except ValueError as err:
#         logger.error(f"Invalid subject in JTW: {token.json()}", exc_info=True)
#         print(err)
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentails",
#             headers={"WWW-Authenticate": "Bearer"},
#         ) from err


async def auth_required(token):
    keycloak_openid = KeycloakOpenID(
        server_url="http://localhost:8081/auth/",
        client_id="admin-cli",
        realm_name="qwerty",
        client_secret_key="2ed071c5-c50d-4048-bf49-45504720693a",
    )

    KEYCLOAK_PUBLIC_KEY = (
        "-----BEGIN PUBLIC KEY-----\n"
        + keycloak_openid.public_key()
        + "\n-----END PUBLIC KEY-----"
    )
    options = {"verify_signature": False, "verify_aud": False, "verify_exp": False}
    token_info = keycloak_openid.decode_token(
        token, key=KEYCLOAK_PUBLIC_KEY, options=options
    )
    return token_info
