from django.urls import path, include

app_name = 'accounts_v1'

urlpatterns = [
    path('v1/', include('accounts.api.v1.urls')),
]
