from django.urls import path
from .views.auth_views import IdentitySubmissionAPIView

app_name = 'accounts'

urlpatterns = [
    path('submit-identity/', IdentitySubmissionAPIView.as_view(), name='submit_identity'),
]