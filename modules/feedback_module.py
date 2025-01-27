def generate_feedback(efficiency):
    if efficiency > 95:
        return "Excellent cutting efficiency! Minimal waste achieved."
    elif efficiency > 85:
        return "Good efficiency, but there's room for improvement."
    else:
        return "Significant waste detected. Review cutting patterns for better results."
