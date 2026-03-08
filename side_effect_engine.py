from typing import List, Dict, Any
from med_db import get_side_effects, get_medicines

def analyze_side_effects(med_name: str, symptoms_text: str) -> Dict[str, Any]:
    """
    Correlates user symptoms with known medicine side effects.
    """
    symptoms = symptoms_text.lower()
    known_side_effects = get_medicines().get(med_name, {}).get("side_effects", [])
    
    detected = []
    for effect in known_side_effects:
        if effect.lower() in symptoms:
            detected.append(effect)
            
    return {
        "medicine": med_name,
        "matched_symptoms": detected,
        "has_reaction": len(detected) > 0,
        "advice": "Stop usage and consult a doctor immediately if you experience severe allergic reactions." if len(detected) > 0 else "No direct side effects currently correlated."
    }
