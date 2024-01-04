from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.logging import get_logger
from boto3.session import Session
from botocore.exceptions import ClientError
from botocore.config import Config
from boto3.dynamodb import resource
import os
import uuid

# Use the logger within your view
logger = get_logger(__name__)

@csrf_exempt
def upload_image(request):
    """
    Handle image upload requests.

    This view function receives POST requests containing the uploaded image file
    and selected inventory classification label in the 'image' and 'label' fields
    of the request body, respectively. It then saves the image to S3, stores the
    filename and label in DynamoDB, and returns a JSON response.

    Args:
        request: A Django HttpRequest object containing the uploaded image and label.

    Returns:
        A Django HttpResponse object with JSON response data.
    """

    if request.method == 'POST':
        # Get the uploaded image file
        image = request.FILES.get('image')

        # Check if image is present
        if not image:
            return HttpResponseBadRequest('Missing image file')

        # Get the selected label
        label = request.POST.get('label')

        # Check if label is present
        if not label:
            return HttpResponseBadRequest('Missing inventory classification label')

        # Get storage backend
        # Access AWS credentials from environment variables
        aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        region_name = os.environ['AWS_REGION_NAME']

        session = Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,)


        # create S3 client with signature version 's3V4'
        s3_client = session.client('s3', 'us-east-1',config=Config(signature_version='s3v4'))
        # generate unique filename
        filename = f'images/{uuid.uuid4()}{os.path.splitext(image.name)[1]}'

        # Upload image to s3 bucket
        try:
            s3_client.put_object(
                Bucket=os.environ['S3_BUCKET_NAME'],
                Key=filename,
                Body=image,
            )
        except ClientError as e:
        # handle S3-specific error
            logger.error(f'Error uploading image to S3: {e}')
            return HttpResponseServerError(f'Error uploading image to S3: {e}')
        except Exception as e:
            logger.error(f'Unexpected error uploading image:{e}')
            return HttpResponseServerError(f'Error uploading image: {e}')           

        
        # Create a DynamoDB client
        dynamodb = resource('dynamodb')     # DYNAMODB_TABLE_NAME = "your_table_name"
        table = dynamodb.Table('your_table_name')

        # Prepare item data
        item = {
            'filename': filename,
            'label': label,
            # Add any other relevant fields to the item
            # ...Time Stamp? User upload (when we add sign in)
        }

        # Save the item to DynamoDB
        try:
            table.put_item(Item=item)
        except ClientError as e
            logger.error(f'DynamoDB client error: {e}')
            # handle specific client errors
        except ResourceNotFoundError as e:
            logger.error(f'DynamoDB resource not found: {e}')
            #handle resource not found error
        except Exception as e:
            logger.error(f'Unexpected error saving item to DynamoDB':{e})
            # handle other unexpected errors

        # Prepare response data
        response_data = {
            'message': 'Image uploaded successfully!',
            'filename': filename,
            'url': s3_client.generate_presigned_url('get_object', Params={'Bucket': os.environ['S3_BUCKET_NAME'], 'Key': filename})
        }

        # Return JSON response
        return JsonResponse(response_data)

    else:
        return HttpResponseBadRequest('Invalid request method')