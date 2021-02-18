from django.contrib import admin
from registrant.models import Individual, AddressField


@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', )

@admin.register(AddressField)
class AddressFieldAdmin(admin.ModelAdmin):
    list_display = ('get_inline_address',)
