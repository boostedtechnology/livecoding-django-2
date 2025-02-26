from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import Pet, PetMedicalCondition, Owner, MedicalCondition, Species
import uuid


class PetMedicalConditionTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Test that all medical conditions can be retrieved for a pet
    def test_list_medical_conditions(self):
        # Arrange
        owner = Owner.objects.create(
            first_name="John", last_name="Marner", province="AB"
        )
        pet = Pet.objects.create(name="Rex", species=Species.OTHER, age=7, owner=owner)
        PetMedicalCondition.objects.create(pet=pet, condition=MedicalCondition.CANCER)
        PetMedicalCondition.objects.create(pet=pet, condition=MedicalCondition.DIABETES)

        # Act
        response = self.client.get(
            reverse("pet-medical-condition-list-create", kwargs={"pk": pet.id})
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # Test that medical conditions cannot be retrieved for a non-existent pet
    def test_list_medical_conditions_not_found(self):
        # Act
        response = self.client.get(
            reverse("pet-medical-condition-list-create", kwargs={"pk": uuid.uuid4()})
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test that a medical condition can be created for a pet
    def test_create_medical_condition(self):
        # Arrange
        owner = Owner.objects.create(
            first_name="Alex", last_name="MacDonald", province="ON"
        )
        pet = Pet.objects.create(name="Shadow", species="CAT", age=11, owner=owner)

        # Act
        response = self.client.post(
            reverse("pet-medical-condition-list-create", kwargs={"pk": pet.id}),
            {"condition": MedicalCondition.CANCER},
        )

        # Assert
        medical_conditions = PetMedicalCondition.objects.filter(pet=pet)
        self.assertEqual(medical_conditions.count(), 1)
        self.assertEqual(medical_conditions[0].condition, MedicalCondition.CANCER)

    # Test that a medical condition cannot be created for a non-existent pet
    def test_create_medical_condition_not_found(self):
        # Act
        response = self.client.post(
            reverse("pet-medical-condition-list-create", kwargs={"pk": uuid.uuid4()}),
            {"condition": MedicalCondition.CANCER},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_medical_condition(self):
        # Arrange
        owner = Owner.objects.create(
            first_name="Jackson", last_name="Why", province="ON"
        )
        pet = Pet.objects.create(name="Fido", species="DOG", age=3, owner=owner)
        medical_condition = PetMedicalCondition.objects.create(
            pet=pet, condition=MedicalCondition.DIABETES
        )
        self.destroy_url = reverse(
            "pet-medical-condition-destroy",
            kwargs={"pk": pet.pk, "condition_pk": medical_condition.pk},
        )

        # Act
        response = self.client.delete(self.destroy_url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PetMedicalCondition.objects.filter(pet=pet.id).count(), 0)

    def test_delete_medical_condition_not_found(self):
        # Act
        response = self.client.delete(
            reverse(
                "pet-medical-condition-destroy",
                kwargs={"pk": uuid.uuid4(), "condition_pk": uuid.uuid4()},
            )
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
