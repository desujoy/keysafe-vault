from django.shortcuts import render
from rest_framework import viewsets
from .serializer import PassSerializer,SecNotesSerializer,CardsSerializer, FilesSerializer
from .models import Pass,SecNotes,Cards, Files
# Create your views here.

class PassViewSet(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer

class SecNotesViewSet(viewsets.ModelViewSet):
    queryset = SecNotes.objects.all()
    serializer_class = SecNotesSerializer

class CardsViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardsSerializer

class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

