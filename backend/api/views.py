from django.shortcuts import render
from rest_framework import viewsets
from .serializer import PassDBSerializer,SecNotesDBSerializer,CardsDBSerializer, FileDBSerializer
from .models import PassDB,SecNotesDB,CardsDB, FileDB
# Create your views here.

class PassDBViewSet(viewsets.ModelViewSet):
    queryset = PassDB.objects.all()
    serializer_class = PassDBSerializer

class SecNotesDBViewSet(viewsets.ModelViewSet):
    queryset = SecNotesDB.objects.all()
    serializer_class = SecNotesDBSerializer

class CardsDBViewSet(viewsets.ModelViewSet):
    queryset = CardsDB.objects.all()
    serializer_class = CardsDBSerializer

class FileDBViewSet(viewsets.ModelViewSet):
    queryset = FileDB.objects.all()
    serializer_class = FileDBSerializer

