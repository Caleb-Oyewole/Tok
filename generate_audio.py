from gtts import gTTS
import os

def create_sample_audio(text: str, output_filename: str):
    """
    Generates an MP3 audio file from text using Google Text-to-Speech.
    
    Parameters:
        text (str): The spoken statement to synthesize.
        output_filename (str): The target output filename (e.g., sample_listing.mp3).
    """
    # Initialize gTTS with English language setting
    tts = gTTS(text=text, lang='en', slow=False)
    
    # Save the audio file locally
    tts.save(output_filename)
    print(f"Successfully generated sample audio: {output_filename}")

if __name__ == "__main__":
    # Sample phrase for testing speech-to-text and LLM extraction
    sample_phrase = "I sell fried rice for 2000 Naira"
    output_path = "sample_listing.mp3"
    
    create_sample_audio(sample_phrase, output_path)