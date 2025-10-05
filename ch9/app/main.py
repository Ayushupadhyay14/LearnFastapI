from fastapi import FastAPI

app = FastAPI()

# :path convertor
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"You requested file at path": file_path}