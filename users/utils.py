from django.conf import settings
from django.core.mail import EmailMultiAlternatives # Imports the class for sending emails with alternative content types.

def send_verification_email(user): # Defines the function for sending verification emails.
    """Sends a verification email to the user with a link to activate their account.

    This function constructs an email message containing a verification link
    and sends it to the user's email address using Django's email functionality.
    Args:
        user: The user object for whom to send the verification email.
    Raises:
        smtplib.SMTPException: If there's an error sending the email.
    Returns:
        None
    """

    subject = 'Verify your email address' #Sets the subject line of the email.
    text_content = f'Please click the link below to verify your email address:\n{settings.FRONTEND_URL}/verify-email/{user.verification_code}' #Creates the plain text content of the email, including a link to the verification URL.
    html_content = f'<p>Please click the link below to verify your email address:</p><p><a href="{settings.FRONTEND_URL}/verify-email/{user.verification_code}">Verify Email</a></p>' #Creates the HTML content of the email, providing a more visually appealing format for the verification link.
    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email]) # Creates an email message instance with the subject, plain text content, sender address, and recipient's email.
    msg.attach_alternative(html_content, 'text/html') #Attaches the HTML content as an alternative version of the email.
    msg.send() # Sends the email.


    # Could add error handling with try + except. Need to impliment logging if so. 

   