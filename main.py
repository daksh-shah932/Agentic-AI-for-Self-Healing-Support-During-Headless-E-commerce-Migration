import json
import traceback  # FIX: Added missing import
from agent import observe, embed, cluster, reason, decide  # FIX: Added missing agent imports
from agent import llm_mock, counterfactual, trajectory, repro_pack

# --- HELPER TO SAVE RESULTS ---
def save_analysis_to_disk(data, filename="analysis_output.json"):
    """Saves the processed agent results for the frontend to read."""
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"--> [SYSTEM] Success! Analysis saved to {filename}")
    except Exception as e:
        print(f"--> [ERROR] Failed to save analysis: {e}")

def generate_restraint_logic(risk_level, confidence):
    """DECIDE (Restraint): Explicitly explains what the agent WON'T do."""
    try:
        conf_val = float(confidence)
    except:
        conf_val = 0.5

    if risk_level == "High":
        return {
            "action_not_taken": "Auto-Rollback of API Deployment",
            "reason": "Risk is Critical, but human approval is required."
        }
    elif conf_val < 0.8:
        return {
            "action_not_taken": "Auto-Email Blast to Merchants",
            "reason": f"Confidence ({conf_val}) is below 0.8 threshold."
        }
    else:
        return {
            "action_not_taken": "Escalation to VP Engineering",
            "reason": "Issue severity does not meet SLA for executive wake-up."
        }

def main():
    print("=== STARTING AGENTIC RUN ===\n")

    try:
        # 1. OBSERVE
        print("--> Step 1: Loading Data...")
        tickets = observe.load_tickets()
        raw_signals = observe.load_system_signals()

        # --- SIGNAL ADAPTER (FIX FOR NEW JSON FORMAT) ---
        # This converts your history-based JSON into the single-signal format
        # expected by the trajectory analyzer.
        if "checkout_error_rate_history" in raw_signals:
            history = raw_signals["checkout_error_rate_history"]
            signals = {
                "signal": "checkout_error_rate",
                "current_value": history[-1] if history else 0, # Take the last value
                "history": history,
                "time_window": "15min"
            }
        else:
            # Fallback for old format or empty
            signals = raw_signals
        # ------------------------------------------------

        # 2. VECTORIZE & CLUSTER
        print("--> Step 2: Clustering...")
        embeddings = embed.generate_embeddings(tickets)
        clusters = cluster.cluster_tickets(tickets, embeddings)

        # 3. ANALYZE TRAJECTORY
        print("--> Step 3: Analyzing Trajectory...")
        traj_label, prediction = trajectory.analyze_signal_trend(signals)
        trend_info = {"trajectory": traj_label, "prediction": prediction}

        # DATA CONTAINER FOR FRONTEND
        frontend_data = []

        # 4. AGENT LOOP
        print("--> Step 4: Reasoning Loop...")
        for label, cluster_tickets in clusters.items():
            if label == -1: continue 

            print(f"    - Processing Cluster {label} ({len(cluster_tickets)} tickets)...")
            
            try:
                cluster_text = " ".join([t['message'] for t in cluster_tickets])
                
                # Reason & Decide
                llm_analysis = llm_mock.analyze_cluster_semantically(cluster_text)
                decision = decide.determine_action(llm_analysis)
                restraint = generate_restraint_logic(decision['risk_level'], llm_analysis['confidence'])
                
                # Check for Repro Pack
                repro_data = None
                conf_val = float(llm_analysis.get('confidence', 0))
                is_stage_3 = "Stage 3" in llm_analysis.get('stage', '')
                is_platform_issue = "Platform Issue" in llm_analysis.get('root_cause', '')

                if is_stage_3 and is_platform_issue and conf_val >= 0.8:
                     path, inc_id, r_type, triggers = repro_pack.generate_repro_pack(
                        llm_analysis, cluster_tickets, signals
                    )
                     repro_data = {"id": inc_id, "type": r_type, "triggers": triggers}

                # CONSTRUCT FRONTEND OBJECT
                cluster_obj = {
                    "id": f"CL-{label}",
                    "title": f"Cluster {label}: {llm_analysis['root_cause']}",
                    "stage": llm_analysis['stage'],
                    "root_cause": llm_analysis['root_cause'],
                    "confidence": llm_analysis['confidence'],
                    "risk": decision['risk_level'],
                    "ticket_ids": [t['ticket_id'] for t in cluster_tickets],
                    "merchants": list(set([t['merchant_id'] for t in cluster_tickets])),
                    "timeline": {
                        "Observe": f"Clustered {len(cluster_tickets)} tickets via DBSCAN.",
                        "Reason": llm_analysis.get('reasoning', 'Analyzed patterns.'),
                        "Decide": decision['recommended_action'],
                        "Act": "Repro Pack Generated" if repro_data else "internal_ticket_created"
                    },
                    "restraint": restraint,
                    "repro_pack": repro_data
                }
                frontend_data.append(cluster_obj)
            except Exception as e:
                print(f"    [ERROR] Failed processing Cluster {label}: {e}")
                traceback.print_exc()

        # 5. SAVE FOR DASHBOARD
        print(f"--> Step 5: Saving {len(frontend_data)} clusters to disk...")
        save_analysis_to_disk(frontend_data)
        
    except Exception as e:
        print("\nCRITICAL FAILURE IN MAIN LOOP:")
        print(e)
        traceback.print_exc()

if __name__ == "__main__":
    main()