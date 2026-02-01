import json
import os

def load_tickets(filepath="tickets.json"):
    """
    OBSERVE: Reads the raw support tickets from the file system.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find {filepath}")
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    print(f"--> [OBSERVE] Loaded {len(data)} tickets.")
    return data

def load_system_signals(filepath="system_signals.json"):
    """
    OBSERVE (Phase 2): Reads simulated infrastructure signals.
    """
    if not os.path.exists(filepath):
        print(f"--> [OBSERVE] Warning: {filepath} not found. Skipping signals.")
        return {} # Return empty dict safely
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    # FIX: Use 'current_value' if 'value' doesn't exist (handles new schema)
    val = data.get('current_value', data.get('value', 'N/A'))
    
    print(f"--> [OBSERVE] Loaded system signal: {data.get('signal')} ({val}%)")
    return data