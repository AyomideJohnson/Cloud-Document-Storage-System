from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import boto3
import os

load_dotenv()

app = FastAPI()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access = os.getenv("AWS_SECRET_ACCESS_KEY")
bucket_name = os.getenv("AWS_BUCKET_NAME")
aws_region = os.getenv("AWS_REGION")

s3= boto3.client(
    "s3",
    aws_access_key_id = aws_access_key, 
    aws_secret_access_key  = aws_secret_access, 
    region_name = aws_region
    )

@app.get("/")
def home():
    return {"message": "Cloud Document Storage API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    s3.upload_fileobj(
        file.file,
        bucket_name,
        file.filename            
    )
    return {"message": "file uploaded successfully",
            "filename": file.filename}