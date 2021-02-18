from django.contrib import admin

from core.models import AddressField, User


@admin.register(AddressField)
class AddressFieldAdmin(admin.ModelAdmin):
    list_display = ('get_inline_address',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
