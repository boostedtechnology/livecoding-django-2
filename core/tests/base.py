from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import Pet, Owner, Species
import uuid


class OwnerTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Test that all owners can be retrieved
    def test_list_owners(self):
        # Arrange
        owner = Owner.objects.create(
            first_name="John", last_name="Marner", province="AB"
        )
        owner = Owner.objects.create(
            first_name="Alex", last_name="MacDonald", province="ON"
        )

        # Act
        response = self.client.get(reverse("owner-list-create"))

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_owner(self):
        # Act
        response = self.client.post(
            reverse("owner-list-create"),
            {"first_name": "Alex", "last_name": "MacDonald", "province": "ON"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Owner.objects.filter(
                first_name="Alex", last_name="MacDonald", province="ON"
            ).count(),
            1,
        )

    def test_create_owner_invalid_no_province(self):
        # Act
        response = self.client.post(
            reverse("owner-list-create"),
            {"first_name": "Alex", "last_name": "MacDonald"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_owner_invalid_bad_province(self):
        # Act
        response = self.client.post(
            reverse("owner-list-create"),
            {"first_name": "Alex", "last_name": "MacDonald", "province": "XX"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_pets(self):
        # Arrange
        owner = Owner.objects.create(
            first_name="John", last_name="Marner", province="AB"
        )
        pet = Pet.objects.create(name="Rex", species=Species.OTHER, age=7, owner=owner)

        # Act
        response = self.client.get(reverse("pet-list-create"))

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_pet(self):
        # Arrange
        owner = Owner.objects.create(
            first_name="John", last_name="Marner", province="AB"
        )
        # Act
        response = self.client.post(
            reverse("pet-list-create"),
            {"name": "Rex", "species": Species.OTHER, "age": 7, "owner": owner.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Pet.objects.filter(
                name="Rex", species=Species.OTHER, age=7, owner=owner
            ).count(),
            1,
        )

    def test_create_pet_invalid_no_owner(self):
        # Act
        response = self.client.post(
            reverse("pet-list-create"),
            {"name": "Rex", "species": Species.OTHER, "age": 7},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_pet_invalid_bad_species(self):
        # Act
        response = self.client.post(
            reverse("pet-list-create"),
            {"name": "Rex", "species": "XX", "age": 7, "owner": uuid.uuid4()},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_pet(self):
        # Arrange
        owner = Owner.objects.create(
            first_name="John", last_name="Marner", province="AB"
        )
        pet = Pet.objects.create(name="Rex", species=Species.OTHER, age=7, owner=owner)

        # Act
        response = self.client.delete(
            reverse("pet-retrieve-update-destroy", kwargs={"pk": pet.id})
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pet.objects.filter(id=pet.id).count(), 0)

    def test_delete_pet_not_found(self):
        # Act
        response = self.client.delete(
            reverse("pet-retrieve-update-destroy", kwargs={"pk": uuid.uuid4()})
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
