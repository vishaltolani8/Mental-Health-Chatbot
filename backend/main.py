#step1 Setup FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ai_agent import run_agent
from tools import query_medgemma, call_emergency    

app = FastAPI()

#Step2 Recience and validate requests from frontend
class Query(BaseModel):
    message: str


@app.post("/ask")
async def ask(request: Query):
    # AI Agent
    tool_called_name, final_response = run_agent(request.message)

    # Step 3: Send response back to frontend
    return {
        "response": final_response,
        "tool_called": tool_called_name
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
