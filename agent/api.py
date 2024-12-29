from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from process import process_map
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="D&D Game Master API",
    description="API for processing D&D battle maps and generating NPC actions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post(
    "/process-map",
    response_model=Dict[str, Any],
    summary="Process battle map",
    description="""
    Takes a map information with characters and generates the next NPC action.
    
    The map_info should contain:
    - map: Dictionary with description of the battle map
    - characters: List of characters with their descriptions
    
    Returns:
    - message: Generated action description
    - data: Updated map information
    """
)
async def process_map_endpoint(map_info: Dict[str, Any]) -> Dict[str, Any]:
    try:
        result = process_map(map_info)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(
    "/health",
    summary="Health check",
    description="Returns the health status of the API",
    response_model=Dict[str, str]
)
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8077)
