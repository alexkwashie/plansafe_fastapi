from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

from db.supabase_client import supabase

load_dotenv()  # This loads the variables from .env into the environment

# Get these from your Supabase project settings
JWT_SECRET = os.getenv("SUPABASE_JWT_KEY")
ALGORITHM = "HS256"

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM], audience="authenticated")
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return {
            "user_id": user_id,
            "email": payload.get("email"),
            "role": payload.get("role"),
            "access_token": token,
            "refresh_token": token,
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


async def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        # Use Supabase's built-in auth verification
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Return the user object with the token for database operations
        return {
            "id": user_response.user.id,
            "email": user_response.user.email,
            "access_token": token,  # Include access token for database operations
            "refresh_token": token  # For now, using the same token as refresh (we'll need to get the actual refresh token)
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
