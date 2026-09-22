import json
import os
from dotenv import load_dotenv
from groq import Groq

# Ensure environment variables are loaded
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is missing.")

client = Groq(api_key=api_key)

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes an audio file using Groq Whisper.
    """
    with open(file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(file_path), file.read()),
            model="whisper-large-v3",
            response_format="text"
        )
    return str(transcription)

def extract_listing_from_transcript(transcript: str) -> dict:
    """
    Extracts item_name and price from raw transcript using Groq Llama 3.3.
    """
    prompt = f"""
    You are an AI assistant for a local market vendor app.
    Extract the product item name and price from the following raw spoken transcript.
    
    Transcript: "{transcript}"
    
    Respond ONLY in valid JSON format with no Markdown formatting or conversational text:
    {{
      "item_name": "string",
      "price": number
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You output strictly valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    raw_content = response.choices[0].message.content or "{}"
    content = raw_content.strip()
    
    return json.loads(content)