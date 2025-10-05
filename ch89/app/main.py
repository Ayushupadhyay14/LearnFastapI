from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def write_notification(email: str, message: str = ""):
  with open("log.txt", mode="w") as email_file:
    content = f"notification for {email} : {message}"
    email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
  background_tasks.add_task(write_notification, email, message="some notification by geekyshows")
  return {"message": "Notification sent !!"}

