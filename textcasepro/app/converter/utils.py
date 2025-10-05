import secrets

def generate_api_key():
  return secrets.token_urlsafe(32)

def convert_text(text: str, operation: str):
  if operation == "upper":
    return text.upper()
  elif operation == "lower":
    return text.lower()
  else:
    raise ValueError("Invalid operation: Use 'lower' or 'upper'")