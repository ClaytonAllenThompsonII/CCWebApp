from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import InventoryItem
from .storage_backends import AWSStorageBackend

from django.utils.logging import get_logger


# Use the logger within your view
logger = get_logger(__name__)

@csrf_exempt
def upload_image(request):

    if request.method == 'POST':
        # Get the uploaded image file and selected label from request
        image = request.FILES.get('image')
        label = request.POST.get('label')

        # Check if image  or label is present
        if not image or not label:
            return JsonResponse({'error', 'Missing image or label'}, status=400)
        
        # create model instance
        item = InventoryItem.objects.create(label=label, user=request.user) # assign logged-in user 

        # Handle image upload and DynamoDB entry
        try:
            item.upload_image(image)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        response_data = {
            'message': 'Image uploaded successfully!',
            'filename': item.filename,
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)