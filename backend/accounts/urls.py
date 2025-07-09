from django.urls import path
from .views.auth_views import IdentitySubmissionView

app_name = 'accounts'

urlpatterns = [
    path('submit-identity/', IdentitySubmissionView.as_view(), name='submit_identity'),
]