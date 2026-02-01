import json

def analyze_cluster_semantically(cluster_text):
    """
    REASON (LLM-Hybrid): Simulates an LLM call to infer context from text.
    Returns structured JSON validation.
    """
    text = cluster_text.lower()
    
    # Mock LLM Reasoning Logic (Simulating semantic understanding)
    response = {
        "stage": "Stage 1: Setup & Auth",
        "root_cause": "Merchant Configuration Error",
        "reasoning": "The user is struggling with initial API key validation, which is typical during setup.",
        "confidence": 0.65
    }

    if "production" in text or "500" in text or "outage" in text:
        response = {
            "stage": "Stage 3: Live / Scale",
            "root_cause": "Platform Issue / Regression",
            "reasoning": "Keywords '500 error' and 'production' indicate a server-side failure affecting live traffic.",
            "confidence": 0.92
        }
    elif "docs" in text or "example" in text or "how to" in text:
        response = {
            "stage": "Stage 2: Integration",
            "root_cause": "Documentation Gap",
            "reasoning": "Users are requesting examples and schema definitions, implying missing information in developer guides.",
            "confidence": 0.85
        }
    elif "checkout" in text and "error" not in text:
        # Edge case: Integration questions about checkout
        response = {
            "stage": "Stage 2: Integration",
            "root_cause": "Merchant Configuration Error",
            "reasoning": "Questions regarding checkout implementation logic suggest implementation hurdles, not platform bugs.",
            "confidence": 0.75
        }

    return response