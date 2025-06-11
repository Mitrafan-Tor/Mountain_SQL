from django.urls import path
from .views import SubmitDataAPI

urlpatterns = [
    path('submitData/', SubmitDataAPI.as_view(), name='submit-data'),
]