from fastapi import HTTPException, status, Request
from jose import jwt
import httpx
import os


SUPABASE_JWKS_URL = os.getenv("SUPABASE_URL")
SUPABASE_AUDIENCE  = os.getenv("SUPABASE_KEY")

# Cache keys
jwks_cache = {}

async def get_jwks():
    if not jwks_cache:
        async with httpx.AsyncClient() as client:
            response = await client.get(SUPABASE_JWKS_URL)
            jwks_cache.update(response.json())
    return jwks_cache

async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    token = auth_header.split(" ")[1]
    jwks = await get_jwks()

    try:
        unverified_header = jwt.get_unverified_header(token)
        key = next(k for k in jwks["keys"] if k["kid"] == unverified_header["kid"])
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=SUPABASE_AUDIENCE,
            options={"verify_aud": False},  # can set to True with proper audience
        )
        return payload
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))