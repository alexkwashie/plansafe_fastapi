from fastapi import APIRouter, HTTPException, status
from routers.schemas import LoginRequest, RegisterRequest, TokenResponse, RefreshRequest
from db.supabase_client import supabase

router = APIRouter(
    prefix='/api/v1/auth',
    tags=['auth']
)


@router.post('/login', response_model=TokenResponse)
async def login(request: LoginRequest):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password,
        })
        session = response.session
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "token_type": "bearer",
            "user_id": response.user.id,
            "email": response.user.email,
        }
    except Exception as e:
        if "Invalid" in str(e) or "invalid" in str(e):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/register')
async def register(request: RegisterRequest):
    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "username": request.username,
                    "firstname": request.firstname,
                    "lastname": request.lastname,
                }
            }
        })
        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed",
            )
        return {
            "user_id": response.user.id,
            "email": response.user.email,
            "message": "Registration successful",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/logout')
async def logout():
    try:
        supabase.auth.sign_out()
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/refresh', response_model=TokenResponse)
async def refresh_token(request: RefreshRequest):
    try:
        response = supabase.auth.refresh_session(request.refresh_token)
        session = response.session
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "token_type": "bearer",
            "user_id": response.user.id,
            "email": response.user.email,
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
