import os
import re
import random
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

# Load .env from the repo or parent directories (local dev). In GitHub Actions
# we will use repository Secrets instead.
load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL", "https://api.zetatechs.com")
api_endpoint = GEMINI_BASE_URL.replace("https://", "").replace("http://", "").rstrip("/")

def generate_cyberpunk_quote():
    if not GEMINI_API_KEY:
        return "> **[System Alert]:** AI Core disconnected."

    genai.configure(
        api_key=GEMINI_API_KEY,
        client_options={"api_endpoint": api_endpoint}
    )
    
    try:
        model = genai.GenerativeModel('gemini-3-flash-preview-free')
        prompt = "You are a cyberpunk hacker AI called 'Sentinel'. Generate a very short (max 2 sentences), cool 'Hacker Quote of the Day' or an insightful software architecture tip in a cypherpunk/dark-web tone. Output only the quote without quotes or explanation."
        response = model.generate_content(prompt)
        quote = response.text.strip()
        return f"> **[AI Core Sentinel]:** {quote}"
        
    except Exception as e:
        print(f"Error fetching from Gemini API: {e}")
        return "> **[System Alert]:** AI Core disconnected. Retrieving cached protocols... // Standby."

def update_readme():
    quote = generate_cyberpunk_quote()
    with open('README.md', 'r', encoding='utf-8') as file:
        readme_contents = file.read()
        
    pattern = r"<!-- START_SECTION:ai_quote -->\n.*?\n<!-- END_SECTION:ai_quote -->"
    replacement = f"<!-- START_SECTION:ai_quote -->\n{quote}\n<!-- END_SECTION:ai_quote -->"
    
    new_contents = re.sub(pattern, replacement, readme_contents, flags=re.DOTALL)
    
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(new_contents)
        
if __name__ == "__main__":
    update_readme()
