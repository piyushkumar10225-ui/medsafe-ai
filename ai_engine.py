import ollama
import json
from typing import Dict, Any
from utils import setup_logger
import streamlit as st

logger = setup_logger(__name__)

# Model identifier for the chosen base model
OLLAMA_MODEL = "llama3"

@st.cache_data(show_spinner=False)
def generate_interaction_explanation(med1: str, med2: str, severity: str) -> str:
    """Uses Ollama to generate an explanation for a drug interaction."""
    prompt = f"Explain the potential drug interaction between {med1} and {med2}. The severity is {severity}. Provide the answer in simple, non-medical terms for educational purposes. Keep it under 4 sentences."
    
    try:
        response = ollama.chat(model=OLLAMA_MODEL, messages=[
            {
                'role': 'system',
                'content': 'You are a helpful healthcare awareness assistant. Remind users to seek professional advice. Be brief and clear.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ])
        return response['message']['content']
    except Exception as e:
        logger.error(f"Ollama generation failed: {e}")
        return "Failed to generate AI explanation. Please ensure Ollama is running."

def parse_prescription_text(ocr_text: str) -> Dict[str, Any]:
    """Uses Ollama to parse messy OCR text into structured JSON."""
    prompt = f"""
    Extract medicines mentioned in the following messy OCR prescription text. 
    Format the output strictly as JSON. No markdown, no explanations. 
    Format: {{"medicines": [{{"name": "MedName", "salt": "SaltName"}}]}}
    
    Text: {ocr_text}
    """
    
    try:
        response = ollama.chat(model=OLLAMA_MODEL, messages=[
            {
                'role': 'system',
                'content': 'You are a precise data extraction tool. Output raw JSON only.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ])
        content = response['message']['content']
        # cleanup if the model wraps in markdown
        if "```json" in content:
            content = content.replace("```json", "").replace("```", "").strip()
        
        parsed = json.loads(content)
        return parsed
    except json.JSONDecodeError as e:
        logger.error(f"JSON Parse failed from AI response: {e}")
        return {"medicines": []}
    except Exception as e:
        logger.error(f"Ollama parsing failed: {e}")
        return {"medicines": []}
