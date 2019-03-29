from django.shortcuts import render
from background_task import background
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.core.cache import cache


# Create your views here.

@background(schedule=1)
def addI():
    i = cache.get('i')
    if not i:
        i = 0
    i = i + 1
    cache.set('i', i, 60 * 15)
    print('hello')
    print(i)


addI(repeat=2, repeat_until=None)


def main_view(request):
    i = cache.get('i')
    if not i:
        i = 0
    return HttpResponse(f'pito {i}')
