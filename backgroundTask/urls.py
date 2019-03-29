from django.conf.urls import url
from .views import main_view

urlpatterns = [
    url('', main_view, name='main_view'),
]
