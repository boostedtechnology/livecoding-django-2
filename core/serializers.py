from rest_framework import serializers
from .models import PetMedicalCondition, Pet, Owner

class PetMedicalConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetMedicalCondition
        fields = ['id', 'pet', 'condition']

class PetMedicalConditionCreateSerializer(serializers.Serializer):
    condition = serializers.CharField(max_length=255)

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'age', 'owner']

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id', 'first_name', 'last_name', 'province']
