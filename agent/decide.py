def determine_action(analysis):
    """
    DECIDE: Maps analysis to action. 
    Now includes handling for mixed/noise clusters.
    """
    stage = analysis['stage']
    root_cause = analysis['root_cause']
    
    # Defaults
    action = "Send standard configuration guide."
    risk = "Low"

    # --- LOGIC MAPPING ---
    if root_cause == "Documentation Gap":
        action = "Create internal ticket to update docs + Notify merchant."
        risk = "Medium"
        
    elif root_cause == "Platform Issue / Regression":
        action = "ESCALATE to Engineering immediately."
        risk = "High"
        
    # [NEW] Logic for Noise/Mixed Issues
    elif root_cause == "Mixed / Uncorrelated Issues":
        action = "Route tickets to standard support workflow (Manual Triage)."
        risk = "Medium"

    # --- STAGE OVERRIDES ---
    if "Stage 3" in stage and risk != "High":
        risk = "High (Production Impact)"
        if "standard support" not in action:
            action = "Escalate to Senior Support (Production Config Check)."

    return {
        "recommended_action": action,
        "risk_level": risk
    }