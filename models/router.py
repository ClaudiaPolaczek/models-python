from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'notifications', NotificationsViewSet, basename='notifications')
router.register(r'images', ImagesViewSet, basename='images')
router.register(r'portfolios', PortfolioViewSet, basename='portfolios')
router.register(r'comments', CommentsViewSet, basename='comments')
router.register(r'photoshoots', PhotoshootsViewSet, basename='photoshoots')
router.register(r'photographers', PhotographersViewSet, basename='photographers')
router.register(r'models', ModelsViewSet, basename='models')
router.register(r'users', UsersViewSet, basename='users')
router.register(r'surveys', SurveysViewSet, basename='surveys')
