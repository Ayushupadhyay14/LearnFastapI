import os
from uuid import uuid4
from fastapi import HTTPException, UploadFile
from decouple import config
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from botocore.client import Config

# DigitalOcean Spaces configuration
AWS_S3_ACCESS_KEY_ID = config("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY= config("AWS_S3_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT_URL = config("AWS_S3_ENDPOINT_URL")
AWS_S3_CUSTOM_DOMAIN = config("AWS_S3_CUSTOM_DOMAIN")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_REGION_NAME = config("AWS_REGION_NAME")

# Initialize boto3 client for DigitalOcean Spaces
session = boto3.session.Session()
s3_client = session.client(
    's3',
    endpoint_url=AWS_S3_ENDPOINT_URL,
    aws_access_key_id=AWS_S3_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY,
    config=Config(s3={'addressing_style': 'virtual'}),
    region_name=AWS_REGION_NAME
)

# Transfer configuration for efficient uploads
TRANSFER_CONFIG = TransferConfig(
    multipart_threshold=5 * 1024 * 1024,  # Use multipart for files > 5MB
    multipart_chunksize=5 * 1024 * 1024,  # 5MB chunks
    max_concurrency=4,  # Parallel uploads for multipart
    use_threads=True
)

async def save_upload_file(upload_file: UploadFile, sub_dir: str) -> str:
  try:
    # Validate file type
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "application/pdf"]
    if upload_file.content_type not in allowed_types:
       raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Check file size
    file_size = upload_file.size
    if file_size is None:
       raise HTTPException(status_code=400, detail="Could not determine file size")
    if file_size > 10 * 1024 * 1024: # Limit to 10MB max (adjust as needed)
       raise HTTPException(status_code=400, detail="File too large")
    
    # Ensure file pointer is at the start
    await upload_file.seek(0)

    # Generate a unique filename
    ext = os.path.splitext(upload_file.filename)[-1]
    filename = f"{uuid4().hex}{ext}"
    file_path = f"{sub_dir}/{filename}"

    # Upload file to DigitalOcean Spaces
    s3_client.upload_fileobj(
       Fileobj = upload_file.file,
       Bucket = AWS_STORAGE_BUCKET_NAME,
       Key = file_path,
       ExtraArgs = {'ACL': 'public-read', 'ContentType': upload_file.content_type},
       Config = TRANSFER_CONFIG
    )
    return file_path

  except ClientError as e:
    raise HTTPException(status_code=500, detail=f"Failed to upload file to Spaces: {str(e)}")
  except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")
  
def get_file_url(file_path: str) -> str:
   return f"{AWS_S3_CUSTOM_DOMAIN}/{file_path}"
  
