from django.db import transaction, IntegrityError
import operator
from django.db.models import Q
from .permissions import UserAccessPermission, IsAdmin
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import *


class NotificationsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            notification = Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            return Response('Notification not found', status=status.HTTP_404_NOT_FOUND)
        serializer = NotificationReaderSerializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='user')
    def retrieve_by_user(self, request):
        email = self.request.GET.get('email', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        notification = Notification.objects.filter(user_id=user.id)
        serializer = NotificationReaderSerializer(notification, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='n')
    def retrieve_non_read_by_user(self, request):
        email = self.request.GET.get('email', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        notification = Notification.objects.filter(user_id=user.id, read_value=0)
        serializer = NotificationReaderSerializer(notification, many=True)
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
        try:
            notification = Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            return Response('Notification not found', status=status.HTTP_404_NOT_FOUND)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ('retrieve_by_user', 'retrieve_non_read_by_user', 'read', 'list', 'create', 'delete'):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdmin]
        return [permission() for permission in permission_classes]


class ImagesViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            image = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response('Image not found', status=status.HTTP_404_NOT_FOUND)
        serializer = ImageReaderSerializer(image)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='portfolio')
    def retrieve_by_portfolio(self, request):
        portfolio_id = self.request.GET.get('portfolio', '')
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id )
        except Portfolio.DoesNotExist:
            return Response('Portfolio not found', status=status.HTTP_404_NOT_FOUND)
        images = Image.objects.filter(portfolio_id=portfolio.id)
        serializer = ImageReaderSerializer(images, many=True)
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

    @action(detail=False, methods=['delete'], url_path='url')
    def delete_by_url(self, request):
        url = self.request.GET.get('url', '')
        try:
            images = Image.objects.filter(file_url=url)
        except Image.DoesNotExist:
            return Response('Images not found', status=status.HTTP_404_NOT_FOUND)
        for image in images:
            image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ('retrieve_by_portfolio', 'list', 'delete_by_url', 'create', 'delete'):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdmin]
        return [permission() for permission in permission_classes]


class PortfolioViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            portfolio = Portfolio.objects.get(pk=pk)
        except Portfolio.DoesNotExist:
            return Response('Portfolio not found', status=status.HTTP_404_NOT_FOUND)
        serializer = PortfolioReaderSerializer(portfolio)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='user')
    def retrieve_by_user(self, request):
        email = self.request.GET.get('email', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        portfolio = Portfolio.objects.filter(user_id=user.id)
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

    def partial_update(self, request, pk=None):
        try:
            portfolio = Portfolio.objects.get(pk=pk)
        except Portfolio.DoesNotExist:
            return Response('Portfolio not found', status=status.HTTP_404_NOT_FOUND)
        data = self.request.data
        portfolio.description = data["description"]
        portfolio.name = data["name"]
        portfolio.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='photo')
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

    def delete(self, request, pk=None):
        try:
            portfolio = Portfolio.objects.get(pk=pk)
        except Portfolio.DoesNotExist:
            return Response('Portfolio not found', status=status.HTTP_404_NOT_FOUND)
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ('retrieve_by_user', 'list', 'partial_update', 'create', 'delete', 'add_main_photo'):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdmin]
        return [permission() for permission in permission_classes]


class CommentsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response('Comment not found', status=status.HTTP_404_NOT_FOUND)
        serializer = CommentReaderSerializer(comment)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='rating')
    def retrieve_by_rating_user(self, request):
        email = self.request.GET.get('email', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(rating_user__id=user.id)
        serializer = CommentReaderSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='rated')
    def retrieve_by_rated_user(self, request):
        email = self.request.GET.get('email', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(rated_user__id=user)
        serializer = CommentReaderSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='users')
    def retrieve_by_rating_and_rated_user(self, request):
        user_rating_email = self.request.GET.get('email_rating', '')
        user_rated_email = self.request.GET.get('email_rated', '')
        try:
            user_rating = User.objects.filter(email=user_rating_email).first()
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        try:
            user_rated = User.objects.filter(email=user_rated_email).first()
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(rating_user__id=user_rating.id, rated_user__id=user_rated.id)
        return Response('Comments not found', status=status.HTTP_404_NOT_FOUND)
        serializer = CommentReaderSerializer(comments, many=True)
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
                comments = Comment.objects.filter(rated_user__email=user)
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
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response('Comment not found', status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ('retrieve_by_rating_user', 'retrieve_by_rated_user',
                             'retrieve_by_rating_and_rated_user', 'get_average_for_users', 'list', 'create'):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdmin]
        return [permission() for permission in permission_classes]


class PhotoshootsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            photoshoot = Photoshoot.objects.get(pk=pk)
        except Photoshoot.DoesNotExist:
            return Response('Photoshoot not found', status=status.HTTP_404_NOT_FOUND)
        serializer = PhotoshootReaderSerializer(photoshoot)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='inviting')
    def retrieve_by_inviting_user(self, request):
        email = self.request.GET.get('email', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        photoshoot = Photoshoot.objects.filter(inviting_user__id=user.id)
        serializer = PhotoshootReaderSerializer(photoshoot, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='invited')
    def retrieve_by_invited_user(self, request):
        email = self.request.GET.get('email', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        photoshoot = Photoshoot.objects.filter(invited_user__id=user.id)
        serializer = PhotoshootReaderSerializer(photoshoot, many=True)
        return Response(serializer.data)

    #TODO retrieve by user

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

    @action(detail=False, methods=['patch'], url_path='cancel')
    def cancel_photoshoot(self, request, pk=None):
        id = self.request.GET.get('id', '')
        try:
            photoshoot = Photoshoot.objects.get(id=id)
        except Photoshoot.DoesNotExist:
            return Response('Photoshoot not found', status=status.HTTP_404_NOT_FOUND)
        if photoshoot.photoshoot_status != Photoshoot.CANCELED:
            if photoshoot.photoshoot_status == Photoshoot.CREATED or photoshoot.photoshoot_status == Photoshoot.ACCEPTED:
                photoshoot.photoshoot_status = Photoshoot.CANCELED
                photoshoot.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response('Photoshoot status should equal ' + str(Photoshoot.CREATED) + " or " + str(Photoshoot.ACCEPTED),
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='accept')
    def accept_photoshoot(self, request, pk=None):
        id = self.request.GET.get('id', '')
        try:
            photoshoot = Photoshoot.objects.get(id=id)
        except Photoshoot.DoesNotExist:
            return Response('Photoshoot not found', status=status.HTTP_404_NOT_FOUND)
        if photoshoot.photoshoot_status != Photoshoot.ACCEPTED:
            if photoshoot.photoshoot_status == Photoshoot.CREATED:
                photoshoot.photoshoot_status = Photoshoot.ACCEPTED
                photoshoot.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response('Photoshoot status should equal ' + str(Photoshoot.CREATED),
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='end')
    def end_photoshoot(self, request, pk=None):
        id = self.request.GET.get('id', '')
        try:
            photoshoot = Photoshoot.objects.get(id=id)
        except Photoshoot.DoesNotExist:
            return Response('Photoshoot not found', status=status.HTTP_404_NOT_FOUND)
        if photoshoot.photoshoot_status != Photoshoot.ENDED:
            if photoshoot.photoshoot_status == Photoshoot.ACCEPTED:
                photoshoot.photoshoot_status = Photoshoot.ENDED
                photoshoot.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response('Photoshoot status should equal ' + str(Photoshoot.ACCEPTED),
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ('retrieve_by_inviting_user', 'retrieve_by_invited_user',
                             'cancel_photoshoot', 'get_average_for_users', 'end_photoshoot',
                             'list', 'create'):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdmin]
        return [permission() for permission in permission_classes]


class ModelsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            model = Model.objects.get(pk=pk)
        except Model.DoesNotExist:
            return Response('Model not found', status=status.HTTP_404_NOT_FOUND)
        serializer = ModelSerializer(model)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='email')
    def retrieve_by_email(self, request):
        email = self.request.GET.get('email', '')
        try:
            user = User.objects.filter(email=email).first()
            model = Model.objects.filter(user_id=user.id).first()
        except Model.DoesNotExist:
            return Response('Model not found', status=status.HTTP_404_NOT_FOUND)
        serializer = ModelSerializer(model)
        return Response(serializer.data)

    def list(self, request):
        queryset = Model.objects.all()
        serializer = ModelSerializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = self.request.data
        register_serializer = RegisterSerializer(data=data)
        try:
            with transaction.atomic():
                if register_serializer.is_valid():
                    new_user = register_serializer.save(request)
                    new_user.role = User.MODEL
                    new_user.save()
                else:
                    return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                survey_serializer = SurveyWriterSerializer(data=data)
                if survey_serializer.is_valid():
                    new_survey = survey_serializer.save()
                else:
                    return Response(survey_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                new_model = Model.objects.create(user=new_user, survey=new_survey)
                new_model.save()
                model = ModelSerializer(new_model)
                return Response(model.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(IntegrityError, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='instagram')
    def instagram(self, request):
        pk = self.request.GET.get('pk', '')
        try:
            model = Model.objects.get(pk=pk)
        except Model.DoesNotExist:
            return Response('Model not found', status=status.HTTP_404_NOT_FOUND)
        survey = model.survey
        data = self.request.data
        survey.instagram_name = data["instagram_name"]
        survey.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='add')
    def additional_information(self, request):
        pk = self.request.GET.get('pk', '')
        try:
            model = Model.objects.get(pk=pk)
        except Model.DoesNotExist:
            return Response('Model not found', status=status.HTTP_404_NOT_FOUND)
        data = self.request.data
        model.eyes_color = data["eyes_color"]
        model.hair_color = data["hair_color"]
        model.save()
        return Response(status=status.HTTP_200_OK)

    #def update(self, request, pk=None):
    #    model = Model.objects.get(pk=pk)
    #    write_serializer = ModelSerializer(model, data=request.data)
    #    if write_serializer.is_valid():
    #        model = write_serializer.save()
    #        read_serializer = ModelSerializer(model)
    #        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
    #    return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, pk=None):
        try:
            with transaction.atomic():
                try:
                    model = Model.objects.get(pk=pk)
                except Model.DoesNotExist:
                    return Response('Model not found', status=status.HTTP_404_NOT_FOUND)
                survey = model.survey
                user = model.user
                user.delete()
                survey.delete()
                model.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            return Response(IntegrityError, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ('retrieve', 'retrieve_by_email', 'list',
                             'create', 'instagram', 'additional_information'):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]


class PhotographersViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            photographer = Photographer.objects.get(pk=pk)
        except Photographer.DoesNotExist:
            return Response('Photographer not found', status=status.HTTP_404_NOT_FOUND)
        serializer = PhotographerSerializer(photographer)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='email')
    def retrieve_by_email(self, request):
        email = self.request.GET.get('email', '')
        try:
            user = User.objects.filter(email=email).first()
            photographer = Photographer.objects.filter(user_id=user.id).first()
        except Photographer.DoesNotExist:
            return Response('Photographer not found', status=status.HTTP_404_NOT_FOUND)
        serializer = PhotographerSerializer(photographer)
        return Response(serializer.data)

    def list(self, request):
        queryset = Photographer.objects.all()
        serializer = PhotographerSerializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = self.request.data
        register_serializer = RegisterSerializer(data=data)
        try:
            with transaction.atomic():
                if register_serializer.is_valid():
                    new_user = register_serializer.save(request)
                    new_user.role = User.PHOTOGRAPHER
                    new_user.save()
                else:
                    return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                survey_serializer = SurveyWriterSerializer(data=data)
                if survey_serializer.is_valid():
                    new_survey = survey_serializer.save()
                else:
                    return Response(survey_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                new_photographer = Photographer.objects.create(user=new_user, survey=new_survey)
                new_photographer.save()
                photographer = PhotographerSerializer(new_photographer)
                return Response(photographer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(IntegrityError, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='instagram')
    def instagram(self, request, pk=None):
        pk = self.request.GET.get('pk', '')
        try:
            photographer = Photographer.objects.get(pk=pk)
        except Photographer.DoesNotExist:
            return Response('Photographer not found', status=status.HTTP_404_NOT_FOUND)
        survey = photographer.survey
        data = self.request.data
        survey.instagram_name = data["instagram_name"]
        survey.save()
        return Response(status=status.HTTP_200_OK)

    #def update(self, request, pk=None):
    #    photographer = Photographer.objects.get(pk=pk)
    #    write_serializer = PhotographerSerializer(photographer, data=request.data)
    #    if write_serializer.is_valid():
    #        photographer = write_serializer.save()
    #        read_serializer = PhotographerSerializer(photographer)
    #        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
    #    return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, pk=None):
        try:
            with transaction.atomic():
                try:
                    photographer = Photographer.objects.get(pk=pk)
                except Photographer.DoesNotExist:
                    return Response('Photographer not found', status=status.HTTP_404_NOT_FOUND)
                survey = photographer.survey
                user = photographer.user
                user.delete()
                survey.delete()
                photographer.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            return Response(IntegrityError, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ('retrieve', 'retrieve_by_email', 'list',
                             'create', 'instagram'):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdmin]
        return [permission() for permission in permission_classes]


class SurveysViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            survey = Survey.objects.get(pk=pk)
        except Survey.DoesNotExist:
            return Response('Survey not found', status=status.HTTP_404_NOT_FOUND)
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

    def partial_update(self, request, pk=None):
        try:
            survey = Survey.objects.get(pk=pk)
        except Survey.DoesNotExist:
            return Response('Survey not found', status=status.HTTP_404_NOT_FOUND)
        data = self.request.data
        survey.first_name = data["first_name"]
        survey.last_name = data["last_name"]
        survey.birthday_year = data["birthday_year"]
        survey.gender = data["gender"]
        survey.region = data["region"]
        survey.city = data["city"]
        survey.phone_number = data["phone_number"]
        survey.regulations_agreement = data["regulations_agreement"]
        survey.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='instagram')
    def set_instagram_name(self, request, pk=None):
        pk = self.request.GET.get('pk', '')
        try:
            survey = Survey.objects.get(pk=pk)
        except Survey.DoesNotExist:
            return Response('Survey not found', status=status.HTTP_404_NOT_FOUND)
        data = self.request.data
        survey.instagram_name = data["instagram_name"]
        survey.save()
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            survey = Survey.objects.get(pk=pk)
        except Survey.DoesNotExist:
            return Response('Survey not found', status=status.HTTP_404_NOT_FOUND)
        survey.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ('partial_update', 'list',
                             'create', 'set_instagram_name'):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdmin]
        return [permission() for permission in permission_classes]


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

    @action(detail=False, methods=['get'], url_path='email')
    def retrieve_by_email(self, request):
        email = self.request.GET.get('email', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        serializer = UserReaderSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='photo')
    def add_main_photo(self, request, pk=None):
        email = self.request.GET.get('email', '')
        try:
            users = User.objects.filter(email=email).values()
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        for user in users:
            user.update(main_photo_url = request.data["fileUrl"])
            return Response(user, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        user.delete()
        #TODO usuniecie wszystkiego co zwiazane z Userem
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ('retrieve_by_username', 'retrieve_by_email', 'list', 'add_main_photo'):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdmin]
        return [permission() for permission in permission_classes]
