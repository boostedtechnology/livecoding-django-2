from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from .models import Owner, Pet, PetMedicalCondition
from .serializers import OwnerSerializer, PetSerializer, PetMedicalConditionSerializer, PetMedicalConditionCreateSerializer


class OwnerListCreateView(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

class OwnerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

class PetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class PetListCreateView(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class PetMedicalConditionDestroyView(generics.DestroyAPIView):
    queryset = PetMedicalCondition.objects.all()
    serializer_class = PetMedicalConditionSerializer

    # Task 1
    # Delete a medical condition from a pet
    def destroy(self, request, *args, **kwargs):
        pet_id = kwargs.get('pk')
        pet = Pet.objects.filter(id=pet_id).first()
        if not pet:
            return Response(status=status.HTTP_404_NOT_FOUND)

        condition_id = kwargs.get('condition_pk')

        try:
            PetMedicalCondition.objects.filter(pet_id=pet_id, id=condition_id).delete();
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PetMedicalCondition.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class PetMedicalConditionListCreateView(generics.ListCreateAPIView):
    queryset = PetMedicalCondition.objects.all()
    serializer_class = PetMedicalConditionSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PetMedicalConditionCreateSerializer
        return super().get_serializer_class()

    # Retrieve all the medical conditions for a specific pet
    def list(self, request, *args, **kwargs):
        pet_id = kwargs.get('pk')
        pet = Pet.objects.filter(id=pet_id).first()
        if not pet:
            return Response(status=status.HTTP_404_NOT_FOUND)

        medical_conditions = PetMedicalCondition.objects.filter(pet=pet)
        serializer = self.get_serializer(medical_conditions, many=True)
        return Response(serializer.data)

    # Task 1
    # Create a medical condition for a pet
    def post(self, request, *args, **kwargs):
        pet_id = kwargs.get('pk')
        pet = Pet.objects.filter(id=pet_id).first()
        if not pet:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        PetMedicalCondition.objects.create(pet_id=pet_id, condition=serializer.validated_data.get('condition'))
        return Response(status=status.HTTP_201_CREATED)

