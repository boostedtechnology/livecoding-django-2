from rest_framework.response import Response
from rest_framework import generics, status
from .models import Owner, Pet, PetMedicalCondition
from .serializers import (
    OwnerSerializer,
    PetSerializer,
    PetMedicalConditionSerializer,
    PetMedicalConditionCreateSerializer,
    PetEstimateSerializer,
)


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
        pet_id = kwargs.get("pk")
        condition_id = kwargs.get("condition_pk")
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class PetMedicalConditionListCreateView(generics.ListCreateAPIView):
    queryset = PetMedicalCondition.objects.all()
    serializer_class = PetMedicalConditionSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PetMedicalConditionCreateSerializer
        return super().get_serializer_class()

    # Retrieve all the medical conditions for a specific pet
    def list(self, request, *args, **kwargs):
        pet_id = kwargs.get("pk")
        pet = Pet.objects.filter(id=pet_id).first()
        if not pet:
            return Response(status=status.HTTP_404_NOT_FOUND)

        medical_conditions = PetMedicalCondition.objects.filter(pet=pet)
        serializer = self.get_serializer(medical_conditions, many=True)
        return Response(serializer.data)

    # Task 1
    # Create a medical condition for a pet
    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class PetEstimateView(generics.RetrieveAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetEstimateSerializer

    def get_object(self):
        return self.get_queryset().filter(id=self.kwargs.get("pk")).first()

    # Task 2
    # Compute the cost of insuring a specific pet
    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
