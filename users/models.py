""" Defines models for managing user data.
This module utilizes Django's ORM to create and interact with user-related data in the database.
Key classes:
    - UserProfile: Represents a user in the system.
Dependencies:
    - Django (models module)
"""
from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

class Profile(models.Model):
    """
    Represents a user in the system.

    Attributes:
        - firstname (str): The user's first name.
        - lastname (str): The user's last name.
        - phone (int, optional): The user's phone number.
        - joined_date (date, optional): The date the user joined.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, auto_created=True, primary_key=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)
    


    def __str__(self):
        if self.user:
            return f'{self.user.username} Profile'
        else:
            return f'Profile without user ({self.pk})'
        
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)

            # Save the image back to the same field
            img_io = BytesIO()
            img.save(img_io, format='JPEG')
            img_file = InMemoryUploadedFile(
                img_io, None, 'profile_pics/' + self.image.name, 'image/jpeg', img_io.tell(), None
            )
            self.image = img_file
            super(Profile, self).save(*args, **kwargs)


        