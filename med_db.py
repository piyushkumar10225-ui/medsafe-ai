import json
import os
import streamlit as st
from typing import Dict, Any

from utils import setup_logger

logger = setup_logger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

@st.cache_data
def load_json_data(filename: str) -> Dict[str, Any]:
    """Loads a JSON dataset with caching."""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        logger.error(f"Dataset {filename} not found at {filepath}")
        return {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing {filename}: {e}")
            return {}

def get_medicines() -> Dict[str, Any]:
    return load_json_data("medicines.json")

def get_interactions() -> Dict[str, Any]:
    return load_json_data("interactions.json")

def get_side_effects() -> Dict[str, Any]:
    return load_json_data("side_effects.json")
