class CustomLoggingMiddleware:
  def __init__(self, app, prefix="LOG"):
    self.app = app
    self.prefix = prefix

  async def __call__(self, scope, receive, send):
    print(f"{self.prefix}: Before processing request (scope: {scope['type']})")
    await self.app(scope, receive, send)
    print(f"{self.prefix}: After processing request")

    
    