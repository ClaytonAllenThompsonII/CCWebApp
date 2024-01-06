from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import InventoryItem

@csrf_exempt
def upload_image(request):
    """
    Handles the image upload request.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the result of the image upload.
    """
    if request.method == 'POST':
        # Get the uploaded image file and selected label from request
        image = request.FILES.get('image')
        label = request.POST.get('label')

        # Check if image  or label is present
        if not image or not label:
            return JsonResponse({'error', 'Missing image or label'}, status=400)
        
          # Check if the user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)
        
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