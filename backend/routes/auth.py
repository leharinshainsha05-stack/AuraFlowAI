import os
import httpx
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://auraflow-backend-nu2p.onrender.com/api/google/callback")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://aura-flow-ai-chi.vercel.app")

@router.get("/google")
async def google_login():
    return RedirectResponse(
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
        f"&redirect_uri={REDIRECT_URI}"
        f"&prompt=select_account"
    )

@router.get("/google/callback")
async def google_callback(code: str):
    print(f"DEBUG: Callback received with code: {code[:10]}...")
    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            }
        )
        tokens = token_res.json()
        if "access_token" not in tokens:
            print(f"DEBUG: Token exchange failed: {tokens}")
            return RedirectResponse(f"{FRONTEND_URL}?error=token_failed")
        user_res = await client.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {tokens['access_token']}"}
        )
        user_info = user_res.json()
    name = user_info.get("name", "User")
    email = user_info.get("email", "")
    print(f"DEBUG: Login successful for {email}")
    return RedirectResponse(
        f"{FRONTEND_URL}?user={name.replace(' ', '%20')}&logged_in=true&email={email}"
    )
