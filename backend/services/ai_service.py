from groq import Groq
import os
import re
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_claude(prompt: str, system: str = "") -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system if system else "You are AuraFlow AI, a Universal Strategic Engine."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4096,
        temperature=0.7
    )
    content = response.choices[0].message.content
    
    # Strip markdown code blocks if present
    content = re.sub(r'```json\s*', '', content)
    content = re.sub(r'```\s*', '', content)
    content = content.strip()
    
    return content