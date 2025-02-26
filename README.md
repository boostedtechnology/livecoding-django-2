# Pet Insurance 

To get started on Mac, assuming Python 3.13.2 is already installed:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
``` 

To confirm everything is working, run `python manage.py test core.tests.accounts` to make sure the base functionality it working.

The other test files are defined but should not work until you implement the tasks.

## Task 1: Implement DELETE /accounts/:id/ endpoint

We want to be able to delete an account by its ID. Add a new endpoint to the controller to delete an account by its ID.

Run `python manage.py test petinsurance.petinsurance.tests.base` to test if it works.

## Task 1: Allow adding medical history to pets

**Context**

To improve our underwriting processes, we want to add medical history to our pet information.

**Task**

Create two endpoints: one to create and one to delete medical conditions on a specific pet.

* POST `/pet/<id>/medical-conditions`

* DELETE `/pet/<id>/medical-conditions/<condition_id>`

Run `python manage.py test petinsurance.petinsurance.tests.task_1` to test if it works.

## Task 2: Create an underwriting calculation

Create a new endpoint for computing the cost of insuring a specific pet.

* POST `/pet/<id>/estimate`

The response of the endpoint should be, in the case where the pet is eligible for insurance:

```json
{
    "eligible": true,
    "costOfInsurance": 24.56,
}
```

and in the case of ineligibility:

```json
{
    "eligible": false,
    "reason": "SPECIES" | "AGE" | "HEALTH"
}
```

The rules for underwriting are as follows:

* Animals other than cats or dogs cannot be insured (ineligible).

* Dogs over the age of 8 and cats over the age of 10 cannot be insured (ineligible).

* For each year of age, the base cost of insurance $2 per year. For example, 1 year old means $2 and 3 years old means $6.

* Multiply the base cost by 1.5 for Ontario and 1.25 for British Columbia, based on the pet owner's province.

* Cancer in the medical history means a pet is ineligible. A history of diabetes adds $8 to the cost of insurance and all other conditions add $5.


## Task 3: List all pets for a pet owner

Create the GET `/owners/<id>/pets` endpoint

Each pet in the response should include the pet's ID, name, species, and insurance eligibility status (from task 2)

Example response body:

```json
[
    {
        "id": <id1>,
        "name": "Dodge",
        "species": "DOG",
        "eligible": true,
    },
    {
        "id": <id2>,
        "name": "Shadow",
        "species": "CAT",
        "eligible": false,
    }
]

