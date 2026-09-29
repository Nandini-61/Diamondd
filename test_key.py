import json
import google.generativeai as genai
from django.conf import settings

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
GOOGLE_API_KEY = "AIzaSyDGsKNjOPjFQkuQub0vyz-2V3R-VN-4m64"  # <--- PASTE KEY HERE

genai.configure(api_key=GOOGLE_API_KEY)

def analyze_email_content(subject, body):
    """
    Uses Google Gemini 2.0 Flash to analyze the email.
    """
    
    # We use 'gemini-2.0-flash' as confirmed in your list
    model = genai.GenerativeModel('models/gemini-2.0-flash')

    prompt = f"""
    Act as an Enterprise Email Risk Analyst.
    Analyze the following email and output strictly valid JSON.
    
    EMAIL SUBJECT: {subject}
    EMAIL BODY: {body}

    REQUIRED JSON STRUCTURE:
    {{
        "summary": "1 short sentence summary",
        "sentiment": "Positive, Neutral, or Negative",
        "tone": "e.g. Formal, Aggressive, Urgent",
        "risk_score": Integer between 0 and 100,
        "flagged_keywords": "comma, separated, bad, words",
        "suggested_category": "inquiry, complaint, support, finance, or other",
        "suggested_reply": "A professional draft response"
    }}
    
    Do not include markdown formatting like ```json. Just return the raw JSON string.
    """

    try:
        # Generate content
        response = model.generate_content(prompt)
        
        # Clean up response (Gemini sometimes adds ```json anyway)
        text_response = response.text
        if "```" in text_response:
            text_response = text_response.replace("```json", "").replace("```", "")
        
        # Parse JSON
        analysis_data = json.loads(text_response.strip())
        return analysis_data

    except Exception as e:
        print(f"Gemini Error: {e}")
        return {
            "summary": "AI Analysis Failed",
            "sentiment": "Neutral",
            "tone": "Unknown",
            "risk_score": 0,
            "flagged_keywords": "Error",
            "suggested_category": "other",
            "suggested_reply": "Could not generate draft due to API error."
        }