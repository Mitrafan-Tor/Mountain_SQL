from django.urls import path
from .views import SubmitDataAPI

urlpatterns = [
    path('submitData/', SubmitDataAPI.as_view(), name='submit-data'),
    path('submitData/<int:pk>/', SubmitDataAPI.as_view(), name='submit-data-detail'),
]