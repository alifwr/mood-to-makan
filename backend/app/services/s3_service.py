import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import UploadFile, HTTPException
import uuid
from app.core.config import settings

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            endpoint_url=settings.S3_ENDPOINT_URL
        )
        self.bucket_name = settings.S3_BUCKET_NAME
        self.base_url = settings.S3_BASE_URL

    def upload_file(self, file: UploadFile, folder: str = "uploads") -> str:
        if not settings.S3_ACCESS_KEY or settings.S3_ACCESS_KEY == "change_me":
             # Mock upload for development if no keys provided
             return f"https://mock-s3.com/{folder}/{file.filename}"

        try:
            file_extension = file.filename.split(".")[-1]
            file_name = f"{folder}/{uuid.uuid4()}.{file_extension}"
            
            self.s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                file_name,
                ExtraArgs={'ACL': 'public-read', 'ContentType': file.content_type}
            )
            
            return f"{self.base_url}/{self.bucket_name}/{file_name}"
        except (NoCredentialsError, ClientError) as e:
            print(f"S3 Upload Error: {e}")
            raise HTTPException(status_code=500, detail="Could not upload image")

s3_service = S3Service()
