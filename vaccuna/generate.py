import factory
from core.models import User, AddressField
from registrant.models import Registrant
from factory.django import DjangoModelFactory
from random import choice, uniform
from lgu.models import LocalGovernmentUnit

CENTER_LAT = [10.369880, 10.325517, 10.293783]
CENTER_LONG = [123.899296, 123.886994,123.864835]
CEBU_CITY = LocalGovernmentUnit.objects.get(id=1)

def RandomCoordinate(center, radius):
    return round(choice(center)+choice([-1, 1])*uniform(0, radius), 6)

def GenerateLat():
    return round(choice(CENTER_LAT)+choice([-1, 1])*uniform(0, 0.030000), 6)

def GenerateLong():
    return round(choice(CENTER_LONG)+choice([-1, 1])*uniform(0, 0.020000), 6)


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = AddressField

    latitude = factory.LazyFunction(GenerateLat)
    longitude = factory.LazyFunction(GenerateLong)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("credit_card_number")
    is_registrant = True


class RegistrantFactory(DjangoModelFactory):
    class Meta:
        model = Registrant

    is_household = choice([True, False])
    address = factory.SubFactory(AddressFactory)
    lgu = CEBU_CITY
    user = factory.SubFactory(UserFactory)

def GenerateRegistrants(count):
    for i in range(count):
        RegistrantFactory()
