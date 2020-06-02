# FastAPI Dynamic Routing & Jinja2 Integration

FastAPI makes it straightforward to build API endpoints that return interactive HTML pages instead of raw JSON data by integrating Jinja2 templates.

## Configuration & Key Components

1. **Jinja2Templates**: Manages the templates directory path.
   ```python
   from fastapi.templating import Jinja2Templates
   templates = Jinja2Templates(directory="templates")
   ```

2. **HTMLResponse & TemplateResponse**: Renders the HTML template file with dynamic context parameters.
   ```python
   @app.get("/", response_class=HTMLResponse)
   async def home(request: Request):
       return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})
   ```
   *Note*: The `request` object is a mandatory key in the template context dictionary for FastAPI's template rendering to function properly.

3. **Dynamic Path Parameters**: Extracting variables from the URL path.
   ```python
   @app.get("/items/{item_id}")
   async def read_item(item_id: int):
       return {"item_id": item_id}
   ```

## Reference Code File
The full routing setup demonstrating both page rendering and dynamic endpoints can be reviewed in the source folder: [fastapi_app.py](file:///G:/dev-root-affinity/src/2026/fastapi_app.py).

---
*Logged on 2025-01-13 18:28:00 (UTC)*
