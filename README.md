# AuraFlow AI(Velow) - Strategic Engine

?? **Live Demo:** [https://auraflow-frontend-p0iqp833i-leharinshainsha05-stacks-projects.vercel.app](https://velow-ai-chi.vercel.app/)

> **Note for Judges:** The live demo shows the full UI. For complete AI functionality, please run locally using the setup instructions below. The backend is hosted on Render free tier which may need 1-2 minutes to wake up on first request.

AuraFlow is an AI-powered project management and strategic planning platform built for the modern startup ecosystem.

## Project Structure
- /backend - FastAPI Python backend
- /frontend - React frontend

## Features
- ?? Soul Search - Real-time market research using AI
- ?? File Manager - AI-powered project brief analysis
- ?? Project Plan Generator
- ?? Pitch Deck Generator
- ??? Multi-Project Manager
- ?? Progress Tracker
- ?? AI Chat Assistant
- ?? Google OAuth Authentication

## Tech Stack
### Backend
- FastAPI + Uvicorn
- Groq AI (llama-3.3-70b-versatile)
- Tavily Search API
- Google OAuth 2.0
- Python 3.14

### Frontend
- React.js
- Axios
- CSS3

## Setup
### Backend
1. cd backend
2. Create .env with: GROQ_API_KEY, TAVILY_API_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
3. pip install -r requirements.txt
4. uvicorn main:app --reload

### Frontend
1. cd frontend
2. npm install
3. npm start
