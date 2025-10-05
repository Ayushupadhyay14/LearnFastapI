from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from typing import Annotated
import os
import shutil

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def get_form():
    return """
    <html>
        <head>
            <title>User Profile Upload</title>
        </head>
        <body>
            <h2>User Profile Form</h2>
            <form action="/user-with-file/" enctype="multipart/form-data" method="post">
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username" required><br><br>
                <label for="file">Profile Picture (optional):</label><br>
                <input type="file" id="file" name="file" accept="image/*"><br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """
@app.post("/user-with-file/")
async def create_user_with_file(
    username: Annotated[str, Form()],
    file: Annotated[UploadFile | None, File()] = None
):
    response = {"username": username}
    if file:
        save_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        response["filename"] = file.filename
    return response



