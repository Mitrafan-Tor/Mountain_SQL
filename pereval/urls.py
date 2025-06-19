from django.urls import path
from .views import SubmitDataListAPI, SubmitDataDetailAPI

urlpatterns = [
    path('submitData/', SubmitDataListAPI.as_view(), name='submit-data'),
    path('submitData/<int:pk>/', SubmitDataDetailAPI.as_view(), name='submit-data-detail'),
]