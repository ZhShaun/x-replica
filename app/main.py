from fastapi import FastAPI, Request,  Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated

templates = Jinja2Templates(directory="app/templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def read_root():
    """
    root endpoint of the API, returning static part of website
    """
    return RedirectResponse(url="static/index.html")

@app.get("/modal", response_class=HTMLResponse)
def get_modal(request: Request):
    context = {"request": request, "modal_title": "今日の質問", "modal_body": "最近読んだ本は何ですか？"}
    return templates.TemplateResponse("modal_content.html", context)

@app.post("/submit-modal-form", response_class=HTMLResponse)
async def submit_modal_form(
    user_name: Annotated[str, Form()],
    user_message: Annotated[str, Form()]
):
    """
    Endpoint to handle form submission from the modal.
    """
    print("Received form submission:")
    print(f"  Name: {user_name}")
    print(f"  Message: {user_message}")

    # --- Simulate some backend processing ---
    success = True # In a real app, this would depend on DB save, validation, etc.

    if success:
        # Construct the response message for inside the modal
        response_html = f"""
        <div class="alert alert-success" role="alert">
            Thank you, <strong>{user_name}</strong>! Your message has been received.
        </div>
        """
        # Send an HTMX-Trigger header to tell the client to close the modal
        # The 'closeModal' event will be listened for in JavaScript
        return Response(content=response_html, headers={"HX-Trigger": "closeModal"})
    else:
        response_html = """
        <div class="alert alert-danger" role="alert">
            Oops! Something went wrong. Please try again.
        </div>
        """
        return HTMLResponse(content=response_html, status_code=400) 
