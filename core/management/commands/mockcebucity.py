from django.core.management.base import BaseCommand, CommandError

from vaccuna.generate import (GenerateAppointments, GenerateCebuCity,
                              GenerateMockRegistrants)


class Command(BaseCommand):
    help = 'Generate Cebu City, it\'s vaccination sites and registrants'

    def add_arguments(self, parser):
        parser.add_argument('number_of_registrants', nargs='+', type=int)

    def handle(self, *args, **options):
        cebu_city = GenerateCebuCity()
        GenerateMockRegistrants(options['number_of_registrants'][0], cebu_city)
        GenerateAppointments(cebu_city)
