from django.contrib import admin
from django.urls import path, include
#from allauth.account.views import confirm_email
#from rest_framework_swagger.views import get_swagger_view

#schema_view = get_swagger_view(title='Models API')

urlpatterns = [
    #path('', schema_view),
    path('admin/', admin.site.urls),
    path('', include('models.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj_rest_auth/registration/', include('dj_rest_auth.registration.urls')),
    path('account/', include('allauth.urls'))
]