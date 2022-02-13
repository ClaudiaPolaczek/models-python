from django.urls import path, include
from .router import router
from . import views

urlpatterns = [
    path('', include(router.urls)),
]