def analyze_risk(hazards):
    """
    Simple risk scoring based on hazard type
    """
    risk_score = 0
    for hazard in hazards:
        if hazard == "gas_cylinder":
            risk_score += 30
        elif hazard == "electrical_fire":
            risk_score += 40
        elif hazard == "industrial_fire":
            risk_score += 50
        elif hazard == "ppe":
            risk_score += 10
    risk_level = "Low"
    if risk_score >= 50:
        risk_level = "High"
    elif risk_score >= 20:
        risk_level = "Medium"
    return risk_score, risk_level

