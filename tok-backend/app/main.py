import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
import app.models  # Registers models with Base
from app import crud
from app.services.groq_service import transcribe_audio, extract_listing_from_transcript

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TOK Backend Service", version="1.0.0")

# Enable CORS for Next.js frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "online", "message": "TOK Python Backend Operational"}

@app.post("/test-voice-processing")
async def test_voice_processing(
    file: UploadFile = File(...),
    phone_number: str = Form("+2348000000000"),
    db: Session = Depends(get_db)
):
    """
    Pre-Hackathon Test Endpoint:
    Uploads audio, transcribes it via Groq Whisper, extracts product details via Llama 3,
    and automatically persists the vendor and listing into PostgreSQL.
    """
    temp_file_path = f"temp_{file.filename}"
    try:
        # Save uploaded audio file locally
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 1. Transcribe audio using Groq Whisper
        transcript = transcribe_audio(temp_file_path)
        
        # 2. Extract structured data using Groq Llama 3
        extracted_data = extract_listing_from_transcript(transcript)
        
        item_name = extracted_data.get("item_name", "Unknown Item")
        price = float(extracted_data.get("price", 0.0))
        
        # 3. Get or create vendor in database
        vendor = crud.get_or_create_vendor(db, phone_number=phone_number)
        
        # 4. Save extracted listing to database
        db_listing = crud.create_vendor_listing(
            db=db,
            vendor_id=vendor.id,
            item_name=item_name,
            price=price,
            raw_transcript=transcript
        )
        
        # 5. Return target response payload
        return {
            "status": "success",
            "vendor_id": vendor.id,
            "listing": {
                "id": db_listing.id,
                "item_name": db_listing.item_name,
                "price": db_listing.price,
                "raw_transcript": db_listing.raw_transcript,
                "created_at": db_listing.created_at
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary audio file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)