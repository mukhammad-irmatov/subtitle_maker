from django.urls import path
from .views import homePageView, videopage

urlpatterns = [
    path('', homePageView, name='homepage'),
    path('result/', videopage, name='resultpage')
]