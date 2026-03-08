from typing import Dict, Any, List

def calculate_risk_score(age: int, symptoms: str, medicines: List[str], side_effect_matches: int) -> Dict[str, Any]:
    """
    Calculates health risk score (0-100).
    """
    score = 0
    
    # Age factor
    if age > 65:
        score += 15
    elif age < 12:
        score += 10
        
    # Medicines count factor
    if len(medicines) > 3:
        score += 20
    elif len(medicines) > 1:
        score += 10
        
    # Symptoms severity factor
    symptoms_lower = symptoms.lower()
    if any(k in symptoms_lower for k in ["chest pain", "shortness of breath", "unconscious", "blood"]):
        score += 50
    elif any(k in symptoms_lower for k in ["vomiting", "dizziness", "fever", "severe pain"]):
        score += 25
        
    # Side effects factor
    if side_effect_matches > 0:
        score += 15 * side_effect_matches
        
    # Cap score
    score = min(score, 100)
    
    # Categorize
    if score <= 30:
        level = "Low Risk"
        rec = "Monitor vitals and rest. Seek medical advice if conditions change."
    elif score <= 60:
        level = "Moderate Risk"
        rec = "Consider consulting a healthcare professional promptly."
    else:
        level = "High Risk"
        rec = "Seek EMERGENCY medical attention immediately."
        
    return {
        "risk_score": score,
        "risk_level": level,
        "recommendation": rec
    }
