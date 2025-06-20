from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()

@app.get("/")
def read_root():
    """
    root endpoint of the API, returning static part of website
    """
    return FileResponse("app/static/index.html")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/data")
def click_button():
    html_content = "<h2>Here is your new content!</h2><p>It was loaded successfully from the server.</p>"
    return HTMLResponse(content=html_content)
