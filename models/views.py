from django.shortcuts import render
from .models import Notification
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .serializers import NotificationReaderSerializer, NotificationWriterSerializer
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
#
#
class NotificationsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        notification = Notification.objects.get(pk=pk)
        serializer = NotificationReaderSerializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def retrieve_by_user(self, request):
        user = self.request.GET.get('username', '')
        try:
            notification = Notification.objects.get(user_username=user)
        except Notification.DoesNotExist:
            return Response('Notifications not found', status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationReaderSerializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='n')
    def retrieve_non_read_by_user(self, request):
        user = self.request.GET.get('username', '')
        try:
            notification = Notification.objects.get(user_username=user, read_value=0)
        except Notification.DoesNotExist:
            return Response('Notifications not found', status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationReaderSerializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'], url_path='read')
    def read(self, request):
        id = self.request.GET.get('id', '')
        try:
            notification = Notification.objects.get(id=id)
        except Notification.DoesNotExist:
            return Response('Notifications not found', status=status.HTTP_404_NOT_FOUND)
        notification.read_value = 1
        notification.save()
        return Response(status=status.HTTP_200_OK)

    def list(self, request):
        queryset = Notification.objects.all()
        serializer = NotificationReaderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        write_serializer = NotificationWriterSerializer(data=request.data)
        if write_serializer.is_valid():
            notification = write_serializer.save()
            read_serializer = NotificationReaderSerializer(notification)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        notification = Notification.objects.get(pk=pk)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
