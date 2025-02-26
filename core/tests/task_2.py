from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import Pet, PetMedicalCondition, Owner, MedicalCondition, Species
import uuid


class PetEstimateTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create owners in different provinces
        self.ontario_owner = Owner.objects.create(
            first_name="John", last_name="Smith", province="ON"
        )

        self.bc_owner = Owner.objects.create(
            first_name="Jane", last_name="Doe", province="BC"
        )

        self.alberta_owner = Owner.objects.create(
            first_name="Bob", last_name="Johnson", province="AB"
        )

        # Create eligible pets
        self.young_dog = Pet.objects.create(
            name="Buddy", species=Species.DOG, age=3, owner=self.ontario_owner
        )

        self.young_cat = Pet.objects.create(
            name="Whiskers", species=Species.CAT, age=5, owner=self.bc_owner
        )

        # Create ineligible pets
        self.old_dog = Pet.objects.create(
            name="Max", species=Species.DOG, age=9, owner=self.alberta_owner
        )

        self.old_cat = Pet.objects.create(
            name="Felix", species=Species.CAT, age=11, owner=self.ontario_owner
        )

        self.other_animal = Pet.objects.create(
            name="Hammy", species=Species.OTHER, age=2, owner=self.bc_owner
        )

        # Create pets with medical conditions
        self.dog_with_diabetes = Pet.objects.create(
            name="Rocky", species=Species.DOG, age=4, owner=self.ontario_owner
        )
        PetMedicalCondition.objects.create(
            pet=self.dog_with_diabetes, condition=MedicalCondition.DIABETES
        )

        self.cat_with_cancer = Pet.objects.create(
            name="Mittens", species=Species.CAT, age=6, owner=self.bc_owner
        )
        PetMedicalCondition.objects.create(
            pet=self.cat_with_cancer, condition=MedicalCondition.CANCER
        )

        self.dog_with_multiple_conditions = Pet.objects.create(
            name="Charlie", species=Species.DOG, age=5, owner=self.ontario_owner
        )
        PetMedicalCondition.objects.create(
            pet=self.dog_with_multiple_conditions,
            condition=MedicalCondition.HEART_DISEASE,
        )
        PetMedicalCondition.objects.create(
            pet=self.dog_with_multiple_conditions, condition=MedicalCondition.OTHER
        )

    def test_estimate_eligible_dog_ontario(self):
        """Test that a young dog in Ontario gets the correct insurance cost."""
        # Act
        response = self.client.post(
            reverse("pet-estimate", kwargs={"pk": self.young_dog.id})
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["eligible"])
        # Base cost: $2 * 3 years = $6, multiplied by 1.5 for Ontario = $9
        self.assertEqual(response.data["costOfInsurance"], 9.0)

    def test_estimate_eligible_cat_bc(self):
        """Test that a young cat in BC gets the correct insurance cost."""
        # Act
        response = self.client.post(
            reverse("pet-estimate", kwargs={"pk": self.young_cat.id})
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["eligible"])
        # Base cost: $2 * 5 years = $10, multiplied by 1.25 for BC = $12.5
        self.assertEqual(response.data["costOfInsurance"], 12.5)

    def test_estimate_ineligible_species(self):
        """Test that animals other than cats or dogs are ineligible."""
        # Act
        response = self.client.post(
            reverse("pet-estimate", kwargs={"pk": self.other_animal.id})
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["eligible"])
        self.assertEqual(response.data["reason"], "SPECIES")

    def test_estimate_ineligible_old_dog(self):
        """Test that dogs over 8 years old are ineligible."""
        # Act
        response = self.client.post(
            reverse("pet-estimate", kwargs={"pk": self.old_dog.id})
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["eligible"])
        self.assertEqual(response.data["reason"], "AGE")

    def test_estimate_ineligible_old_cat(self):
        """Test that cats over 10 years old are ineligible."""
        # Act
        response = self.client.post(
            reverse("pet-estimate", kwargs={"pk": self.old_cat.id})
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["eligible"])
        self.assertEqual(response.data["reason"], "AGE")

    def test_estimate_ineligible_cancer(self):
        """Test that pets with cancer are ineligible."""
        # Act
        response = self.client.post(
            reverse("pet-estimate", kwargs={"pk": self.cat_with_cancer.id})
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["eligible"])
        self.assertEqual(response.data["reason"], "HEALTH")

    def test_estimate_eligible_with_diabetes(self):
        """Test that pets with diabetes get the correct additional cost."""
        # Act
        response = self.client.post(
            reverse("pet-estimate", kwargs={"pk": self.dog_with_diabetes.id})
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["eligible"])
        # Base cost: $2 * 4 years = $8, multiplied by 1.5 for Ontario = $12, plus $8 for diabetes = $20
        self.assertEqual(response.data["costOfInsurance"], 20.0)

    def test_estimate_eligible_with_multiple_conditions(self):
        """Test that pets with multiple conditions get the correct additional costs."""
        # Act
        response = self.client.post(
            reverse("pet-estimate", kwargs={"pk": self.dog_with_multiple_conditions.id})
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["eligible"])
        # Base cost: $2 * 5 years = $10, multiplied by 1.5 for Ontario = $15
        # Plus $5 for heart disease and $5 for other condition = $25
        self.assertEqual(response.data["costOfInsurance"], 25.0)

    def test_estimate_pet_not_found(self):
        """Test that requesting an estimate for a non-existent pet returns 404."""
        # Act
        response = self.client.post(
            reverse("pet-estimate", kwargs={"pk": uuid.uuid4()})
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
