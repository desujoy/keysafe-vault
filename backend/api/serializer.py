from rest_framework import serializers
from .models import Pass, SecNotes, Cards, Files


class PassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pass
        fields = '__all__'

class SecNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecNotes
        fields = '__all__'

class CardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = '__all__'

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'

