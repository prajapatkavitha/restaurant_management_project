from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import ContactFormSubmission
from .serializers import ContactFormSubmissionSerializer

class ContactFormSubmissionCreateAPIView(generics.CreateAPIView):
    """
    API view for submitting a new contact form.
    Only allows POST requests to create a new submission.
    """
    queryset = ContactFormSubmission.objects.all()
    serializer_class = ContactFormSubmissionSerializer
    permission_classes = [AllowAny]
