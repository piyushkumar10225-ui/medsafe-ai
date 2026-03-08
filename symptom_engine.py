from typing import Dict, Any

def analyze_symptoms(symptoms_text: str) -> Dict[str, Any]:
    """
    Rule-based symptom severity analysis.
    Returns severity (Low, Moderate, High) and advice.
    """
    symptoms = symptoms_text.lower()
    
    # Emergency Keywords
    emergency_keywords = ["chest pain", "shortness of breath", "unconscious", "stroke", "paralysis", "blood", "severe"]
    moderate_keywords = ["vomiting", "dizziness", "fever", "migraine", "persistent", "dehydration"]
    
    for word in emergency_keywords:
        if word in symptoms:
            return {
                "level": "High",
                "warning": "EMERGENCY: Seek immediate medical attention.",
                "advice": f"Your symptom description includes '{word}', which may indicate a life-threatening condition. Please visit an emergency room."
            }
            
    for word in moderate_keywords:
        if word in symptoms:
            return {
                "level": "Moderate",
                "warning": "Warning: Monitor your condition closely.",
                "advice": f"You mentioned '{word}'. Stay hydrated and rest. If symptoms worsen, consult a doctor."
            }
            
    return {
        "level": "Low",
        "warning": "No immediate severe risks detected based on your input.",
        "advice": "Rest and monitor your symptoms. Consult a doctor if they persist."
    }
