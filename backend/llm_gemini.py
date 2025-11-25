import google.generativeai as genai
from backend.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def ask_gemini(question: str, context: str = ""):
    prompt = f"Use this context to answer:\n{context}\n\nQuestion: {question}"
    
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(prompt)

    return response.text