import json
import os
import time
import datetime
import uuid  # FIX 1: Import UUID

def generate_repro_pack(analysis, tickets, system_signals):
    """
    ACT (Engineering Handoff): Generates a JSON artifact for engineers.
    Now supports unique IDs and preliminary vs full repro contexts.
    """
    timestamp = datetime.datetime.now().isoformat()
    
    # FIX 1: UNIQUE INCIDENT ID
    # Use 8-char UUID to guarantee uniqueness across clusters/runs
    unique_suffix = uuid.uuid4().hex[:8].upper()
    incident_id = f"INC-{unique_suffix}"
    
    # FIX 2: CLUSTER-SIZE AWARENESS
    # Determine if this is a "Preliminary" signal or a "Full" repro
    cluster_size = len(tickets)
    is_preliminary = cluster_size < 5
    
    repro_type = "preliminary" if is_preliminary else "full"
    
    # 1. Extract Merchant Context
    merchant_ids = list(set([t.get('merchant_id') for t in tickets]))
    
    # 2. Infer Endpoints
    combined_text = " ".join([t['message'].lower() for t in tickets])
    endpoints = []
    if "checkout" in combined_text: endpoints.append("POST /api/v1/checkout")
    elif "payment" in combined_text: endpoints.append("POST /api/v1/payments")
    elif "cart" in combined_text: endpoints.append("POST /api/v1/carts")
    else: endpoints.append("GET /api/status (Fallback)")

    # 3. Extract Errors
    error_samples = set()
    for t in tickets:
        msg = t['message']
        if "500" in msg or "error" in msg.lower() or "timeout" in msg.lower():
            error_samples.add(msg[:120])
            
    # 4. Generate Repro Steps (Adaptive)
    target_endpoint = endpoints[0] if endpoints else "affected endpoint"
    
    if is_preliminary:
        repro_steps = [
            "NOTE: EARLY SIGNAL (Low Volume). Steps are heuristic.",
            f"1. Check logs for merchants: {merchant_ids}.",
            f"2. Monitor {target_endpoint} for latency spikes.",
            "3. Attempt manual reproduction using sample payload."
        ]
    else:
        repro_steps = [
            f"1. Authenticate as one of the affected merchants (e.g., {merchant_ids[0] if merchant_ids else 'ID 101'}).",
            f"2. Construct a standard payload for {target_endpoint}.",
            f"3. Send request and monitor for HTTP 500 or Timeout > 5000ms.",
            "4. Correlate request ID with system logs."
        ]

    # FIX 3: EXPLICIT TRIGGER REASONS
    trigger_reasons = [
        "High confidence platform regression",
        "Production environment (Stage 3)"
    ]
    if not is_preliminary:
        trigger_reasons.append(f"Significant cluster size ({cluster_size} tickets)")
    if len(merchant_ids) > 1:
        trigger_reasons.append("Multiple merchants affected")

    # 5. Assemble the Pack Dictionary
    repro_data = {
        "incident_id": incident_id,
        "repro_type": repro_type,          # NEW FIELD
        "repro_trigger_reason": trigger_reasons, # NEW FIELD
        "suspected_stage": analysis.get('stage'),
        "suspected_root_cause": analysis.get('root_cause'),
        "confidence": analysis.get('confidence'),
        "affected_merchants": merchant_ids,
        "affected_endpoints": endpoints,
        "sample_error_messages": list(error_samples),
        "repro_steps": repro_steps,
        "sample_payload": {
            "items": [{"id": "sku_123", "qty": 1}], 
            "currency": "USD",
            "context": "generated_by_agent"
        },
        "system_context": {
            "signal_name": system_signals.get('signal', 'N/A'),
            "current_value": system_signals.get('current_value', 'N/A'),
            "trend": "High/Critical"
        },
        "generated_at": timestamp
    }

    # 6. Save to Disk
    output_dir = "repro_packs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filepath = os.path.join(output_dir, f"{incident_id}.json")
    with open(filepath, 'w') as f:
        json.dump(repro_data, f, indent=2)

    return filepath, incident_id, repro_type, trigger_reasons