from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="CurioSync Dashboard Proof")

# Configure templates and static folders
templates = Jinja2Templates(directory="templates")

# Mock database records
items_db = [
    {"id": 1, "title": "Understanding C Pointers", "category": "Core"},
    {"id": 2, "title": "COVID-19 Remote Learning Reflects", "category": "Data"},
    {"id": 3, "title": "TensorFlow CNN Hand Gestures", "category": "AI/ML"},
    {"id": 4, "title": "Snowflake Sales Star Schema", "category": "Data Engineering"},
    {"id": 5, "title": "CurioSync Pipeline Automation", "category": "DevOps/AI"},
]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Renders the index dashboard using Jinja2 templates.
    """
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Dev-Root-Affinity Live Node", "items": items_db}
    )

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    Dynamic routing endpoint to view specific learning items.
    """
    for item in items_db:
        if item["id"] == item_id:
            return {"status": "success", "item": item}
    return {"status": "error", "message": "Item not found"}
