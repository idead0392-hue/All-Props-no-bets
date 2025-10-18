from cfb_prop_predictor.types import GatheredData, AnalysisOutput

def analyze(data: GatheredData, prop_type: str) -> AnalysisOutput:
    """Analyzes the gathered data to produce key metrics and risk factors."""
    print("[Analyzer] Analyzing gathered data...")

    key_metrics = {}
    risks = []

    # Analyze Player Stats (if available)
    if data.player_stats:
        key_metrics['player_name'] = data.player_stats.name
        # NOTE: This is a placeholder until historical data is integrated
        key_metrics['season_average_placeholder'] = "Historical player data not yet implemented."

    # Analyze Odds Data (if available)
    if data.odds_data:
        key_metrics['prop_line'] = data.odds_data.prop_line
    else:
        risks.append("Could not retrieve live betting odds for this prop.")

    # Analyze Team Stats (if available)
    if data.team_stats:
        key_metrics['opponent_defensive_rank_placeholder'] = data.team_stats.defensive_rank
        if data.team_stats.defensive_rank <= 25:
            risks.append(f"Facing a strong defense (ranked #{data.team_stats.defensive_rank}).")

    if not risks:
        risks.append("No major risk factors identified.")

    summary = f"Analysis for {prop_type}. Betting line is {key_metrics.get('prop_line', 'N/A')}."

    return AnalysisOutput(
        key_metrics=key_metrics,
        risk_factors=risks,
        summary=summary
    )


