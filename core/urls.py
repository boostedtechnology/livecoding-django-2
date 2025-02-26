from django.urls import path
from .views import (
    OwnerListCreateView,
    OwnerRetrieveUpdateDestroyView,
    PetListCreateView,
    PetRetrieveUpdateDestroyView,
    PetMedicalConditionDestroyView,
    PetMedicalConditionListCreateView,
)

urlpatterns = [
    path('owners/', OwnerListCreateView.as_view(), name='owner-list-create'),
    path('owners/<uuid:pk>/', OwnerRetrieveUpdateDestroyView.as_view(), name='owner-retrieve-update-destroy'),

    path('pets/', PetListCreateView.as_view(), name='pet-list-create'),
    path('pets/<uuid:pk>/', PetRetrieveUpdateDestroyView.as_view(), name='pet-retrieve-update-destroy'),

    # Task 1
    path('pets/<uuid:pk>/medical-conditions/<uuid:condition_pk>', PetMedicalConditionDestroyView.as_view(), name='pet-medical-condition-destroy'),
    path('pets/<uuid:pk>/medical-conditions/', PetMedicalConditionListCreateView.as_view(), name='pet-medical-condition-list-create'),

    # Task 2
    # path('pets/<uuid:pk>/quote/', PetQuoteView.as_view(), name='pet-quote'),

    # Task 3
    # path('owners/<int:pk>/pets/', PetListCreateView.as_view(), name='pet-list-create'),
]
