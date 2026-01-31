from agent import observe, embed, cluster, reason, decide

def generate_global_insight(all_analyses):
    """
    ACT (Global): triggers alerts ONLY if strict criteria are met.
    """
    print("\n" + "="*60)
    print("GLOBAL SYSTEM HEALTH CHECK")
    print("="*60)
    
    severe_alerts = []
    
    for a in all_analyses:
        # --- UPDATED GLOBAL ALERT LOGIC ---
        # 1. Ignore Noise (-1)
        # 2. Ignore small clusters (< 3 tickets)
        # 3. Must be Stage 3 (Live)
        # 4. Must have High Confidence (>= 0.7)
        # 5. Must be a Platform Issue
        if (a['cluster_label'] != -1 and 
            a['ticket_count'] >= 3 and
            "Stage 3" in a['stage'] and
            a['confidence_score'] >= 0.7 and 
            "Platform" in a['root_cause']):
            
            severe_alerts.append(a)

    if severe_alerts:
        print(f"🚨 CRITICAL ALERT: {len(severe_alerts)} Verified Production Outage(s) Detected.")
        print("   Logic: High-confidence clusters matching Stage 3 regression patterns.")
        print("   RECOMMENDATION: FREEZE DEPLOYMENTS & PAGE ON-CALL ENGINEERING.")
    else:
        # Fallback for standard insights
        print("✅ STATUS: Operational. No critical platform outages detected.")
        print("   NOTE: Monitoring standard support volume.")

def main():
    print("=== STARTING AGENTIC SUPPORT OPERATIONS MANAGER ===\n")

    # 1. OBSERVE
    tickets = observe.load_tickets()

    # 2. REASON (Part A: Vectorize & Cluster)
    embeddings = embed.generate_embeddings(tickets)
    clusters = cluster.cluster_tickets(tickets, embeddings)

    # List to store analysis for the Global Insight step
    all_cluster_analyses = []

    print("\n--- DETAILED CLUSTER REPORTS ---\n")

    # Iterate through ALL clusters (including Noise/-1)
    for label, cluster_tickets in clusters.items():
        
        # 2. REASON (Part B: Inference)
        # We pass the label to handle the "Noise" cluster logic inside reason.py
        analysis = reason.analyze_cluster(label, cluster_tickets)

        # 3. DECIDE
        decision = decide.determine_action(analysis)

        # 4. EXPLAIN (Output)
        print(f"[{analysis['cluster_name']}] ({analysis['ticket_count']} tickets)")
        print(f"  • Inferred Stage:  {analysis['stage']}")
        print(f"  • Root Cause:      {analysis['root_cause']}")
        print(f"  • Confidence:      {analysis['confidence']}")
        print(f"  • Risk Level:      {decision['risk_level']}")
        print(f"  • ACTION:          {decision['recommended_action']}")
        print("-" * 40)
        
        # Save for global insight
        all_cluster_analyses.append(analysis)

    # 5. GLOBAL ACT
    generate_global_insight(all_cluster_analyses)

if __name__ == "__main__":
    main()