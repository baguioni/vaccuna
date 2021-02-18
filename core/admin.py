from django.contrib import admin
from core.models import AddressField

@admin.register(AddressField)
class AddressFieldAdmin(admin.ModelAdmin):
    list_display = ('get_inline_address',)
