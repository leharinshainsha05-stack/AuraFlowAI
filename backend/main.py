from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import soul_search, project_plan, pitch_deck, file_manager, progress, chat, auth, analyze
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="AuraFlow AI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=".*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(soul_search.router, prefix="/api")
app.include_router(project_plan.router, prefix="/api")
app.include_router(pitch_deck.router, prefix="/api")
app.include_router(file_manager.router, prefix="/api")
app.include_router(progress.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AuraFlow AI Backend is running 🚀"}
