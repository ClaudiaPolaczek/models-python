from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'notifications', NotificationsViewSet, basename='notifications')
#router.register(r'notifications/{pk}/$', NotificationsViewSet, basename='notifications-detail')
