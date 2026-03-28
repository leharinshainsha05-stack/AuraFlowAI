import os
import httpx
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

router = APIRouter()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/api/google")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

@router.get("/google")
async def google_auth(request: Request):
    # This is the secret to breaking the loop: 
    # Grabbing the code directly from the raw query params
    params = request.query_params
    code = params.get("code")

    # 1. If NO code is present, we are STARTING the login
    if not code:
        print("DEBUG: No code found, redirecting to Google...")
        return RedirectResponse(
            f"https://accounts.google.com/o/oauth2/v2/auth?client_id={CLIENT_ID}"
            f"&response_type=code&scope=openid%20email%20profile"
            f"&redirect_uri={REDIRECT_URI}"
            f"&prompt=select_account" # This ensures it doesn't auto-loop
        )

    # 2. If code IS present, Google just sent us back! 
    # STOP THE LOOP: Exchange the code for a token
    print(f"DEBUG: Code received: {code[:10]}...")
    
    async with httpx.AsyncClient() as client:
        token_res = await client.post("https://oauth2.googleapis.com/token", data={
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        })
        
        tokens = token_res.json()
        
        if "access_token" not in tokens:
            print(f"DEBUG: Token exchange failed: {tokens}")
            return RedirectResponse(f"{FRONTEND_URL}?error=token_failed")

        # 3. Get User Data
        user_res = await client.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {tokens['access_token']}"}
        )
        user_info = user_res.json()

    # 4. FINAL REDIRECT: Go back to Frontend (The Loop ends here!)
    name = user_info.get("name", "User")
    return RedirectResponse(f"{FRONTEND_URL}?user={name.replace(' ', '%20')}&logged_in=true")
