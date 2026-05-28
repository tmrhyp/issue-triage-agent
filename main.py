from fastapi import FastAPI
from agent import build_graph

app = FastAPI()
graph = build_graph()

@app.get("/")
def root():
    return {"status": "Agent ready"}

@app.post("/triage")
def triage(repo: str):
    result = graph.invoke({"repo": repo, "result": ""})
    return {"result": result["result"]}
