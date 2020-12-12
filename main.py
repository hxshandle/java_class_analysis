from fastapi import FastAPI
from pydantic import BaseModel
from java_class_analysis.lib import analysis, plantuml

app = FastAPI()

analyzer = analysis.Analyzer(r"/data/workspace/tmp/trunk", enable_method_filter=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}


class QueryModel(BaseModel):
    name: str
    method: str = None


@app.post("/query")
async def query(q: QueryModel):
    global analyzer
    arr = analyzer.parse(q.name)
    mindmap = plantuml.mind_diagram(arr[0])
    sequence_diagram = plantuml.sequence_diagram(arr[0])
    ret = dict()
    ret['mindmap'] = mindmap
    ret['sequence'] = sequence_diagram
    return ret


