import os
import boto3
from dotenv import load_dotenv

load_dotenv()

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

response = s3.list_objects_v2(Bucket=bucket_name)

print("Connected to s3 successfully")
print("Bucket name:", bucket_name)
print("Aws region:", aws_region)
print("Object count:", response.get("KeyCount", 0))
