from django.shortcuts import render
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets,response
from .serializer import PassSerializer,SecNotesSerializer,CardsSerializer, FilesSerializer, UsersSerializer
from .models import Pass,SecNotes,Cards, Files, Users
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .enc.algo import genKeyPass, encryptPass, decryptPass
from django.http import HttpResponse
from django.conf import settings
import hashlib
import os
# Create your views here.

Response = response.Response

class PassViewSet(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer
    def list_user_pass(self, request, pk=None):
        queryset = Pass.objects.filter(owner_id=pk)
        serializer = PassSerializer(queryset, many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        owner_id = request.data['owner_id']
        owner=Users.objects.get(pk=owner_id)
        data=request.data.copy()
        for key in data:
            if key!='owner_id':
                data[key] = encryptPass(owner.username, data[key])
        pass_serializer = PassSerializer(data=data)
        if pass_serializer.is_valid():
            pass_serializer.save()
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)
        
    def update(self, request, pk=None):
        owner_id = request.data['owner_id']
        owner=Users.objects.get(pk=owner_id)
        data=request.data.copy()
        for key in data:
            if key!='owner_id':
                data[key] = encryptPass(owner.username, data[key])
        pass_serializer = PassSerializer(data=request.data)
        if pass_serializer.is_valid():
            pass_serializer.save()
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)
        
    def retrieve(self, request, pk=None):
        try:
            pass_obj = Pass.objects.get(pk=pk)
        except:
            return Response({'error':'pass not found'}, status=404)
        owner=Users.objects.get(pk=pass_obj.owner_id.id)
        print(pass_obj.__dict__)
        pass_dict = pass_obj.__dict__
        pass_dict_copy = pass_dict.copy()
        for key in pass_dict_copy:
            if pass_dict_copy[key] is not None and type(pass_dict_copy[key]) is str:
                print(key)
                print(type(pass_dict_copy[key]))
                pass_dict_copy[key] = decryptPass(owner.username, pass_dict_copy[key])
        pass_dict_copy['owner_id'] = pass_dict_copy['owner_id_id']
        print(pass_dict_copy)
        pass_serializer = PassSerializer(data=pass_dict_copy)
        if pass_serializer.is_valid():
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)
        
    

class SecNotesViewSet(viewsets.ModelViewSet):
    queryset = SecNotes.objects.all()
    serializer_class = SecNotesSerializer
    def list_user_notes(self, request, pk=None):
        queryset = SecNotes.objects.filter(owner_id=pk)
        serializer = SecNotesSerializer(queryset, many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        owner_id = request.data['owner_id']
        owner=Users.objects.get(pk=owner_id)
        data=request.data.copy()
        for key in data:
            if key!='owner_id':
                data[key] = encryptPass(owner.username, data[key])
        pass_serializer = SecNotesSerializer(data=data)
        if pass_serializer.is_valid():
            pass_serializer.save()
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)
        
    def update(self, request, pk=None):
        owner_id = request.data['owner_id']
        owner=Users.objects.get(pk=owner_id)
        data=request.data.copy()
        for key in data:
            if key!='owner_id':
                data[key] = encryptPass(owner.username, data[key])
        pass_serializer = SecNotesSerializer(data=request.data)
        if pass_serializer.is_valid():
            pass_serializer.save()
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)
        
    def retrieve(self, request, pk=None):
        try:
            pass_obj = Cards.objects.get(pk=pk)
        except:
            return Response({'error':'note not found'}, status=404)
        owner=Users.objects.get(pk=pass_obj.owner_id.id)
        print(pass_obj.__dict__)
        pass_dict = pass_obj.__dict__
        pass_dict_copy = pass_dict.copy()
        for key in pass_dict_copy:
            if pass_dict_copy[key] is not None and type(pass_dict_copy[key]) is str:
                print(key)
                print(type(pass_dict_copy[key]))
                pass_dict_copy[key] = decryptPass(owner.username, pass_dict_copy[key])
        pass_dict_copy['owner_id'] = pass_dict_copy['owner_id_id']
        print(pass_dict_copy)
        pass_serializer = SecNotesSerializer(data=pass_dict_copy)
        if pass_serializer.is_valid():
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)

class CardsViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardsSerializer
    def list_user_cards(self, request, pk=None):
        queryset = Cards.objects.filter(owner_id=pk)
        serializer = CardsSerializer(queryset, many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        owner_id = request.data['owner_id']
        owner=Users.objects.get(pk=owner_id)
        data=request.data.copy()
        for key in data:
            if key!='owner_id':
                data[key] = encryptPass(owner.username, data[key])
        pass_serializer = CardsSerializer(data=data)
        if pass_serializer.is_valid():
            pass_serializer.save()
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)
        
    def update(self, request, pk=None):
        owner_id = request.data['owner_id']
        owner=Users.objects.get(pk=owner_id)
        data=request.data.copy()
        for key in data:
            if key!='owner_id':
                data[key] = encryptPass(owner.username, data[key])
        pass_serializer = CardsSerializer(data=request.data)
        if pass_serializer.is_valid():
            pass_serializer.save()
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)
        
    def retrieve(self, request, pk=None):
        try:
            pass_obj = Cards.objects.get(pk=pk)
        except:
            return Response({'error':'card not found'}, status=404)
        owner=Users.objects.get(pk=pass_obj.owner_id.id)
        print(pass_obj.__dict__)
        pass_dict = pass_obj.__dict__
        pass_dict_copy = pass_dict.copy()
        for key in pass_dict_copy:
            if pass_dict_copy[key] is not None and type(pass_dict_copy[key]) is str:
                print(key)
                print(type(pass_dict_copy[key]))
                pass_dict_copy[key] = decryptPass(owner.username, pass_dict_copy[key])
        pass_dict_copy['owner_id'] = pass_dict_copy['owner_id_id']
        print(pass_dict_copy)
        pass_serializer = CardsSerializer(data=pass_dict_copy)
        if pass_serializer.is_valid():
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)

class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    def list_user_files(self, request, pk=None):
        queryset = Files.objects.filter(owner_id=pk)
        serializer = FilesSerializer(queryset, many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        request.data['encrypted_file_name'] = hashlib.sha256(request.data['file'].name.encode('utf-8')).hexdigest()
        file_serializer = FilesSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=201)
        else:
            return Response(file_serializer.errors, status=400)
    def download(self, request, pk=None):
        file = Files.objects.get(pk=pk)
        file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        else:
            return Response({'error': 'file not found'}, status=404)

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