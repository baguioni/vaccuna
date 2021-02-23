import factory
from factory import fuzzy
import datetime
from core.models import User, AddressField
from registrant.models import Registrant, Individual
from factory.django import DjangoModelFactory
from random import choice, uniform, randint
from lgu.models import LocalGovernmentUnit
from registrant.tasks import AssignPriorityGroup


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


class IndividualFactory(DjangoModelFactory):
    class Meta:
        model = Individual

    first_name = factory.Faker("first_name")
    middle_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birthday = factory.fuzzy.FuzzyDate(
        start_date=datetime.date(1, 1, 1),
        end_date=datetime.date.today() - datetime.timedelta(days=20 * 365),
    )

    cancer = choice([True, False, False, False, False])
    lgu = CEBU_CITY


def GenerateRegistrants(count):
    job = [
        'is_frontline_worker',
        'is_frontline_personnel',
        'is_uniformed_personnel',
        'is_teacher_or_social_worker',
        'is_government_worker',
        'is_overseas_filipino_worker',
        'is_employed',
    ]
    for i in range(count):
        registrant = RegistrantFactory()
        for i in range(randint(1,5)):

            individual = IndividualFactory.build()
            if choice([True, False]):
                setattr(individual, job[randint(0,6)], True)
            individual.registrant = registrant
            AssignPriorityGroup(individual)
            individual.save()
