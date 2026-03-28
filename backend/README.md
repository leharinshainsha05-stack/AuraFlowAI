# AuraFlow AI Backend

A FastAPI backend powering the AuraFlow Strategic Engine.

## Features
- Soul Search - Real-time market research using Tavily + Groq AI
- Project Plan Generator
- Pitch Deck Generator  
- File Manager - AI-powered project brief analysis
- Multi-Project Manager
- Progress Tracker
- AI Chat Assistant
- Google OAuth Authentication

## Tech Stack
- FastAPI + Uvicorn
- Groq AI (llama-3.3-70b-versatile)
- Tavily Search API
- Google OAuth 2.0
- Python 3.14

## Setup
1. Clone the repo
2. Create .env with: GROQ_API_KEY, TAVILY_API_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
3. pip install -r requirements.txt
4. uvicorn main:app --reload
