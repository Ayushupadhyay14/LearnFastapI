from fastapi import  Request

# First Middleware
async def my_first_middleware(request: Request, call_next):
  print("1st Middleware: Before processing the request")
  response = await call_next(request)
  print("1st Middleware: After processing the request, before returning response")
  return response

# Second Middleware
async def my_second_middleware(request: Request, call_next):
  print("2nd Middleware: Before processing the request")
  response = await call_next(request)
  print("2nd Middleware: After processing the request, before returning response")
  return response