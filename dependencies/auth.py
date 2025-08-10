from fastapi import Depends

async def verify_token():
    print(">>> Dummy auth used ✅")
    return {"sub": "test-user-id"}
