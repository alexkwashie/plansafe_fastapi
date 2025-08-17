from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from supabase import create_client, Client

load_dotenv()  # This loads the variables from .env into the environment

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class User(BaseModel):
    id: str

# Get these from your Supabase project settings
JWT_SECRET = os.getenv("SUPABASE_JWT_KEY")
ALGORITHM = "HS256"

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    token = credentials.credentials
    try:
        # Decode and verify JWT
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        print(f"** user {payload}")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        
        return User(id=user_id)
    except JWTError:
        print(f'#### --- {JWTError}')
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
        print(f"Auth error: {e}")
        raise HTTPException(status_code=401, detail=str(e))
    

def verified_user_path(function):
    async def protected_route(user: User = Depends(verify_jwt)):

        result = await function(user)

        return result

    return protected_route