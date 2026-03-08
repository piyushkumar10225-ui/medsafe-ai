from rapidfuzz import process, fuzz
from typing import List, Dict, Tuple, Any
from med_db import get_medicines, get_interactions
import streamlit as st

@st.cache_data
def fuzzy_match_medicine(search_term: str) -> Tuple[str, float]:
    """Finds the closest matching medicine name from the database."""
    medicines = list(get_medicines().keys())
    if not medicines:
        return "", 0.0
    
    # Extract the best match
    match = process.extractOne(search_term.lower(), medicines, scorer=fuzz.WRatio)
    if match:
        name, score, _ = match
        return name, score
    return "", 0.0

def check_interactions(med_list: List[str]) -> List[Dict[str, Any]]:
    """
    Checks for interactions between a list of matched medicines.
    Returns a list of interactions found.
    """
    db_interactions = get_interactions()
    found_interactions = []
    
    # Check pairs
    for i in range(len(med_list)):
        for j in range(i + 1, len(med_list)):
            med1 = med_list[i]
            med2 = med_list[j]
            
            key1 = f"{med1}_{med2}"
            key2 = f"{med2}_{med1}"
            
            if key1 in db_interactions:
                desc = db_interactions[key1]
                found_interactions.append({"meds": (med1, med2), **desc})
            elif key2 in db_interactions:
                desc = db_interactions[key2]
                found_interactions.append({"meds": (med1, med2), **desc})
                
    return found_interactions
