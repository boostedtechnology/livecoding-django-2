from django.db import models
import uuid

class Province(models.TextChoices):
    ALBERTA = 'AB'
    BRITISH_COLUMBIA = 'BC'
    MANITOBA = 'MB'
    NEW_BRUNSWICK = 'NB'
    NEWFOUNDLAND_AND_LABRADOR = 'NL'
    NOVA_SCOTIA = 'NS'
    ONTARIO = 'ON'
    PRINCE_EDWARD_ISLAND = 'PE'
    QUEBEC = 'QC'
    SASKATCHEWAN = 'SK'
    YUKON = 'YT'
    NORTHWEST_TERRITORIES = 'NT'
    NUNAVUT = 'NU'

class Owner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.TextField()
    last_name = models.TextField()
    province = models.CharField(max_length=2, choices=Province.choices)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Species(models.TextChoices):
    DOG = 'DOG'
    CAT = 'CAT'
    OTHER = 'OTHER'

# Pet associated with an owner
class Pet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    species = models.CharField(max_length=6, choices=Species.choices)
    age = models.IntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} the {self.species.lower()}"


class MedicalCondition(models.TextChoices):
    CANCER = 'CANCER'
    DIABETES = 'DIABETES'
    HEART_DISEASE = 'HEART_DISEASE'
    OTHER = 'OTHER'

# Medical condition associated with a pet, stored in a separate table
class PetMedicalCondition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    condition = models.CharField(max_length=50, choices=MedicalCondition.choices)
