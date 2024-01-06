# model.py file for inventory app. 
from django.db import models
from django.contrib.auth.models import User  # Import User model
from .storage_backends import AWSStorageBackend

# Create your models here.
class InventoryItem(models.Model):
    """
    Represents an inventory item with its associated image, label, timestamp, and user.
    """
    label = models.CharField(max_length=255) # to store the inventory classification label.
    filename = models.CharField(max_length=255) # to store the image filename in S3.
    timestamp = models.DateTimeField(auto_now_add=True) # to automatically record the data and time of item creation. Although this is automated by using objects.create()
    user = models.ForeignKey(User, on_delete=models.CASCADE) # to associate the item with the user who uploaded it (once you implement user sign-in)

    def upload_image(self, image):
        """
        Uploads the image to S3, stores the filename, and creates a DynamoDB entry.

        Args:
            image: The image file to be uploaded.

        Raises:
            Exception: If any errors occur during S3 or DynamoDB operations.
        """
        storage_backend = AWSStorageBackend() # creates instance of the storage backend class to interact with S3 and DynamoDB. 
        filename = storage_backend.upload_file(image) # uploads the provided image to S3 and returns the generated filename
        self.filename = filename # stores the S3 filename in the model instance
        self.save() # persists the updated model instance with the filename in the data base

        storage_backend.create_inventroy_item({
            'filename': self.filename,
            'label': self.label,
            'timestamp': self.timestamp.date(), # format timestamp for DynamoDB
            'user_id': self.user.id # store user ID in DynamoDB
        })


