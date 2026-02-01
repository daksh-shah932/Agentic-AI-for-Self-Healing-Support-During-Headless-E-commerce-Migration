def analyze_signal_trend(signal_data):
    """
    REASON (Predictive): Analyzes time-series data to predict near-term outcomes.
    """
    history = signal_data.get('history', [])
    if len(history) < 2:
        return "Insufficient Data", "Monitor"

    # Simple derivative/trend logic
    start = history[0]
    end = history[-1]
    diff = end - start
    
    trajectory = "Stable"
    prediction = "No change expected in ticket volume."

    if diff > 10:
        trajectory = "Rapid Escalation (Critical)"
        prediction = "Expect surge in high-priority tickets within 15-30 minutes."
    elif diff > 0:
        trajectory = "Rising Trend"
        prediction = "Minor increase in support volume likely."
    elif diff < 0:
        trajectory = "Recovering"
        prediction = "Incident potentially resolving; ticket volume should taper."

    return trajectory, prediction