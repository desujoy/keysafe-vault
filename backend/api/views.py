from django.shortcuts import render
from rest_framework import viewsets,response
from .serializer import PassSerializer,SecNotesSerializer,CardsSerializer, FilesSerializer, UsersSerializer
from .models import Pass,SecNotes,Cards, Files, Users
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .enc.algo import genKeyPass
# Create your views here.

Response = response.Response

class PassViewSet(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer
    def list_user_pass(self, request, pk=None):
        queryset = Pass.objects.filter(owner_id=pk)
        serializer = PassSerializer(queryset, many=True)
        return Response(serializer.data)
    

class SecNotesViewSet(viewsets.ModelViewSet):
    queryset = SecNotes.objects.all()
    serializer_class = SecNotesSerializer
    def list_user_notes(self, request, pk=None):
        queryset = SecNotes.objects.filter(owner_id=pk)
        serializer = SecNotesSerializer(queryset, many=True)
        return Response(serializer.data)

class CardsViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardsSerializer
    def list_user_cards(self, request, pk=None):
        queryset = Cards.objects.filter(owner_id=pk)
        serializer = CardsSerializer(queryset, many=True)
        return Response(serializer.data)

class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    def list_user_files(self, request, pk=None):
        queryset = Files.objects.filter(owner_id=pk)
        serializer = FilesSerializer(queryset, many=True)
        return Response(serializer.data)

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

@csrf_exempt
def genkeypass(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username is None or password is None:
            return JsonResponse({'username':'This field is required', 'password':'This field is required'})
        enc_blob=genKeyPass(username, password)
        return JsonResponse({'keypass':enc_blob.decode('utf-8')})
    else:
        return JsonResponse({'error': 'invalid request'})