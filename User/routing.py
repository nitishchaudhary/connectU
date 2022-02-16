from django.urls import path
from . import consumers
from . import views


websocket_urlpatterns=[
    path('user/<str:username>',consumers.UserConsumer.as_asgi(),),
]