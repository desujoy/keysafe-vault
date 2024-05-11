from django.shortcuts import render
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, response
from django.conf import settings
from .serializer import (
    PassSerializer,
    SecNotesSerializer,
    CardsSerializer,
    FilesSerializer,
    UsersSerializer,
)
from .models import Pass, SecNotes, Cards, Files, Users
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .enc.algo import (
    genKeyPass,
    encryptPass,
    decryptPass,
    encryptFile,
    decryptFile,
    decryptKeyPass,
    genToken,
    verifyKeyPass,
    encryptFile2,
    decryptFile2,
    reencryptFile2,
)
from django.http import HttpResponse
from django.conf import settings
import hashlib, base64
import os
import random
from io import BytesIO

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
        owner_id = request.data["owner_id"]
        owner = Users.objects.get(pk=owner_id)
        data = request.data.copy()
        # data["id"] = random.randint(1, 1000000000)
        data["password"] = encryptPass(owner.token, data["password"]).decode("utf-8")
        pass_serializer = PassSerializer(data=data)
        if pass_serializer.is_valid():
            pass_serializer.save()
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)

    def update(self, request, pk=None):
        owner_id = request.data["owner_id"]
        owner = Users.objects.get(pk=owner_id)
        data = request.data.copy()
        data["password"] = encryptPass(owner.token, data["password"]).decode("utf-8")
        old_data = Pass.objects.get(id=pk)
        old_data.delete()
        pass_serializer = PassSerializer(data=data)
        if pass_serializer.is_valid():
            pass_serializer.save()
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        try:
            pass_obj = Pass.objects.get(id=pk)
        except:
            return Response({"error": "pass not found"}, status=404)
        owner = Users.objects.get(pk=pass_obj.owner_id.id)
        print(pass_obj.__dict__)
        pass_dict = pass_obj.__dict__
        pass_dict_copy = pass_dict.copy()
        pass_dict_copy["password"] = decryptPass(
            owner.token, pass_dict_copy["password"]
        )
        pass_dict_copy["owner_id"] = pass_dict_copy["owner_id_id"]
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
        owner_id = request.data["owner_id"]
        owner = Users.objects.get(pk=owner_id)
        data = request.data.copy()
        # data["id"] = random.randint(1, 1000000000)
        data["content"] = encryptPass(owner.token, data["content"]).decode("utf-8")
        pass_serializer = SecNotesSerializer(data=data)
        if pass_serializer.is_valid():
            pass_serializer.save()
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)

    def update(self, request, pk=None):
        owner_id = request.data["owner_id"]
        owner = Users.objects.get(pk=owner_id)
        data = request.data.copy()
        data["content"] = encryptPass(owner.token, data["content"]).decode("utf-8")
        old_data = SecNotes.objects.get(id=pk)
        old_data.delete()
        pass_serializer = SecNotesSerializer(data=data)
        if pass_serializer.is_valid():
            pass_serializer.save()
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        try:
            pass_obj = SecNotes.objects.get(id=pk)
        except:
            return Response({"error": "note not found"}, status=404)
        owner = Users.objects.get(pk=pass_obj.owner_id.id)
        print(pass_obj.__dict__)
        pass_dict = pass_obj.__dict__
        pass_dict_copy = pass_dict.copy()
        print(pass_dict_copy)
        pass_dict_copy["content"] = decryptPass(owner.token, pass_dict_copy["content"])
        pass_dict_copy["owner_id"] = pass_dict_copy["owner_id_id"]
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
        owner_id = request.data["owner_id"]
        owner = Users.objects.get(pk=owner_id)
        data = request.data.copy()
        # data["id"] = random.randint(1, 1000000000)
        data["card_number"] = encryptPass(owner.token, data["card_number"]).decode(
            "utf-8"
        )
        data["card_exp"] = encryptPass(owner.token, data["card_exp"]).decode("utf-8")
        data["card_cvv"] = encryptPass(owner.token, data["card_cvv"]).decode("utf-8")
        pass_serializer = CardsSerializer(data=data)
        if pass_serializer.is_valid():
            pass_serializer.save()
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)

    def update(self, request, pk=None):
        owner_id = request.data["owner_id"]
        owner = Users.objects.get(pk=owner_id)
        data = request.data.copy()
        data["card_number"] = encryptPass(owner.token, data["card_number"]).decode(
            "utf-8"
        )
        data["card_exp"] = encryptPass(owner.token, data["card_exp"]).decode("utf-8")
        data["card_cvv"] = encryptPass(owner.token, data["card_cvv"]).decode("utf-8")
        old_data = Cards.objects.get(id=pk)
        old_data.delete()
        pass_serializer = CardsSerializer(data=data)
        if pass_serializer.is_valid():
            pass_serializer.save()
            return Response(pass_serializer.data, status=201)
        else:
            return Response(pass_serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        try:
            pass_obj = Cards.objects.get(id=pk)
        except:
            return Response({"error": "card not found"}, status=404)
        owner = Users.objects.get(pk=pass_obj.owner_id.id)
        print(pass_obj.__dict__)
        pass_dict = pass_obj.__dict__
        pass_dict_copy = pass_dict.copy()
        pass_dict_copy["card_number"] = decryptPass(
            owner.token, pass_dict_copy["card_number"]
        )
        pass_dict_copy["card_exp"] = decryptPass(
            owner.token, pass_dict_copy["card_exp"]
        )
        pass_dict_copy["card_cvv"] = decryptPass(
            owner.token, pass_dict_copy["card_cvv"]
        )
        pass_dict_copy["owner_id"] = pass_dict_copy["owner_id_id"]
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
        request.data["encrypted_file_name"] = hashlib.sha256(
            request.data["file"].name.encode("utf-8")
        ).hexdigest()
        # request.data["id"] = random.randint(1, 1000000000)
        # print(request.data)
        owner_id = request.data["owner_id"]
        owner = Users.objects.get(pk=owner_id)
        file_serializer = FilesSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            # file_path=os.path.join(settings.MEDIA_ROOT, file_serializer.data['file'])
            encryptFile2(
                owner.token,
                file_serializer.data["file"].split("/")[-1],
                file_serializer.data["encrypted_file_name"],
            )
            return Response(file_serializer.data, status=201)
        else:
            return Response(file_serializer.errors, status=400)

    def download(self, request, pk=None):
        file = Files.objects.get(id=pk)
        try:
            owner = Users.objects.get(pk=file.owner_id.id)
        except:
            return Response({"error": "file not found"}, status=404)
        file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
        encrypted_file_path = os.path.join(
            settings.BASE_DIR_ABSOLUTE, "files", "files", file.encrypted_file_name
        )
        if os.path.exists(encrypted_file_path):
            with open(encrypted_file_path, "rb") as file:
                file_data = file.read()
            # print(file_data)
            decrypted_file_data = decryptFile2(file_data, owner.token)
            # decrypted_file_data=base64.b64encode(decrypted_file_data)
            # print(decrypted_file_data)
            decrypted_file = BytesIO(decrypted_file_data)
            # print(decrypted_file.read())
            response = FileResponse(decrypted_file)
            response["Content-Disposition"] = (
                "attachment; filename=" + os.path.basename(file_path)
            )
            return response
        else:
            return Response({"error": "file not found"}, status=404)

    def destroy(self, request, *args, **kwargs):
        os.remove(
            os.path.join(
                settings.BASE_DIR_ABSOLUTE,
                "files",
                "files",
                Files.objects.get(id=kwargs["pk"]).encrypted_file_name,
            )
        )
        print(
            os.path.join(
                settings.BASE_DIR_ABSOLUTE,
                "files",
                "files",
                Files.objects.get(id=kwargs["pk"]).encrypted_file_name,
            )
        )
        return super().destroy(request, *args, **kwargs)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        print(f'username={data["username"]}, passowrd={data["password"]}')
        print(type(data["username"]))
        print(data)
        data["token"] = genToken(data["username"], data["password"])
        print(data["token"])
        print(type(data["token"]))
        data["verification_string"] = encryptPass(
            data["token"], settings.SECRET_KEY
        ).decode("utf-8")
        del data["username"]
        del data["password"]
        user_serializer = UsersSerializer(data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=201)
        else:
            return Response(user_serializer.errors, status=400)


@csrf_exempt
def genkeypass(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        if username is None or password is None:
            return JsonResponse(
                {
                    "username": "This field is required",
                    "password": "This field is required",
                }
            )
        print(f"views genkeypass: username={username}, password={password}")
        enc_blob = genKeyPass(username, password)
        response = JsonResponse({"enc_blob": enc_blob.decode("utf-8")})
        return response
    else:
        return JsonResponse({"error": "invalid request"})


@csrf_exempt
def verifykeypass(request):
    if request.method == "POST":
        enc_blob = request.POST.get("enc_blob", None)
        if enc_blob is None:
            return JsonResponse(
                {
                    "enc_blob": "This field is required",
                }
            )
        print(request.POST)
        print(f"views verifykeypass: enc_blob={enc_blob}")
        if verifyKeyPass(enc_blob):
            token = decryptKeyPass(enc_blob)
            print("views verifykeypass: after_decrypt old_token= " + token)
            user = Users.objects.get(token=token)
            try:
                secret = decryptPass(token, user.verification_string)
                if secret == settings.SECRET_KEY:
                    return JsonResponse({"status": "success", "old_id": user.id})
                else:
                    return JsonResponse({"status": "fail"})
            except:
                return JsonResponse({"status": "fail"})
        else:
            return JsonResponse({"status": "fail"})


@csrf_exempt
def restoreAll(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        enc_blob = request.POST.get("enc_blob", None)
        if username is None or password is None or enc_blob is None:
            return JsonResponse(
                {
                    "username": "This field is required",
                    "password": "This field is required",
                    "enc_blob": "This field is required",
                }
            )
        token = decryptKeyPass(enc_blob)
        print("views restoreAll: after_decrypt old_token= " + token)
        print(f"views restoreAll: username={username}, password={password}")
        user = Users.objects.get(token=token)
        userID = user.id
        pass_objs = Pass.objects.filter(owner_id=userID)
        notes_objs = SecNotes.objects.filter(owner_id=userID)
        cards_objs = Cards.objects.filter(owner_id=userID)
        files_objs = Files.objects.filter(owner_id=userID)
        new_token = genToken(username, password)
        print("views restoreAll: new_token= " + new_token)
        user.token = new_token
        user.verification_string = encryptPass(new_token, settings.SECRET_KEY).decode(
            "utf-8"
        )
        user.save()
        for pass_obj in pass_objs:
            pass_obj.password = encryptPass(
                new_token, decryptPass(token, pass_obj.password)
            ).decode("utf-8")
            pass_obj.save()
        for notes_obj in notes_objs:
            notes_obj.content = encryptPass(
                new_token, decryptPass(token, notes_obj.content)
            ).decode("utf-8")
            notes_obj.save()
        for cards_obj in cards_objs:
            cards_obj.card_number = encryptPass(
                new_token, decryptPass(token, cards_obj.card_number)
            ).decode("utf-8")
            cards_obj.card_exp = encryptPass(
                new_token, decryptPass(token, cards_obj.card_exp)
            ).decode("utf-8")
            cards_obj.card_cvv = encryptPass(
                new_token, decryptPass(token, cards_obj.card_cvv)
            ).decode("utf-8")
            cards_obj.save()
        for files_obj in files_objs:
            reencryptFile2(token, new_token, files_obj.encrypted_file_name)
        response = JsonResponse(
            {
                "status": "success",
                "new_keypass": genKeyPass(username, password).decode("utf-8"),
            }
        )
        return response
    else:
        return JsonResponse({"status": "invalid request"})
