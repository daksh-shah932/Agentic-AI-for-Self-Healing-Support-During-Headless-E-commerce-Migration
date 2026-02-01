def generate_alternatives(selected_root_cause, cluster_text):
    """
    REASON (Counterfactual): Generates 'Why not X?' arguments.
    Crucial for explainability and reducing hallucination.
    """
    text = cluster_text.lower()
    alternatives = []

    # Hypothesis 1: Platform Issue
    if selected_root_cause != "Platform Issue / Regression":
        if "500" not in text and "outage" not in text:
            alternatives.append({
                "hypothesis": "Platform Issue / Regression",
                "reason_rejected": "No server-side error codes (5xx) or 'outage' keywords detected in ticket text."
            })
        else:
            alternatives.append({
                "hypothesis": "Platform Issue / Regression",
                "reason_rejected": "Symptoms appeared isolated to specific configuration rather than global failure."
            })

    # Hypothesis 2: Documentation Gap
    if selected_root_cause != "Documentation Gap":
        if "example" not in text and "docs" not in text:
            alternatives.append({
                "hypothesis": "Documentation Gap",
                "reason_rejected": "Users are reporting errors, not asking for clarification or missing links."
            })
        else:
             alternatives.append({
                "hypothesis": "Documentation Gap",
                "reason_rejected": "Documentation exists, but user implementation contradicts the schema."
            })

    # Hypothesis 3: Merchant Config
    if selected_root_cause != "Merchant Configuration Error":
        alternatives.append({
            "hypothesis": "Merchant Configuration Error",
            "reason_rejected": "Issue persists across multiple merchants or affects internal systems, ruling out individual config."
        })

    return alternatives