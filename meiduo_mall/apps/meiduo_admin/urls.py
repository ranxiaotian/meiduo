# from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path
from apps.meiduo_admin.user import meiduo_token
urlpatterns = [
    # path('authorizations/',obtain_jwt_token),
    path('authorizations/',meiduo_token),
]