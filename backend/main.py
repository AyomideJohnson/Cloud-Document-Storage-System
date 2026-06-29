from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
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

@app.get("/files")
def receive_files():
    response = s3.list_objects_v2(Bucket=bucket_name)
    files = []
    for item in response.get("Contents", []):
        files.append(item["Key"])
    return{"message":"files retrieved",
           "files": files}

@app.get("/files/{filename}")
def download_file(filename: str):
    response = s3.get_object(
        Bucket = bucket_name, 
        Key = filename     
    )
    return StreamingResponse(
        response["Body"],
        media_type=response["ContentType"],
        headers={
        "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )
@app.delete("/files/{filename}")
def delete_file(filename: str):
    s3.delete_object(
        Bucket = bucket_name, 
        Key = filename  
    )
    return {"message": "file has been deleted", "filename": filename}