from django.urls import path
from clickercore.views import index

urls = [
    path('clicer', index),
]
