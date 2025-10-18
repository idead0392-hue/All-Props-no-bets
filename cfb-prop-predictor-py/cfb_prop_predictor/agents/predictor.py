from cfb_prop_predictor.types import AnalysisOutput, PredictionOutput

def predict(analysis: AnalysisOutput) -> PredictionOutput:
    """Generates a final prediction based on the analysis."""
    print("[Predictor] Generating prediction...")

    prop_line = analysis.key_metrics.get('prop_line', 0.0)
    
    # NOTE: This is a placeholder until real projections are implemented
    projected_value = float(prop_line) * 1.05  # Simple projection: 5% over the line
    
    edge = projected_value - float(prop_line)
    
    # Determine confidence
    confidence = 65
    if "strong defense" in " ".join(analysis.risk_factors):
        confidence -= 15
    if abs(edge) < float(prop_line) * 0.05: # Lower confidence if edge is small
        confidence -= 10

    # Determine recommendation
    if confidence < 50:
        recommendation = "avoid"
    else:
        recommendation = "over" if edge > 0 else "under"

    return PredictionOutput(
        recommended_bet=recommendation,
        projected_value=round(projected_value, 2),
        edge=round(edge, 2),
        confidence=int(confidence)
    )


