import factory
from factory import fuzzy
import datetime
from core.models import User, AddressField
from registrant.models import Registrant, Individual
from factory.django import DjangoModelFactory
from random import choice, uniform, randint
from lgu.models import LocalGovernmentUnit, VaccinationSite, PriorityLocation
from registrant.tasks import AssignPriorityGroup

# Random locations in City
CENTER_LAT = [10.369880, 10.325517, 10.293783, 10.3905245]
CENTER_LONG = [123.899296, 123.886994,123.864835, 123.907329]

def RandomCoordinate(center, radius):
    return round(choice(center)+choice([-1, 1])*uniform(0, radius), 6)

def GenerateLat():
    return round(choice(CENTER_LAT)+choice([-1, 1])*uniform(0, 0.030000), 6)

def GenerateLong():
    return round(choice(CENTER_LONG)+choice([-1, 1])*uniform(0, 0.020000), 6)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("credit_card_number")
    is_registrant = True

def GenerateCebuCity():
    user = UserFactory(
        is_registrant=False,
        is_lgu=True,
        first_name='Cebu',
        last_name='City',
    )

    cebu_city = LocalGovernmentUnit.objects.create(
        name="Cebu City",
        latitude=10.2929,
        longitude=123.9017,
        user=user
    )

    vaccinations_sites = (
        ('Banawa Health Center', 10.313075658278146, 123.87873325715285, 500),
        ('Cebu City Health Department', 10.308020183444768, 123.90914714181325, 700),
        ('Banilad Health Center', 10.346957228916628, 123.91256807101787, 600),
        ('Kasambagan Health Center', 10.324775525623524, 123.91091651482282, 700),
        ('Pit-os Health Center', 10.401299847952568, 123.92203047545613, 400),
        ('Talamban Health Center', 10.370149714903702, 123.9183207148935, 700),
        ('Basak Pardo Health Center', 10.290336098752293, 123.86532682529544, 600),
        ('Ermita Health Center', 10.29132410087735, 123.89745609706983, 500)
    )

    for vs in vaccinations_sites:
        VaccinationSite.objects.create(
            name=vs[0],
            address=AddressField.objects.create(latitude=vs[1], longitude=vs[2]),
            daily_capacity=vs[3],
            lgu=cebu_city,
    )

    # Based from
    # https://www.rappler.com/newsbreak/iq/things-to-know-cebu-city-post-holiday-christmas-new-year-covid-19-surge-january-2021
    priority_locations = (
        'Guadalupe',
        'Basak San Nicolas',
        'Lahug (Pob.)',
        'Mambaling',
    )

    for pl in priority_locations:
        PriorityLocation.objects.create(
            address=AddressField.objects.create(
                barangay=pl,
                city='Cebu City',
                province='Cebu',
            ),
            lgu=cebu_city
        )

    return cebu_city


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = AddressField

    latitude = factory.LazyFunction(GenerateLat)
    longitude = factory.LazyFunction(GenerateLong)


class RegistrantFactory(DjangoModelFactory):
    class Meta:
        model = Registrant

    is_household = choice([True, False])
    address = factory.SubFactory(AddressFactory)
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
    # Simulate A2 priority group
    cancer = choice([True, False, False, False, False])

def GenerateMockRegistrants(count, lgu):
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
        registrant = RegistrantFactory(lgu=lgu)
        for i in range(randint(1,5)):

            individual = IndividualFactory.build()
            if choice([True, False]):
                setattr(individual, job[randint(0,6)], True)
            individual.registrant = registrant
            individual.lgu = lgu
            AssignPriorityGroup(individual)
            individual.save()
