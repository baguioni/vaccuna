from django.contrib import admin
from .models import QR
from .models import sms
from core.models import AddressField, User

admin.site.register(QR)
admin.site.register(sms)


@admin.register(AddressField)
class AddressFieldAdmin(admin.ModelAdmin):
    list_display = ('get_inline_address',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
