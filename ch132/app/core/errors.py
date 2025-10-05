from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.log_config import logger

async def validation_exception_handler(request: Request, exc: RequestValidationError):
  logger.warning(f"Validation error: {exc.errors()} - URL: {request.url}")
  return JSONResponse(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    content={"message": "Invalid input. Please check your data."}
  )

async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc} - URL: {request.url}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Something went wrong. Please try again later."},
    )