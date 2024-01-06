import boto3
from botocore.config import Config
import os
import uuid

from boto3.dynamodb import resource
from django.http import HttpResponse
from .models import InventoryItem



class AWSStorageBackend:
    """Handles interactions with AWS S3 and DynamoDB for image storage and metadata management."""   
    def __init__(self) -> None:
             """Initializes the S3 and DynamoDB clients using environment variables for credentials."""
             self.s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
             self.dynamodb_client = boto3.client('dynamodb')
             
             # Set bucket and table names from environment variables
             self.bucket_name = os.environ['S3_BUCKET_NAME'] # user image bucket
             self.table_name = os.environ['DYNAMODB_TABLE_NAME'] # image label bucket

    def upload_file(self, file):
        """Uploads a file to S3 and returns the generated filename."""
        filename = f'images/{uuid.uuid4()}{os.path.splitext(file.name)[1]}'
        try:
            self.s3_client.upload_fileobj(file, self.bucket_name, filename)
            return filename
        except Exception as e:
            raise Exception(f'Error uploading file to S3: {e}')
    
    def create_inventroy_item(self, item_data):
        """Creates an item in the DynamoDB table with the provided data."""
        try:
            self.dynamodb_client.put_item(TableName=self.table_name, Item=item_data)
        except Exception as e:
            raise Exception(f'Error creating item in DynamoDB: {e}')






