# TOK Backend

TOK is a FastAPI backend that turns short voice recordings from market vendors into structured product listings. It uses Groq Whisper for transcription and Groq Llama for item/price extraction, then stores the result in a PostgreSQL database.

This project is designed for a local-market or informal vendor workflow where a seller records a voice note, and the system turns it into a product listing automatically.

## Project overview

The backend exposes a single primary endpoint for voice processing:

- `POST /test-voice-processing`
- Accepts an audio file upload and optional phone number
- Transcribes the spoken audio using Groq Whisper
- Extracts the product name and price using Groq Llama
- Saves the vendor and listing to the database
- Returns the created listing and vendor metadata

## Key features

- Audio transcription with Groq Whisper
- AI-based listing extraction with Groq Llama 3.3
- Vendor tracking by phone number
- Product listing persistence in PostgreSQL
- FastAPI REST API with CORS enabled for browser-based frontend integrations
- Local SQLite fallback support via environment configuration

## Repository structure

```text
Tok/
├── generate_audio.py            # Generates a sample MP3 for testing
├── sample_listing.mp3           # Sample vendor audio file
├── tok-backend/
│   ├── .env                    # Local environment file with API and DB config
│   ├── create_db.py            # Creates the PostgreSQL database if needed
│   ├── requirements.txt        # Python dependencies
│   ├── README.md               # Project documentation
│   └── app/
│       ├── config.py           # Pydantic settings and environment loading
│       ├── crud.py             # Database operations for vendor/listing records
│       ├── database.py         # SQLAlchemy engine/session configuration
│       ├── main.py             # FastAPI app and API endpoints
│       ├── models.py           # SQLAlchemy data models
│       ├── schemas.py          # Pydantic response/request schemas
│       └── services/
│           └── groq_service.py # Groq transcription and extraction logic
```

## Tech stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic + Pydantic Settings
- Groq API
- python-dotenv

## Prerequisites

Before running the project, make sure you have:

- Python installed and available on your PATH
- PostgreSQL running locally
- A Groq API key
- Access to a local database named `tok_db` or adjust the database URL in `.env`

## Environment configuration

Create or update the file `.env` inside `tok-backend` with values like:

```env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tok_db
```

The project loads environment variables via `python-dotenv` and `pydantic-settings`.

> The default database URL in the config is SQLite, but this app is intended for PostgreSQL and uses the `.env` value when configured.

## Installation

From the project root or the backend directory:

```bash
cd tok-backend
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# or
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Database setup

The project includes a helper script to create the PostgreSQL database:

```bash
python create_db.py
```

This connects to the local PostgreSQL server, checks whether `tok_db` exists, and creates it if needed.

## Running the app

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

## Sample audio generation

At the workspace root, there is a script that creates a sample voice message:

```bash
cd ..
python generate_audio.py
```

This generates a file named `sample_listing.mp3` using Google Text-to-Speech and can be used for testing the voice pipeline.

## API usage

### Endpoint

```http
POST /test-voice-processing
```

### Form fields

- `file`: audio file upload
- `phone_number`: optional vendor phone number, default is `+2348000000000`

### Example with curl

```bash
curl -X POST "http://127.0.0.1:8000/test-voice-processing" \
  -F "file=@sample_listing.mp3" \
  -F "phone_number=+2348000000000"
```

### Example response

```json
{
  "status": "success",
  "vendor_id": 1,
  "listing": {
    "id": 5,
    "item_name": "fried rice",
    "price": 2000.0,
    "raw_transcript": "I sell fried rice for 2000 Naira",
    "created_at": "2026-09-22T12:00:00"
  }
}
```

## Data model

### Vendor

- `id`
- `phone_number` (unique)
- `name` (optional)
- `created_at`

### Listing

- `id`
- `vendor_id`
- `item_name`
- `price`
- `raw_transcript`
- `is_available`
- `created_at`

## Notes on the workflow

1. An audio file is uploaded to the backend.
2. The file is saved temporarily.
3. Groq Whisper converts speech to text.
4. Llama extracts structured data (`item_name` and `price`).
5. A vendor is created or fetched by phone number.
6. The listing is saved to the database.
7. The temporary audio file is deleted.

## Operational considerations

- Ensure `GROQ_API_KEY` is set before starting the backend.
- If PostgreSQL is not running, the app will fail to persist records.
- The project is intentionally simple and is meant for local prototyping or hackathon-style validation.
- The root-level `generate_audio.py` script is a helpful tool for generating synthetic sample inputs.

## Typical development flow

```bash
cd tok-backend
python -m venv .venv
. .venv/Scripts/activate   # Windows
pip install -r requirements.txt
python create_db.py
uvicorn app.main:app --reload
```

Then upload audio through the `/test-voice-processing` endpoint or test with a frontend client.

## Summary

This project demonstrates a practical voice-to-commerce pipeline: audio input is transcribed and parsed into a listing, then stored for later retrieval or display by a frontend application. It is a strong foundation for building a vendor inventory or local marketplace product ingestion flow.
