def generate_action_plan(hazards, risk_level):
    plan = []
    for hazard in hazards:
        if hazard == "gas_cylinder":
            plan.append("Check cylinder valve and isolate area")
        elif hazard == "electrical_fire":
            plan.append("Cut power supply and use extinguisher")
        elif hazard == "industrial_fire":
            plan.append("Activate fire alarm and evacuate")
        elif hazard == "ppe":
            plan.append("Ensure workers wear proper PPE")
    if risk_level == "High":
        plan.append("Notify safety officer immediately")
    return plan

