def analyze_cluster(cluster_label, tickets):
    """
    REASON: Infers context/problem. Handles Noise (-1) explicitly.
    """
    combined_text = " ".join([t['message'].lower() for t in tickets])
    
    # --- DEFAULT INFERENCE LOGIC (Preserved) ---
    stage = "Stage 1: Setup & Auth"
    if any(w in combined_text for w in ['traffic', 'timeout', 'peak', 'latency', 'production', 'outage', '500']):
        stage = "Stage 3: Live / Scale"
    elif any(w in combined_text for w in ['checkout', 'order', 'webhook', 'payment', 'cart']):
        stage = "Stage 2: Integration"
    
    root_cause = "Merchant Configuration Error"
    if any(w in combined_text for w in ['documentation', 'example', 'where can i find', 'docs', 'schema']):
        root_cause = "Documentation Gap"
    elif any(w in combined_text for w in ['timeout', 'internal error', '500', 'latency', 'failure']):
        root_cause = "Platform Issue / Regression"

    # Base confidence calculation
    confidence = min(0.6 + (len(tickets) * 0.1), 0.95)

    # --- UPDATED NOISE HANDLING LOGIC ---
    if cluster_label == -1 or cluster_label == "Noise":
        cluster_name = "Isolated / Rare Issues"
        # Overwrite specific fields for Noise
        root_cause = "Mixed / Uncorrelated Issues"
        stage = "Various / Indeterminate" 
        confidence = 0.3  # Cap confidence for noise
        reasoning = "Tickets lack strong semantic similarity (outliers)."
    else:
        cluster_name = f"Cluster {cluster_label}"
        reasoning = f"Cluster keywords mapped to {root_cause} pattern."

    return {
        "cluster_name": cluster_name,
        "cluster_label": cluster_label, # Needed for filtering
        "stage": stage,
        "root_cause": root_cause,
        "confidence_score": confidence, # Raw float for logic checks
        "confidence": f"{int(confidence * 100)}%", # String for display
        "ticket_count": len(tickets),
        "reasoning": reasoning
    }