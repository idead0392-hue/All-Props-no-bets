from cfb_prop_predictor.agents.data_gatherer import gather_data
from cfb_prop_predictor.agents.analyzer import analyze
from cfb_prop_predictor.agents.predictor import predict
from cfb_prop_predictor.types import CFBPropResult
import asyncio

async def run_cfb_prop_workflow(request: dict) -> dict:
    """Orchestrates the data gathering, analysis, and prediction workflow."""
    
    # Step 1: Gather Data
    gathered = await gather_data(
        game=request['game'],
        player=request.get('player'),
        prop_type=request['prop_type']
    )
    
    # Step 2: Analyze Data
    analysis = analyze(gathered, request['prop_type'])
    
    # Step 3: Generate Prediction
    prediction = predict(analysis)
    
    # Assemble the final result
    result = CFBPropResult(
        prediction=prediction,
        analysis=analysis,
        gathered_data=gathered
    )
    
    return result.dict()

def run_workflow_sync(request: dict) -> dict:
    """Synchronous wrapper for running the async workflow."""
    return asyncio.run(run_cfb_prop_workflow(request))


