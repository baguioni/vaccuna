from django.contrib import admin
from registrant.models import Individual


@admin.register(Individual)
class RegistrantAdmin(admin.ModelAdmin):
    pass
