from django.shortcuts import render
from .models import Notification, Image, Portfolio, Comment, User
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse


class NotificationsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        notification = Notification.objects.get(pk=pk)
        serializer = NotificationReaderSerializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def retrieve_by_user(self, request):
        user = self.request.GET.get('username', '')
        try:
            notification = Notification.objects.filter(user_username=user)
        except Notification.DoesNotExist:
            return Response('Notifications not found', status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationReaderSerializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='n')
    def retrieve_non_read_by_user(self, request):
        user = self.request.GET.get('username', '')
        try:
            notification = Notification.objects.filter(user_username=user, read_value=0)
        except Notification.DoesNotExist:
            return Response('Notifications not found', status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationReaderSerializer(notification)
        return Response(serializer.data)

    #TODO: sciezka na read/id
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


class ImagesViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        image = Image.objects.get(pk=pk)
        serializer = ImageReaderSerializer(image)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def retrieve_by_portfolio(self, request):
        portfolio = self.request.GET.get('portfolio', '')
        try:
            image = Image.objects.filter(portfolio_id=portfolio)
        except Image.DoesNotExist:
            return Response('Images not found', status=status.HTTP_404_NOT_FOUND)
        serializer = ImageReaderSerializer(image, many=True)
        return Response(serializer.data)

    def list(self, request):
        queryset = Image.objects.all()
        serializer = ImageReaderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        write_serializer = ImageWriterSerializer(data=request.data)
        if write_serializer.is_valid():
            image = write_serializer.save()
            read_serializer = ImageReaderSerializer(image)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        image = Image.objects.get(pk=pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['delete'], url_path='url')
    def delete_by_url(self, request):
        url = self.request.GET.get('url', '')
        try:
            image = Image.objects.filter(url=url)
        except Image.DoesNotExist:
            return Response('Images not found', status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PortfolioViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        portfolio = Portfolio.objects.get(pk=pk)
        serializer = PortfolioReaderSerializer(portfolio)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def retrieve_by_user(self, request):
        username = self.request.GET.get('user', '')
        try:
            portfolio = Portfolio.objects.filter(user__username=username)
        except Portfolio.DoesNotExist:
            return Response('Images not found', status=status.HTTP_404_NOT_FOUND)
        serializer = PortfolioReaderSerializer(portfolio, many=True)
        return Response(serializer.data)

    def list(self, request):
        queryset = Portfolio.objects.all()
        serializer = PortfolioReaderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        write_serializer = PortfolioWriterSerializer(data=request.data)
        if write_serializer.is_valid():
            portfolio = write_serializer.save()
            read_serializer = PortfolioReaderSerializer(portfolio)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        portfolio = Portfolio.objects.get(pk=pk)
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        try:
            portfolio = Portfolio.objects.get(pk=pk)
        except Portfolio.DoesNotExist:
            return Response('Portfolio not found', status=status.HTTP_404_NOT_FOUND)
        data = self.request.data
        portfolio.description = data["description"]
        portfolio.main_photo_url = data["main_photo_url"]
        portfolio.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['update'], url_path='photo')
    def add_main_photo(self, request):
        id = self.request.GET.get('id', '')
        try:
            portfolio = Portfolio.objects.get(pk=id)
        except Portfolio.DoesNotExist:
            return Response('Portfolio not found', status=status.HTTP_404_NOT_FOUND)
        data = self.request.data
        portfolio.main_photo_url = data["main_photo_url"]
        portfolio.save()
        return Response(status=status.HTTP_200_OK)


class CommentsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        serializer = CommentReaderSerializer(comment)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def retrieve_by_rating_user(self, request):
        user = self.request.GET.get('username', '')
        try:
            comment = Comment.objects.filter(rating_user__username=user)
        except Comment.DoesNotExist:
            return Response('Comments not found', status=status.HTTP_404_NOT_FOUND)
        serializer = CommentReaderSerializer(comment, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def retrieve_by_rated_user(self, request):
        user = self.request.GET.get('username', '')
        try:
            comment = Comment.objects.filter(rated_user__username=user)
        except Comment.DoesNotExist:
            return Response('Comments not found', status=status.HTTP_404_NOT_FOUND)
        serializer = CommentReaderSerializer(comment, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='avg')
    def get_average_for_users(self, request):
        avg = 0.0
        try:
            users = User.objects.all()
        except User.DoesNotExist:
            return Response('Users do not exists', status=status.HTTP_404_NOT_FOUND)
        for user in users:
            if user.role != User.ADMIN:
                comments = Comment.objects.filter(rated_user__username=user)
                if len(comments) != 0:
                    sum = 0.0
                    for comment in comments:
                        sum += comment.rating
                    avg = sum / len(comments)
                    user.avg_rate = avg
                    user.save()
        serializer = UserReaderSerializer(users, many=True)
        return Response(serializer.data)

    def list(self, request):
        queryset = Comment.objects.all()
        serializer = CommentReaderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        write_serializer = CommentWriterSerializer(data=request.data)
        if write_serializer.is_valid():
            comment = write_serializer.save()
            read_serializer = CommentReaderSerializer(comment)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoshootsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        photoshoot = Photoshoot.objects.get(pk=pk)
        serializer = PortfolioReaderSerializer(photoshoot)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='inviting')
    def retrieve_by_inviting_user(self, request):
        user = self.request.GET.get('username', '')
        try:
            photoshoot = Photoshoot.objects.filter(inviting_user__username=user)
        except Photoshoot.DoesNotExist:
            return Response('Photoshoots not found', status=status.HTTP_404_NOT_FOUND)
        serializer = PhotoshootReaderSerializer(photoshoot, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='invited')
    def retrieve_by_invited_user(self, request):
        user = self.request.GET.get('username', '')
        try:
            photoshoot = Photoshoot.objects.filter(invited_user__username=user)
        except Comment.DoesNotExist:
            return Response('Photoshoots not found', status=status.HTTP_404_NOT_FOUND)
        serializer = PhotoshootReaderSerializer(photoshoot, many=True)
        return Response(serializer.data)

    def list(self, request):
        queryset = Photoshoot.objects.all()
        serializer = PhotoshootReaderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        write_serializer = PhotoshootWriterSerializer(data=request.data)
        if write_serializer.is_valid():
            photoshoot = write_serializer.save()
            read_serializer = PhotoshootReaderSerializer(photoshoot)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        photoshoot = Photoshoot.objects.get(pk=pk)
        photoshoot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['patch'], url_path='cancel')
    def cancel_photoshoot(self, request, pk=None):
        photoshoot = Photoshoot.objects.get(pk=pk)
        if photoshoot.photoshoot_status != Photoshoot.CANCELED:
            if photoshoot.photoshoot_status == Photoshoot.CREATED or photoshoot.photoshoot_status == Photoshoot.ACCEPTED:
                photoshoot.photoshoot_status = Photoshoot.CANCELED
                photoshoot.save()
            else:
                return Response('Photoshoot status should equal' + str(Photoshoot.CREATED) + " or " + str(Photoshoot.ACCEPTED),
                                status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['patch'], url_path='accept')
    def accept_photoshoot(self, request, pk=None):
        photoshoot = Photoshoot.objects.get(pk=pk)
        if photoshoot.photoshoot_status != Photoshoot.ACCEPTED:
            if photoshoot.photoshoot_status == Photoshoot.CREATED:
                photoshoot.photoshoot_status = Photoshoot.ACCEPTED
                photoshoot.save()
            else:
                return Response('Photoshoot status should equal' + str(Photoshoot.CREATED),
                                status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], url_path='end')
    def end_photoshoot(self, request, pk=None):
        photoshoot = Photoshoot.objects.get(pk=pk)
        if photoshoot.photoshoot_status != Photoshoot.ENDED:
            if photoshoot.photoshoot_status == Photoshoot.ACCEPTED:
                photoshoot.photoshoot_status = Photoshoot.ENDED
                photoshoot.save()
            else:
                return Response('Photoshoot status should equal' + str(Photoshoot.ACCEPTED),
                                status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='all')
    def retrieve_by_user(self, request):
        user = self.request.GET.get('username', '')
        photoshoots = list(Photoshoot.objects.filter(inviting_user__username=user))
        photoshoots.append(list(Photoshoot.objects.filter(invited_user__username=user)))
        serializer = PhotoshootReaderSerializer(photoshoots, many=True)
        return Response(serializer.data)


class PhotographersViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        photographer = Photographer.objects.get(pk=pk)
        serializer = PhotographerReaderSerializer(photographer)
        return Response(serializer.data)

    def list(self, request):
        queryset = Photographer.objects.all()
        serializer = PhotographerReaderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        write_serializer = PhotographerWriterSerializer(data=request.data)
        if write_serializer.is_valid():
            photographer = write_serializer.save()
            read_serializer = PhotographerReaderSerializer(photographer)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        photographer = Photographer.objects.get(pk=pk)
        write_serializer = PhotographerWriterSerializer(photographer, data=request.data)
        if write_serializer.is_valid():
            photographer = write_serializer.save()
            read_serializer = PhotographerReaderSerializer(photographer)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        photographer = Photographer.objects.get(pk=pk)
        photographer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SurveysViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        survey = Survey.objects.get(pk=pk)
        serializer = SurveyReaderSerializer(survey)
        return Response(serializer.data)

    def list(self, request):
        queryset = Survey.objects.all()
        serializer = SurveyReaderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        write_serializer = SurveyWriterSerializer(data=request.data)
        if write_serializer.is_valid():
            survey = write_serializer.save()
            read_serializer = SurveyReaderSerializer(survey)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        serializer = UserReaderSerializer(user)
        return Response(serializer.data)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserReaderSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='username')
    def retrieve_by_username(self, request):
        username = self.request.GET.get('username', '')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        serializer = UserReaderSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'], url_path='password')
    def change_password(self, request, pk=None):
        user = User.objects.get(username=pk)
        #TODO change password
        user.main_photo_url = request.data["password"]
        user.save()
        return Response(user, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='photo')
    def add_main_photo(self, request, pk=None):
        user = User.objects.get(username=pk)
        user.main_photo_url = request.data["main_photo_url"]
        user.save()
        return Response(user, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        user = User.objects.get(pk=pk)
        user.delete()
        #TODO usuniecie wszystkiego co zwiazane
        return Response(status=status.HTTP_204_NO_CONTENT)