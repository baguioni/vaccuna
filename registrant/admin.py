from django.contrib import admin
from registrant.models import Individual, Registrant


@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', )


@admin.register(Registrant)
class RegistrantAdmin(admin.ModelAdmin):
    pass
