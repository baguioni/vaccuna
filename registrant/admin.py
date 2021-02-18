from django.contrib import admin
from registrant.models import Individual


@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', )
