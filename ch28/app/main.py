from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from typing import Annotated
from pydantic import BaseModel, Field
app = FastAPI()

# # Simple HTML form for testing
@app.get("/", response_class=HTMLResponse)
async def get_form():
    return """
    <html>
        <body>
            <h2>Login Form</h2>
            <form action="/login/" method="post">
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username"><br>
                <label for="password">Password:</label><br>
                <input type="password" id="password" name="password"><br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """
## Pydantic Models for Forms
class FormData(BaseModel):
    username: str
    password: str

# Pydantic Models for Forms with Validation
# class FormData(BaseModel):
#     username: str = Field(min_length=3)
#     password: str = Field(min_length=3, max_length=20)

# # Pydantic Models for Forms with Validation
# class FormData(BaseModel):
#     username: str = Field(min_length=3)
#     password: str = Field(min_length=3, max_length=20)
#     model_config = {"extra": "forbid"}

@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
