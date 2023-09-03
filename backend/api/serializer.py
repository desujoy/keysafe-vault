from rest_framework import serializers
from .models import PassDB, SecNotesDB, CardsDB, FileDB


class PassDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassDB
        fields = '__all__'

class SecNotesDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecNotesDB
        fields = '__all__'

class CardsDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardsDB
        fields = '__all__'

class FileDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileDB
        fields = '__all__'

